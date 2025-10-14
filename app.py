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
        
        # Security check
        if not is_code_safe(code):
            return jsonify({
                'success': False, 
                'error': 'Code contains potentially unsafe operations'
            })
        
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
    """Get the current grid state"""
    bot = Bot(game_grid)
    return jsonify({
        'grid_state': str(bot),
        'max_commands': game_grid.par
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

