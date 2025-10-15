# Bot Game - Quick Start Guide

## Starting the Application

```bash
cd "/home/hason/bot game"
python3 app.py
```

The application will start on:
- http://localhost:5000
- http://127.0.0.1:5000

## What's New - Flask-Only Progress Tracking

The progress tracking system has been completely rewritten with a clean, Flask-only implementation:

### Key Features

✅ **Session-based storage** - No files, no database, just Flask sessions
✅ **Clean API** - Simple REST endpoints for all operations
✅ **No JavaScript dependencies** - Uses standard fetch() API
✅ **Star ratings** - 3 stars for perfect, 2 for good, 1 for completed
✅ **Progress icons** - Visual indicators in level selector

### How It Works

1. **Play a level** - Write code, run it
2. **Complete it** - Guide bot to the finish line
3. **Get stars** - Based on efficiency (commands used vs par)
4. **Track progress** - See completion icons and stats

### Star System

- ⭐ **3 stars** - Completed at or under par (perfect!)
- ✅ **2 stars** - Completed within 1.5× par (good!)
- ✔️ **1 star** - Completed (over 1.5× par)

### Icons

- ⚪ Not attempted
- 🔄 Attempted but not completed
- ⭐ Perfect score (3 stars)
- ✅ Good score (2 stars)
- ✔️ Completed (1 star)

## Playing the Game

1. **Select a level** from the dropdown
2. **Write Python code** in the code editor
3. **Run your code** to see the bot in action
4. **Optimize** to get 3 stars!

### Available Commands

```python
bot.move_forward()  # Move forward one space
bot.turn_left()     # Turn 90° counterclockwise
bot.turn_right()    # Turn 90° clockwise
bot.can_move()      # Check if forward is walkable
```

### Example Code

```python
# Simple loop to navigate
while True:
    if bot.can_move():
        bot.move_forward()
    else:
        bot.turn_right()
```

## Progress API

### Get Level Progress
```javascript
const response = await fetch('/progress/1');
const data = await response.json();
// Returns: { progress: {...}, icon: "⭐", success: true }
```

### Save Progress
```javascript
await fetch('/progress/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        level_number: 1,
        commands_used: 3,
        par: 3,
        completed: true
    })
});
```

### Get Overall Stats
```javascript
const response = await fetch('/progress/stats');
const stats = await response.json();
// Returns: { total_stars: 5, levels_completed: 2, total_levels: 8 }
```

## Documentation

- **PROGRESS_TRACKING.md** - Detailed technical documentation
- **RESET_SUMMARY.md** - What changed in the reset
- **README.md** - General project information

## Levels

1. **Tutorial: First Steps** (Easy, 5×5)
2. **The Corner** (Easy, 7×7)
3. **The Maze** (Medium, 9×9)
4. **Spiral** (Medium, 11×11)
5. **The Trap** (Medium, 7×8) - Watch out for zappy walls!
6. **Key Hunt** (Hard, 9×9) - Find and use keys
7. **Double Keys** (Hard, 9×11) - Multiple keys and gates
8. **The Challenge** (Expert, 13×13) - Ultimate test!

## Tips

- Use loops to avoid repetition
- Check `bot.can_move()` before moving
- Try to minimize commands for more stars
- Adjust animation speed with the slider
- Use Ctrl+Enter to run code quickly

## Troubleshooting

**Progress not saving?**
- Make sure cookies are enabled
- Progress is stored in Flask sessions (lost on server restart)

**Bot not moving?**
- Check for syntax errors in your code
- Make sure you're calling bot methods correctly

**Can't see animation?**
- Adjust the animation speed slider
- Check browser console for errors

## Development

**Running tests:**
```bash
# Test endpoints
curl http://localhost:5000/levels
curl http://localhost:5000/progress/1
curl http://localhost:5000/progress/stats
```

**Clean restart:**
```bash
# Stop server
pkill -f "python3 app.py"

# Clear pycache
rm -rf __pycache__

# Start fresh
python3 app.py
```

## Have Fun!

Enjoy coding and solving puzzles! 🤖⭐

