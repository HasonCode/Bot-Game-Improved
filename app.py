#!/usr/bin/env python3
"""
Flask web application for the Bot Game
Production-ready version with security and configuration improvements
"""

import os
import re
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv
from python_decoder import Grid, Bot, interpreter, count_bot_commands, WinInterruption
import grids

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Security Configuration
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours

# CORS Configuration
CORS(app, origins=os.environ.get('ALLOWED_ORIGINS', '*').split(','))

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
    
    def turn_right(self):
        super().turn_right()
        self.capture_frame("Turn right")
    
    def turn_left(self):
        super().turn_left()
        self.capture_frame("Turn left")

def is_code_safe(code):
    """Basic security check for code safety"""
    dangerous_patterns = [
        r'import\s+(os|sys|subprocess|socket|urllib|requests|http|ftplib)',
        r'__import__\s*\(',
        r'exec\s*\(',
        r'eval\s*\(',
        r'compile\s*\(',
        r'open\s*\(',
        r'file\s*\(',
        r'input\s*\(',
        r'exit\s*\(',
        r'quit\s*\(',
        r'reload\s*\('
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            return False
    return True

@app.route('/')
def index():
    """Serve the main game page"""
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_code():
    """Execute bot code and return results"""
    try:
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({'success': False, 'error': 'No code provided'})
        
        code = data['code']
        level_number = data.get('level', current_level)
        
        # Security check
        if not is_code_safe(code):
            return jsonify({
                'success': False, 
                'error': 'Code contains potentially unsafe operations'
            })
        
        # Get the grid for the specified level
        game_grid = grids.create_grid(level_number)
        
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
            exec(clean_code, {'bot': bot})
            
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
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Execution error: {str(e)}'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

@app.route('/grid')
def get_grid():
    """Get the current grid state for a specific level"""
    level_number = request.args.get('level', current_level, type=int)
    
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
        return jsonify({'error': str(e)}), 404

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
        return jsonify({'error': str(e)}), 404


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

