# 🤖 Bot Game

A Python programming puzzle game where you write code to guide a bot through increasingly complex mazes!

## 🎮 Game Features

- **15 Progressive Levels** - From basic movement to complex algorithms
- **Star System** - Complete levels efficiently to earn stars ⭐
- **Progress Tracking** - Save your progress and best scores
- **Multiple Bot Commands** - Forward, backward, turning, and path checking
- **Key & Gate Puzzles** - Collect keys to unlock gates
- **Zappy Walls** - Navigate dangerous obstacles that reset your bot
- **Real-time Animation** - Watch your bot execute your code step by step

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd bot-game
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your settings
   ```

4. **Run the game**
   ```bash
   python app.py
   ```

5. **Open your browser**
   ```
   http://localhost:5000
   ```

## 🌐 Deploy to Railway

### One-Click Deployment

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/deploy)

### Manual Deployment

1. **Fork this repository** on GitHub
2. **Connect to Railway**:
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your forked repository

3. **Set environment variables** (optional):
   - `SECRET_KEY`: Generate with `python generate_secret.py`
   - `FLASK_ENV`: Set to `production`

4. **Deploy!** Railway will automatically build and deploy your game.

## 🎯 How to Play

### Bot Commands

- `bot.move_forward()` - Move forward in current direction
- `bot.move_backward()` - Move backward from current direction  
- `bot.turn_left()` - Turn left (counterclockwise)
- `bot.turn_right()` - Turn right (clockwise)
- `bot.can_move()` - Check if can move forward
- `bot.can_move_back()` - Check if can move backward

### Game Elements

- **🤖 Bot** - Your character (shows direction with arrows)
- **⬜ Empty** - Walkable space
- **⬛ Wall** - Impassable barrier
- **🟧 Zappy Wall** - Dangerous! Resets bot to start
- **🟫 Finish Line** - Your goal
- **🟡 Keys & Gates** - Collect keys to unlock gates
- **🔴 Red, 🔵 Blue, 🟢 Green, 🟣 Purple** - Different key types

### Scoring

- **⭐ Star**: Complete at or under par (optimal solution)
- **✅ Checkmark**: Complete above par (still counts as completed)
- **Stars can replace checkmarks, but not vice versa**

## 🏗️ Technical Details

### Architecture

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Game Engine**: Custom Python bot simulation
- **Progress**: Browser session storage

### File Structure

```
bot-game/
├── app.py              # Main Flask application
├── grids.py            # Game level definitions
├── python_decoder.py   # Bot game engine
├── templates/
│   └── index.html      # Game interface
├── static/
│   └── style.css       # Styling
├── requirements.txt    # Python dependencies
├── Procfile           # Railway deployment
└── README.md          # This file
```

### Security Features

- ✅ Environment-based configuration
- ✅ Secure session cookies
- ✅ CORS protection
- ✅ Code execution sandboxing
- ✅ Input validation

## 🎨 Customization

### Adding New Levels

1. **Edit `grids.py`**:
   ```python
   LEVEL_X = {
       'name': 'Level Name',
       'description': 'Description',
       'data': [...],  # 2D array of tile types
       'start_pos': (row, col),
       'start_dir': 0,  # 0=up, 1=left, 2=down, 3=right
       'par': 10,       # Target command count
       'difficulty': 'Medium'
   }
   ```

2. **Add to `ALL_LEVELS`** list
3. **Update level counter** in frontend

### Tile Types

- `0`: Empty space
- `1`: Wall
- `2`: Zappy wall
- `3`: Finish line
- `4`: Yellow key → `5`: Yellow gate
- `6`: Red key → `7`: Red gate
- `8`: Blue key → `9`: Blue gate
- `10`: Green key → `11`: Green gate
- `12`: Purple key → `13`: Purple gate

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🎮 Play Now

Ready to start coding? Deploy to Railway and begin your bot programming adventure!

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/deploy)

---

**Made with ❤️ for programming education**