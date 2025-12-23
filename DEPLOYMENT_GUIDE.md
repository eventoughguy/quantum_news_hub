# Quantum News Hub Deployment Guide

## Step 1: Push to GitHub

Since authentication is required, please run these commands in your terminal:

```bash
# Navigate to the project directory
cd /home/liuyiwen/AI/AI\ Agent/quantum_news_agent

# Push to your GitHub repository
git push -u origin main
```

If you get authentication errors, you may need to:
1. Set up a GitHub personal access token
2. Use SSH instead of HTTPS
3. Configure your Git credentials

## Step 2: Deploy to Render (Recommended)

Render is a great free hosting platform for web apps.

1. **Sign up for Render**: Go to [render.com](https://render.com) and sign up
2. **Connect GitHub**: Link your GitHub account to Render
3. **Create New Web Service**:
   - Click "New" → "Web Service"
   - Select your `quantum_news_hub` repository
   - Configure the service:
     - **Name**: quantum-news-hub (or your preferred name)
     - **Environment**: Python
     - **Build Command**: `cd project && pip install -r requirements.txt`
     - **Start Command**: `cd project/news_agent && gunicorn --bind 0.0.0.0:$PORT enhanced_app:app`
     - **Instance Type**: Free tier
4. **Set Environment Variables**:
   - Go to Environment tab
   - Add `GOOGLE_API_KEY` with your actual Google API key
5. **Deploy**: Click "Create Web Service"

## Step 3: Alternative - Deploy to Railway

Railway is another excellent free hosting platform:

1. **Sign up for Railway**: Go to [railway.app](https://railway.app)
2. **Connect GitHub**: Link your GitHub account
3. **Deploy from GitHub**:
   - Click "Deploy from GitHub repo"
   - Select your `quantum_news_hub` repository
4. **Set Environment Variables**:
   - Go to Variables tab
   - Add `GOOGLE_API_KEY` with your actual Google API key
5. **Configure Start Command** (if needed):
   - Railway should auto-detect, but if not, set: `cd project/news_agent && gunicorn --bind 0.0.0.0:$PORT enhanced_app:app`

## Step 4: Alternative - Deploy to Heroku

Heroku also offers free tiers:

1. **Install Heroku CLI**: Download from [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)
2. **Login to Heroku**: `heroku login`
3. **Create Heroku App**: `heroku create your-quantum-news-hub`
4. **Set Environment Variables**: `heroku config:set GOOGLE_API_KEY=your_actual_api_key`
5. **Deploy**:
   ```bash
   git push heroku main
   ```

## Files Created for Deployment

✅ **Procfile**: Tells Heroku how to run your app
✅ **requirements.txt**: Updated with all dependencies including gunicorn
✅ **runtime.txt**: Specifies Python version
✅ **Dockerfile**: For container-based deployments
✅ **render.yaml**: Configuration for Render platform
✅ **README.md**: Documentation for your project
✅ **.gitignore**: Prevents sensitive files from being committed
✅ **.env**: Template for environment variables (add your real API key)

## Important Security Notes

🔒 **Never commit your actual API key to GitHub**
🔒 **Always use environment variables in production**
🔒 **The .env file in the repo has a placeholder - replace it on your deployment platform**

## Your App Features

Once deployed, your Quantum News Hub will have:
- 🚀 Real-time quantum computing news aggregation
- 🤖 AI-powered article summaries using Google Gemini
- 🔗 Interactive quantum supply chain ontology visualization
- 📱 Responsive web interface
- 📊 News statistics and health monitoring
- 🔄 Automatic RSS feed processing

## Post-Deployment

After deployment:
1. Visit your app URL to verify it's working
2. Check the logs if there are any issues
3. The app will create a SQLite database automatically
4. RSS feeds will be processed and articles summarized
5. The ontology visualization will be available at your app URL

## Need Help?

- Check the platform-specific logs for any deployment issues
- Ensure your Google API key is correctly set as an environment variable
- Verify all dependencies are installing correctly
- Contact support for your chosen platform if needed

Your Quantum News Hub is now ready for the world! 🌟