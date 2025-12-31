# 🚀 Deployment Guide: PlanetScale + Vercel

Complete step-by-step guide to deploy your SQL Analyst app to the cloud.

---

## 📋 Prerequisites

- GitHub account
- PlanetScale account (free)
- Vercel account (free)
- Your local project working

---

## Step 1️⃣: Export Your Local Database

1. **Open your terminal** in the project directory:
   ```bash
   cd d:\sql_analyst
   ```

2. **Activate virtual environment**:
   ```bash
   .\sql_analyst\Scripts\activate
   ```

3. **Run the export script**:
   ```bash
   python export_database.py
   ```

4. **You should see**:
   - A new file: `retail_analytics_export_YYYYMMDD_HHMMSS.sql`
   - This contains all your tables and data

---

## Step 2️⃣: Set Up PlanetScale

### A. Create Account and Database

1. **Go to**: https://planetscale.com
2. **Sign up** with GitHub (easiest)
3. **Click "Create database"**
4. **Fill in**:
   - Database name: `retail-analytics` (or any name you prefer)
   - Region: Choose closest to you (e.g., AWS us-east-1)
   - Click "Create database"

### B. Get Connection Details

1. **Click "Connect"** on your database dashboard
2. **Select**: "Connect with: MySQL CLI"
3. **Copy the connection details** - you'll see something like:
   ```
   Host: xxxx.connect.psdb.cloud
   Username: xxxxxxxxxxxx
   Password: pscale_pw_xxxxxxxxxxxx
   ```
4. **Save these** - you'll need them later!

### C. Import Your Data

**Option A: Using PlanetScale CLI (Recommended)**

1. **Install PlanetScale CLI**:
   ```bash
   # Windows (using Scoop)
   scoop bucket add pscale https://github.com/planetscale/scoop-bucket.git
   scoop install pscale mysql
   
   # Or download from: https://github.com/planetscale/cli#installation
   ```

2. **Login**:
   ```bash
   pscale auth login
   ```

3. **Import your SQL file**:
   ```bash
   pscale database restore retail-analytics main retail_analytics_export_YYYYMMDD_HHMMSS.sql
   ```

**Option B: Using MySQL Workbench**

1. **Open MySQL Workbench**
2. **Create new connection**:
   - Connection Name: PlanetScale
   - Hostname: (from PlanetScale dashboard)
   - Username: (from PlanetScale dashboard)
   - Password: (from PlanetScale dashboard)
   - Enable SSL
3. **Connect** and **run your SQL file** (File → Run SQL Script)

---

## Step 3️⃣: Update Your Code for Production

Your code is already set up to use environment variables, so you just need to update `.env`:

1. **Create `.env.example`** (for GitHub):
   ```bash
   GROQ_API_KEY=your_groq_api_key_here
   DB_HOST=your_planetscale_host
   DB_USER=your_planetscale_username
   DB_PASSWORD=your_planetscale_password
   DB_NAME=retail-analytics
   DB_PORT=3306
   ```

2. **Update your `.env`** with PlanetScale credentials (for local testing)

3. **Test locally** with PlanetScale:
   ```bash
   python app.py
   ```
   - Open http://localhost:8000
   - Click "View Database" to verify connection

---

## Step 4️⃣: Push to GitHub

1. **Initialize git** (if not already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - SQL Analyst with PlanetScale"
   ```

2. **Create repository on GitHub**:
   - Go to: https://github.com/new
   - Name: `sql-analyst` (or your choice)
   - Keep it public or private
   - Don't initialize with README
   - Click "Create repository"

3. **Push your code**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/sql-analyst.git
   git branch -M main
   git push -u origin main
   ```

**⚠️ IMPORTANT**: Make sure `.env` is in your `.gitignore` file!

---

## Step 5️⃣: Deploy to Vercel

1. **Go to**: https://vercel.com
2. **Sign up** with GitHub
3. **Click "Add New Project"**
4. **Import** your `sql-analyst` repository
5. **Configure**:
   - Framework Preset: Other
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: (leave empty)
   - Install Command: (leave default)

6. **Add Environment Variables** (click on "Environment Variables"):
   ```
   GROQ_API_KEY = your_actual_groq_api_key
   DB_HOST = your_planetscale_host.connect.psdb.cloud
   DB_USER = your_planetscale_username
   DB_PASSWORD = your_planetscale_password
   DB_NAME = retail-analytics
   DB_PORT = 3306
   ```

7. **Click "Deploy"**

8. **Wait 2-3 minutes** for deployment

9. **Visit your app**:
   - Vercel will give you a URL like: `https://sql-analyst-xxx.vercel.app`
   - Test the "View Database" feature!

---

## Step 6️⃣: Update App Configuration

You might need to update `app.py` to read environment variables properly for production:

1. **Update database config** to use environment variables:
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   
   config['database'] = {
       'host': os.getenv('DB_HOST', 'localhost'),
       'user': os.getenv('DB_USER', 'root'),
       'password': os.getenv('DB_PASSWORD'),
       'database': os.getenv('DB_NAME', 'retail_analytics'),
       'port': int(os.getenv('DB_PORT', 3306))
   }
   ```

---

## 🎯 Troubleshooting

### Connection Issues
- ✅ Verify PlanetScale credentials are correct
- ✅ Make sure SSL is enabled (PlanetScale requires it)
- ✅ Check that your IP isn't blocked (PlanetScale free tier allows all IPs)

### Vercel Deployment Fails
- ✅ Check build logs in Vercel dashboard
- ✅ Ensure `requirements.txt` has all dependencies
- ✅ Verify environment variables are set correctly

### Database Not Loading
- ✅ Test connection locally with PlanetScale credentials
- ✅ Check Vercel logs for error messages
- ✅ Verify table names match between local and cloud

---

## 📝 Important Notes

1. **Free Tier Limits**:
   - PlanetScale: 5GB storage, 1 billion row reads/month
   - Vercel: 100GB bandwidth, unlimited hobby projects

2. **SSL/TLS**:
   - PlanetScale requires SSL connections
   - Add this to your MySQL connection if needed:
     ```python
     ssl={'ssl_disabled': False}
     ```

3. **Keep `.env` Secret**:
   - Never commit `.env` to GitHub
   - Always use environment variables in Vercel

---

## 🎉 Success!

Once deployed, you'll have:
- ✅ Cloud-hosted database (PlanetScale)
- ✅ Live web app (Vercel)
- ✅ Free hosting forever (within limits)
- ✅ HTTPS and custom domain support

Share your deployed URL and enjoy your SQL Analyst app! 🚀
