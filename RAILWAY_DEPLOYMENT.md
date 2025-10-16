# Railway Deployment Guide for Bot Game

This guide will help you deploy your Flask Bot Game to Railway, a modern cloud platform that makes deployment simple.

## Prerequisites

1. **GitHub Repository**: Your code should be in a GitHub repository
2. **Railway Account**: Sign up at [railway.app](https://railway.app)
3. **Git**: Make sure you have Git installed locally

## Step 1: Prepare Your Repository

### Files Already Created:
- ✅ `Procfile` - Tells Railway how to start your app
- ✅ `railway.json` - Railway configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `app.py` - Updated for Railway deployment

### Repository Structure:
```
bot-game/
├── app.py              # Main Flask application
├── grids.py            # Game levels
├── python_decoder.py   # Game engine
├── templates/
│   └── index.html      # Frontend
├── static/
│   └── style.css       # Styling
├── requirements.txt    # Python dependencies
├── Procfile           # Railway startup command
├── railway.json       # Railway configuration
└── README.md          # Documentation
```

## Step 2: Deploy to Railway

### Method 1: GitHub Integration (Recommended)

1. **Go to Railway Dashboard**
   - Visit [railway.app](https://railway.app)
   - Sign in with your GitHub account

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your bot-game repository

3. **Configure Deployment**
   - Railway will auto-detect it's a Python app
   - It will use the `Procfile` to start your app
   - No additional configuration needed!

4. **Set Environment Variables (Optional)**
   - Go to your project settings
   - Add environment variables:
     - `SECRET_KEY`: Generate a secure random string
     - `FLASK_ENV`: Set to `production` (or leave empty)

### Method 2: Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Deploy Your App**
   ```bash
   cd /path/to/your/bot-game
   railway init
   railway up
   ```

## Step 3: Access Your Deployed Game

1. **Get Your URL**
   - Railway will provide a URL like: `https://your-app-name.railway.app`
   - You can also set a custom domain in Railway settings

2. **Test Your Game**
   - Visit the URL in your browser
   - Test all features: levels, progress tracking, etc.

## Step 4: Custom Domain (Optional)

1. **In Railway Dashboard**
   - Go to your project settings
   - Click "Domains"
   - Add your custom domain
   - Follow DNS setup instructions

## Environment Variables

### Required:
- `PORT`: Automatically set by Railway (don't change)

### Optional:
- `SECRET_KEY`: For session security (generate a random string)
- `FLASK_ENV`: Set to `production` for production deployment

### Generate a Secret Key:
```python
import secrets
print(secrets.token_hex(32))
```

## Railway Pricing

### Free Tier:
- ✅ **$5 credit monthly** (usually enough for small apps)
- ✅ **Unlimited deployments**
- ✅ **Custom domains**
- ✅ **Automatic HTTPS**

### Paid Plans:
- Start at $5/month for more resources
- Only pay for what you use

## Troubleshooting

### Common Issues:

1. **App Won't Start**
   - Check Railway logs in the dashboard
   - Ensure `requirements.txt` includes all dependencies
   - Verify `Procfile` is correct

2. **Static Files Not Loading**
   - Ensure `static/` folder is in your repository
   - Check file paths in your HTML

3. **Environment Variables Not Working**
   - Set them in Railway dashboard under "Variables"
   - Redeploy after adding variables

4. **Database/Session Issues**
   - Railway provides persistent storage
   - Sessions should work out of the box

### View Logs:
```bash
railway logs
```

## Auto-Deployments

Railway automatically deploys when you push to your main branch:
1. Push code to GitHub
2. Railway detects changes
3. Automatically rebuilds and deploys
4. Your game updates live!

## Monitoring

Railway provides:
- **Real-time logs**
- **Performance metrics**
- **Uptime monitoring**
- **Error tracking**

## Next Steps

1. **Deploy your app** following the steps above
2. **Test thoroughly** on the live URL
3. **Share your game** with others!
4. **Monitor usage** in Railway dashboard

## Support

- **Railway Documentation**: [docs.railway.app](https://docs.railway.app)
- **Railway Discord**: Community support
- **GitHub Issues**: For code-related problems

## Example URLs

Your deployed game will be available at:
- `https://your-app-name.railway.app`
- Or your custom domain if configured

## Security Notes

- ✅ HTTPS enabled by default
- ✅ Environment variables for secrets
- ✅ Session security configured
- ✅ CORS properly configured

Happy deploying! 🚀
