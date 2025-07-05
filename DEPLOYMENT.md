# 🚀 Deployment Guide for Render.com

This guide will help you deploy the Stream Suggestor application to Render.com.

## 📋 Prerequisites

1. **GitHub Repository**: Your code should be pushed to GitHub (✅ Done!)
2. **Render.com Account**: Sign up at [render.com](https://render.com)
3. **Google Gemini API Key**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🎯 Step-by-Step Deployment

### Step 1: Connect to Render.com

1. **Sign in to Render.com**
2. **Click "New +"** in the dashboard
3. **Select "Web Service"**

### Step 2: Connect Your Repository

1. **Connect your GitHub account** (if not already connected)
2. **Select the repository**: `NeelBorad00/stream-suggestor`
3. **Choose the branch**: `master`

### Step 3: Configure the Web Service

Fill in the following details:

#### Basic Settings
- **Name**: `stream-suggestor` (or your preferred name)
- **Region**: Choose the closest to your users
- **Branch**: `master`
- **Root Directory**: Leave empty (root of repository)

#### Build & Deploy Settings
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

#### Environment Variables
Add these environment variables:

| Key | Value | Description |
|-----|-------|-------------|
| `GEMINI_API_KEY` | `your_actual_api_key_here` | Your Google Gemini API key |
| `FLASK_ENV` | `production` | Set Flask to production mode |

### Step 4: Deploy

1. **Click "Create Web Service"**
2. **Wait for the build to complete** (usually 2-5 minutes)
3. **Your app will be live** at the provided URL

## 🔧 Configuration Details

### Build Command
```bash
pip install -r requirements.txt
```

### Start Command
```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

### Environment Variables Required
- `GEMINI_API_KEY`: Your Google Gemini API key
- `FLASK_ENV`: Set to `production`

## 📊 Monitoring & Logs

### View Logs
1. Go to your web service dashboard
2. Click on "Logs" tab
3. Monitor for any errors or issues

### Health Checks
- Render automatically checks if your app is responding
- The app should return a 200 status code on the root path

## 🔒 Security Considerations

### API Key Security
- ✅ API key is stored as environment variable
- ✅ Never commit API keys to Git
- ✅ Use Render's secure environment variable storage

### Rate Limiting
- The app includes rate limiting (15 RPM, 1500 RPD)
- This prevents abuse and keeps costs under control

## 🚨 Troubleshooting

### Common Issues

#### 1. Build Fails
**Error**: `ModuleNotFoundError: No module named 'google'`
**Solution**: Ensure `google-generativeai` is in `requirements.txt`

#### 2. App Won't Start
**Error**: `GEMINI_API_KEY environment variable is required`
**Solution**: Add the environment variable in Render dashboard

#### 3. 500 Internal Server Error
**Check**: 
- API key is valid
- Database permissions
- Logs for specific error messages

#### 4. App Times Out
**Solution**: 
- Check if the app is responding on the root path
- Verify the start command is correct
- Check logs for startup errors

### Debugging Steps

1. **Check Build Logs**: Look for any errors during the build process
2. **Check Runtime Logs**: Monitor the application logs for runtime errors
3. **Test Locally**: Ensure the app works locally with the same environment variables
4. **Verify API Key**: Test your Gemini API key separately

## 📈 Scaling (Optional)

### Auto-Scaling
- Render can automatically scale your app based on traffic
- Configure in the "Settings" tab of your web service

### Custom Domain
1. Go to your web service settings
2. Click "Custom Domains"
3. Add your domain and configure DNS

## 🔄 Updates & Maintenance

### Updating Your App
1. **Make changes** to your code
2. **Commit and push** to GitHub
3. **Render automatically deploys** the new version

### Environment Variable Updates
1. Go to your web service dashboard
2. Click "Environment" tab
3. Update variables as needed
4. **Redeploy** the service

## 📞 Support

### Render Support
- [Render Documentation](https://render.com/docs)
- [Render Community](https://community.render.com)

### Application Support
- Check the logs for specific error messages
- Verify all environment variables are set correctly
- Ensure your API key is valid and has sufficient quota

## 🎉 Success!

Once deployed, your Stream Suggestor app will be available at:
`https://your-app-name.onrender.com`

### Test Your Deployment
1. **Visit the landing page**: Should show "Stream Suggestor - Go Beyond the Flow"
2. **Test the form**: Fill out the career questionnaire
3. **Check AI responses**: Verify career recommendations are generated
4. **Test mobile responsiveness**: Try on different devices

---

**🎯 Your AI-powered career counseling app is now live and ready to help students worldwide!** 