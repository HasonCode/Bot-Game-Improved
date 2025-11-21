#!/usr/bin/env python3
"""
Flask web application for the Bot Game
Production-ready version with security and configuration improvements
"""

import os
import re
import logging
from telnetlib import EL
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv
from python_decoder import Grid, Bot, interpreter, count_bot_commands, WinInterruption, execute_with_timeout
import grids
import signal
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Security: Validate required environment variables in production
FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
if FLASK_ENV == 'production':
    if not os.environ.get('SECRET_KEY'):
        logger.error("❌ SECURITY ERROR: SECRET_KEY not set in production mode!")
        raise ValueError("SECRET_KEY environment variable must be set in production mode. "
                        "Generate one with: python generate_secret.py")

app = Flask(__name__)

# Security Configuration
app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-secret-key-not-for-production')
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours

# Security Warning in development
if FLASK_ENV == 'development':
    logger.warning("⚠️  Running in development mode. Do NOT use this in production without:")
    logger.warning("   1. Setting SECRET_KEY in .env file")
    logger.warning("   2. Setting SESSION_COOKIE_SECURE=True in .env")
    logger.warning("   3. Setting ALLOWED_ORIGINS to your domain")
    logger.warning("   4. Deploying with HTTPS")

# CORS Configuration - restrict to specific origin
allowed_origins = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:5000')
if FLASK_ENV == 'production' and allowed_origins == 'http://localhost:5000':
    logger.warning("⚠️  CORS is still using localhost. Set ALLOWED_ORIGINS in production!")
CORS(app, origins=allowed_origins.split(','))

# Default level
current_level = 1

class AnimatedBot(Bot):
    """Bot class that captures each frame for animation"""
    
    def __init__(self, grid):
        super().__init__(grid)
        self.frames = []  # Store grid state after each action
        self.action_log = []
        self.capture_frame("Initial state")
    
    def capture_frame(self, action_description):
        """Capture current grid state as a frame"""
        self.frames.append({
            'grid_state': str(self),
            'action': action_description,
            'position': (self.i, self.j),
            'direction': self.direction,
            'alive': self.alive,
            'win_state': self.win_state
        })
        self.action_log.append(action_description)
    
    def move_forward(self):
        try:
            super().move_forward()
        except WinInterruption:
            # Bot reached the finish line - capture this winning state
            direction_name = ['up', 'left', 'down', 'right'][self.direction]
            self.capture_frame(f"Move forward ({direction_name}) - REACHED FINISH!")
            raise  # Re-raise the exception after capturing the frame
        
        direction_name = ['up', 'left', 'down', 'right'][self.direction]
        self.capture_frame(f"Move forward ({direction_name})")
    
    def move_backward(self):
        try:
            super().move_backward()
        except WinInterruption:
            # Bot reached the finish line - capture this winning state
            direction_name = ['up', 'left', 'down', 'right'][self.direction]
            self.capture_frame(f"Move backward ({direction_name}) - REACHED FINISH!")
            raise  # Re-raise the exception after capturing the frame
        
        direction_name = ['up', 'left', 'down', 'right'][self.direction]
        self.capture_frame(f"Move backward ({direction_name})")
    
    def turn_right(self):
        super().turn_right()
        self.capture_frame("Turn right")
    
    def turn_left(self):
        super().turn_left()
        self.capture_frame("Turn left")

def is_code_safe(code):
    """
    Enhanced security check for code safety using multiple layers:
    1. AST parsing to detect suspicious patterns
    2. Regex blacklist for additional protection
    """
    import ast
    
    # First, try to parse the code to catch syntax errors early
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        logger.warning(f"Syntax error in user code: {e}")
        return False
    
    # Dangerous built-in functions and attributes that could cause harm
    dangerous_names = {
        'exec', 'eval', '__import__', 'open', 'file', 'input', 'exit', 'quit',
        'compile', 'globals', 'locals', 'vars', 'getattr', 'setattr', 'delattr',
        'reload', 'breakpoint', '__builtins__', 'memoryview', 'bytearray'
    }
    
    dangerous_modules = {
        'os', 'sys', 'subprocess', 'socket', 'urllib', 'requests', 'http',
        'ftplib', 'smtplib', 'ssl', 'pdb', '__main__', 'importlib',
        'pickle', 'shelve', 'tempfile', 'shutil', 'glob'
    }
    
    # Walk through AST nodes
    for node in ast.walk(tree):
        # Check for import statements
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name.split('.')[0]
                    if module_name in dangerous_modules:
                        logger.warning(f"Blocked import: {module_name}")
                        return False
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.split('.')[0] in dangerous_modules:
                    logger.warning(f"Blocked import: {node.module}")
                    return False
        
        # Check for dangerous function calls
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in dangerous_names:
                logger.warning(f"Blocked function call: {node.func.id}")
                return False
            # Check for getattr-based imports: getattr(__builtins__, '__import__')
            if isinstance(node.func, ast.Name) and node.func.id == 'getattr':
                logger.warning("Blocked: getattr() not allowed")
                return False
        
        # Check for attribute access on builtins
        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id == '__builtins__':
                logger.warning("Blocked: Access to __builtins__")
                return False
    
    # Additional regex checks for obfuscated patterns
    dangerous_patterns = [
        r'__.*__',  # Dunder methods
        r'\\x[0-9a-fA-F]{2}',  # Hex escapes for obfuscation
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, code):
            logger.warning(f"Blocked: Suspicious pattern detected: {pattern}")
            return False
    
    return True

@app.route('/')
def index():
    """Serve the main game page"""
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_code():
    """Execute bot code and return results"""
    timeout_seconds = 30
    try:
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({'success': False, 'error': 'No code provided'})
        
        code = data['code']
        level_number = data.get('level', current_level)
        
        # Validate level number
        if not isinstance(level_number, int) or level_number < 1 or level_number > len(grids.ALL_LEVELS):
            logger.warning(f"Invalid level number attempted: {level_number}")
            return jsonify({
                'success': False, 
                'error': f'Invalid level number. Must be between 1 and {len(grids.ALL_LEVELS)}'
            })
        
        # Security check
        if not is_code_safe(code):
            return jsonify({
                'success': False, 
                'error': 'Code contains potentially unsafe operations. Please check your code and try again.'
            })
        
        # Get the grid for the specified level
        try:
            game_grid = grids.create_grid(level_number)
        except ValueError as e:
            logger.warning(f"Invalid level {level_number}: {e}")
            return jsonify({
                'success': False, 
                'error': f'Invalid level number'
            })
        
        # Explicitly reset the grid to ensure all keys and gates are restored
        game_grid.reset()
        
        # Create a new bot for this execution
        bot = AnimatedBot(game_grid)
        
        # Clean the code (remove imports except math)
        lines = code.split('\n')
        clean_lines = []
        for line in lines:
            if 'import' in line and 'math' not in line:
                continue
            clean_lines.append(line)
        clean_code = '\n'.join(clean_lines)
        
        # Execute the code
        try:
            # Use exec with the bot in the global namespace
            execute_with_timeout(clean_code, {'bot': bot}, timeout_seconds=timeout_seconds)
            
            # Get results
            command_count = count_bot_commands(clean_code)
            grid_state = str(bot)
            
            # Determine success
            if bot.win_state:
                if command_count <= game_grid.par:
                    message = '🌟 STAR! You completed the level efficiently!'
                else:
                    message = '✅ Success! But try to use fewer commands for a star.'
                success = True
            elif not bot.alive:
                message = '💀 Bot died! Try a different approach.'
                success = False
            else:
                message = 'Code executed but bot did not reach the goal.'
                success = False
            
            return jsonify({
                'success': success,
                'message': message,
                'grid_state': grid_state,
                'command_count': command_count,
                'win_state': bot.win_state,
                'alive': bot.alive,
                'action_log': bot.action_log,
                'frames': bot.frames  # Return all frames for animation
            })
            
        except WinInterruption:
            # Bot reached the finish line
            command_count = count_bot_commands(clean_code)
            grid_state = str(bot)
            
            if command_count <= game_grid.par:
                message = '🌟 STAR! You completed the level efficiently!'
            else:
                message = '✅ Success! But try to use fewer commands for a star.'
            
            return jsonify({
                'success': True,
                'message': message,
                'grid_state': grid_state,
                'command_count': command_count,
                'win_state': True,
                'alive': bot.alive,
                'action_log': bot.action_log,
                'frames': bot.frames  # Return all frames for animation
            })
        except TimeoutError as e:
            logger.warning(f"Code execution timeout: {str(e)}")
            return jsonify({
                    'success': False,
                    'error': f'Code execution exceeded the time limit ({timeout_seconds} seconds). Please check for infinite loops.'
                })
        except Exception as e:
            # Log the full error for debugging
            logger.error(f"Code execution error: {type(e).__name__}: {str(e)}", exc_info=True)
            # Return generic message to user
            return jsonify({
                'success': False,
                'error': f'An error occurred while executing your code. Please check your syntax and try again. Error: {e}'
            })
            
    except Exception as e:
        # Log the full error for debugging
        logger.error(f"Server error processing request: {type(e).__name__}: {str(e)}", exc_info=True)
        # Return generic message to user
        return jsonify({
            'success': False,
            'error': 'A server error occurred. Please try again later.'
        })

@app.route('/grid')
def get_grid():
    """Get the current grid state for a specific level"""
    level_number = request.args.get('level', current_level, type=int)
    
    # Validate level number
    if not isinstance(level_number, int) or level_number < 1 or level_number > len(grids.ALL_LEVELS):
        logger.warning(f"Invalid level number attempted: {level_number}")
        return jsonify({'error': 'Invalid level number'}), 400
    
    try:
        game_grid = grids.create_grid(level_number)
        bot = Bot(game_grid)
        level_info = grids.get_level_info(level_number)
        
        return jsonify({
            'grid_state': str(bot),
            'max_commands': game_grid.par,
            'level_info': level_info
        })
    except ValueError as e:
        logger.warning(f"Error loading level {level_number}: {e}")
        return jsonify({'error': 'Invalid level'}), 404

@app.route('/levels')
def get_levels():
    """Get list of all available levels with progress icons"""
    levels = grids.list_all_levels()
    
    # Add progress icons to each level
    for level in levels:
        level['icon'] = get_completion_icon(level['number'])
    
    return jsonify({
        'levels': levels,
        'total': len(grids.ALL_LEVELS)
    })

@app.route('/level/<int:level_number>')
def get_level_details(level_number):
    """Get detailed information about a specific level"""
    # Validate level number
    if level_number < 1 or level_number > len(grids.ALL_LEVELS):
        logger.warning(f"Invalid level number attempted: {level_number}")
        return jsonify({'error': 'Invalid level number'}), 400
    
    try:
        level_info = grids.get_level_info(level_number)
        game_grid = grids.create_grid(level_number)
        bot = Bot(game_grid)
        
        return jsonify({
            'level_info': level_info,
            'grid_state': str(bot),
            'grid_size': {
                'rows': game_grid.rows,
                'cols': game_grid.cols
            }
        })
    except ValueError as e:
        logger.warning(f"Error loading level {level_number}: {e}")
        return jsonify({'error': 'Invalid level'}), 404


def init_session_progress():
    """Initialize progress tracking in session if not exists"""
    if 'progress' not in session:
        session['progress'] = {}
        session.modified = True

def get_level_progress(level_number):
    """Get progress for a specific level from session"""
    init_session_progress()
    level_key = str(level_number)
    if level_key not in session['progress']:
        session['progress'][level_key] = {
            'completed': False,
            'best_commands': None,
            'attempts': 0,
            'has_star': False
        }
        session.modified = True
    return session['progress'][level_key]

def save_level_progress(level_number, commands_used, par, completed):
    """Save progress for a level"""
    init_session_progress()
    level_key = str(level_number)
    progress = get_level_progress(level_number)
    
    if completed:
        progress['completed'] = True
        
        # Determine what type of completion this is
        earned_star = commands_used <= par  # True for star, False for checkmark
        
        # Star/Checkmark logic:
        # - Complete at or below par = star (⭐)
        # - Complete above par = checkmark (✅)
        # - Star can replace checkmark (upgrade)
        # - Checkmark CANNOT replace star (no downgrade)
        
        if earned_star:
            # Always set star if earned (replaces checkmark if present)
            progress['has_star'] = True
        else:
            # Only set checkmark if we don't already have a star
            if not progress.get('has_star', False):
                progress['has_star'] = False
        
        # Update best score
        if progress['best_commands'] is None or commands_used < progress['best_commands']:
            progress['best_commands'] = commands_used
    
    session['progress'][level_key] = progress
    session.modified = True
    return progress

def get_progress_stats():
    """Get overall progress statistics"""
    init_session_progress()
    total_levels = len(grids.ALL_LEVELS)
    total_stars = 0
    levels_completed = 0
    
    for level_num in range(1, total_levels + 1):
        progress = get_level_progress(level_num)
        if progress.get('has_star', False):
            total_stars += 1
        if progress.get('completed', False):
            levels_completed += 1
    
    return {
        'total_stars': total_stars,
        'levels_completed': levels_completed,
        'total_levels': total_levels
    }

def get_completion_icon(level_number):
    """Get completion icon for a level based on progress"""
    progress = get_level_progress(level_number)
    
    if not progress.get('completed', False):
        return "⚪"  # Not completed
    
    # Binary system: star (par or better) or checkmark (over par)
    # These are mutually exclusive - if has_star is True, show star; otherwise checkmark
    if progress.get('has_star', False):
        return "⭐"  # Completed at or under par
    else:
        return "✅"  # Completed over par

@app.route('/progress/<int:level_number>')
def get_progress_route(level_number):
    """Get progress for a specific level"""
    try:
        progress = get_level_progress(level_number)
        icon = get_completion_icon(level_number)
        return jsonify({
            'progress': progress,
            'icon': icon,
            'success': True
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/progress/stats')
def progress_stats():
    """Get overall progress statistics"""
    try:
        stats = get_progress_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/progress/save', methods=['POST'])
def save_progress():
    """Save progress for a level"""
    try:
        data = request.get_json()
        level_number = data.get('level_number')
        commands_used = data.get('commands_used', 0)
        par = data.get('par', 999)
        completed = data.get('completed', False)
        
        progress = save_level_progress(level_number, commands_used, par, completed)
        
        return jsonify({
            'progress': progress,
            'success': True
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for deployment platforms"""
    return jsonify({
        'status': 'healthy',
        'app': 'Bot Game',
        'version': '1.0.0',
        'levels': len(grids.ALL_LEVELS),
        'features': [
            '15 progressive levels',
            'Star system',
            'Progress tracking',
            'Real-time animation',
            'Multiple bot commands'
        ]
    })


if __name__ == '__main__':
    # Production configuration
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    # Use gunicorn in production, Flask dev server in development
    if os.environ.get('FLASK_ENV') == 'production':
        print(f"🚀 Bot Game starting in production mode on port {port}")
        print("📊 Features: 15 levels, star system, progress tracking")
        print("🎮 Ready to play!")
    else:
        print(f"🔧 Bot Game starting in development mode on port {port}")
        print("📊 Features: 15 levels, star system, progress tracking")
        print("🎮 Ready to play!")
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

