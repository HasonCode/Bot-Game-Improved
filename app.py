#!/usr/bin/env python3
"""
Flask web application for the Bot Game
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from python_decoder import Grid, Bot, interpreter, count_bot_commands, WinInterruption
import re
import time
import threading

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the game grid (same as in python_decoder.py)
GRID_DATA = [
    [1,1,1,1,1],
    [1,0,0,3,1],
    [1,0,1,1,1],
    [1,0,1,1,1],
    [1,0,1,1,1]
]
ROBOT_START = (4,1)
DIRECTION = 0
MAX_COMMANDS = 3

# Create the game grid
game_grid = Grid(GRID_DATA, ROBOT_START, DIRECTION, MAX_COMMANDS)

class DelayedBot(Bot):
    """Bot class with delay between actions for visualization"""
    
    def __init__(self, grid, delay=0.5):
        super().__init__(grid)
        self.delay = delay
        self.action_log = []
    
    def move_forward(self):
        super().move_forward()
        self.action_log.append(f"Move forward (direction: {['up', 'left', 'down', 'right'][self.direction]})")
        time.sleep(self.delay)
    
    def turn_right(self):
        super().turn_right()
        self.action_log.append("Turn right")
        time.sleep(self.delay)
    
    def turn_left(self):
        super().turn_left()
        self.action_log.append("Turn left")
        time.sleep(self.delay)

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
        
        # Security check
        if not is_code_safe(code):
            return jsonify({
                'success': False, 
                'error': 'Code contains potentially unsafe operations'
            })
        
        # Get delay parameter (default 0.5 seconds)
        delay = data.get('delay', 0.5)
        
        # Create a new bot for this execution
        bot = DelayedBot(game_grid, delay)
        
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
                'action_log': bot.action_log
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
                'action_log': bot.action_log
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

@app.route('/execute-step', methods=['POST'])
def execute_step():
    """Execute one step of bot code for step-by-step visualization"""
    try:
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({'success': False, 'error': 'No code provided'})
        
        code = data['code']
        step = data.get('step', 0)
        
        # Security check
        if not is_code_safe(code):
            return jsonify({
                'success': False, 
                'error': 'Code contains potentially unsafe operations'
            })
        
        # Create bot and execute one command
        bot = DelayedBot(game_grid, 0.1)  # Short delay for step execution
        
        # Parse code to get individual commands
        lines = code.split('\n')
        clean_lines = []
        for line in lines:
            if 'import' in line and 'math' not in line:
                continue
            clean_lines.append(line)
        
        # Execute one command at a time
        commands_executed = 0
        for line in clean_lines:
            if commands_executed >= step + 1:
                break
                
            line = line.strip()
            if 'bot.move_forward()' in line and (line.find('#') == -1 or line.find('#') > line.find('bot.move_forward()')):
                bot.move_forward()
                commands_executed += 1
            elif 'bot.turn_left()' in line and (line.find('#') == -1 or line.find('#') > line.find('bot.turn_left()')):
                bot.turn_left()
                commands_executed += 1
            elif 'bot.turn_right()' in line and (line.find('#') == -1 or line.find('#') > line.find('bot.turn_right()')):
                bot.turn_right()
                commands_executed += 1
        
        return jsonify({
            'success': True,
            'grid_state': str(bot),
            'step': step,
            'total_steps': len([l for l in clean_lines if any(cmd in l for cmd in ['bot.move_forward()', 'bot.turn_left()', 'bot.turn_right()'])]),
            'win_state': bot.win_state,
            'alive': bot.alive,
            'last_action': bot.action_log[-1] if bot.action_log else None
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Step execution error: {str(e)}'
        })

@app.route('/grid')
def get_grid():
    """Get the current grid state"""
    bot = Bot(game_grid)
    return jsonify({
        'grid_state': str(bot),
        'max_commands': game_grid.par
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

