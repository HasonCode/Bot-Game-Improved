# 🤖 Bot Game - Flask Web Application

A web-based coding game where you write Python code to control a bot and navigate through a grid to reach the finish line.

## 🚀 Quick Start

### 1. Start the Server

```bash
cd "/home/hason/bot game"
python3 app.py
```

### 2. Open Your Browser

Navigate to: `http://localhost:5000`

### 3. Write Code & Watch the Animation!

Write Python code using the bot commands and click "Run Code" to see your bot move in real-time!

## 🎮 How It Works

### Animation System

The game features a **frame-by-frame animation system**:

- Each time the bot moves or turns, a new frame is captured
- The animation speed slider controls the delay between frames (0-2 seconds)
- Watch your bot move step-by-step through the grid
- Perfect for understanding and debugging your code!

### Bot Commands

| Command | Description |
|---------|-------------|
| `bot.move_forward()` | Move the bot forward in its current direction |
| `bot.turn_left()` | Turn the bot left (counterclockwise) |
| `bot.turn_right()` | Turn the bot right (clockwise) |
| `bot.can_move()` | Check if the bot can move forward (returns True/False) |

### Controls

1. **🚀 Run Code** - Execute all commands with animated frames
   - Adjust animation speed with the slider (0-2 seconds)
   - See each move and turn in sequence
   - Final result shown after animation completes

2. **🔄 Reset** - Reset the bot to starting position

## 📊 Game Elements

- **⬜** Empty space (walkable)
- **⬛** Basic wall (impassable)
- **🟦** Special wall (respawns bot if touched)
- **🟫** Finish line (goal!)
- **⬆️⬅️⬇️➡️** Bot with direction indicator

## 💡 Example Code

### Simple Solution
```python
# Keep moving forward, turn right when blocked
while True:
    if bot.can_move():
        bot.move_forward()
    else:
        bot.turn_right()
```

### Complex Solution
```python
# Move forward 3 times, then navigate
for i in range(3):
    if bot.can_move():
        bot.move_forward()

bot.turn_right()
while bot.can_move():
    bot.move_forward()
```

## 🎯 Winning

- Get your bot to the finish line (🟫)
- Use as few commands as possible for a ⭐ STAR rating
- Par for the default level: **3 commands**

## 🔧 Technical Details

### Architecture

- **Backend**: Flask (Python)
- **Frontend**: Vanilla JavaScript + HTML/CSS
- **Animation**: Frame-by-frame rendering with async/await

### How Animation Works

1. **Python Backend (`AnimatedBot` class)**:
   - Captures grid state after each action
   - Stores frames with position, direction, and status
   - Returns all frames to frontend

2. **JavaScript Frontend (`playAnimation` function)**:
   - Receives all frames from backend
   - Displays each frame sequentially
   - Uses setTimeout for delay between frames
   - Updates grid display in real-time

3. **User Control**:
   - Slider adjusts delay (0 = instant, 2 = slow motion)
   - Each frame shows one bot action
   - Animation is smooth and controllable

### Security

The server includes safety checks:
- Blocks dangerous imports and operations
- Input sanitization
- Code validation before execution

## 📁 File Structure

```
bot game/
├── python_decoder.py      # Original bot logic (UNCHANGED)
├── app.py                 # Flask server with AnimatedBot
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface with animation
├── static/
│   └── style.css         # Styling
└── README.md             # This file
```

## 🎨 Features

✅ Real-time frame-by-frame animation  
✅ Adjustable animation speed (0-2 seconds)  
✅ Step-by-step execution mode  
✅ Action logging  
✅ Command counting  
✅ Win/lose detection  
✅ Beautiful, responsive UI  
✅ Your original Python code stays intact!  

## 🐛 Troubleshooting

**Port already in use:**
```bash
python3 app.py  # Uses port 5000 by default
```

**Slow animation:**
- Adjust the animation speed slider to 0 for instant execution

**Bot not moving:**
- Check your code logic
- Use "Step Through" mode to debug
- Check the output panel for errors

## 🔮 Future Enhancements

- Multiple levels with different grids
- Save/load code snippets
- Leaderboard for efficient solutions
- Custom grid editor
- Share solutions via URL

Enjoy coding your bot! 🤖
