# 🚀 Quick Start: Deployment Steps

Follow these steps **in order** to deploy your SQL Analyst app to the cloud.

---

## ✅ Step-by-Step Checklist

### 1️⃣ Export Your Database (5 minutes)

```bash
# Make sure you're in the project directory
cd d:\sql_analyst

# Activate virtual environment
.\sql_analyst\Scripts\activate

# Run export script
python export_database.py
```

**✓ You should see**: A new `.sql` file created with all your data

---

### 2️⃣ Create PlanetScale Account (5 minutes)

1. Go to: https://planetscale.com
2. Click **"Sign up"** (use GitHub for easy login)
3. Click **"Create database"**
4. Name it: `retail-analytics`
5. Choose region: **US East** (or closest to you)
6. Click **"Create database"**

**✓ You should see**: Your database dashboard

---

### 3️⃣ Get PlanetScale Connection Info (2 minutes)

1. On your database dashboard, click **"Connect"**
2. Select: **"General"** or **"MySQL CLI"**
3. **Copy and save**:
   - Host
   - Username  
   - Password

**✓ You should have**: 3 pieces of info copied somewhere safe

---

### 4️⃣ Import Your Data to PlanetScale (10 minutes)

**Option A: Use PlanetScale Web Console (Easier)**

1. In PlanetScale dashboard, click **"Console"** tab
2. Click **"main"** branch
3. Open your exported `.sql` file in a text editor
4. **Copy the entire content**
5. **Paste into the console** and click **"Execute"**

**Option B: Use MySQL Workbench**

1. Open MySQL Workbench
2. Create new connection with PlanetScale credentials
3. File → Run SQL Script → Select your `.sql` file

**✓ You should see**: Tables `customers`, `orders`, `products` in PlanetScale

---

### 5️⃣ Test PlanetScale Connection Locally (5 minutes)

1. Open your `.env` file
2. Update with PlanetScale credentials:
   ```
   GROQ_API_KEY=your_existing_key
   DB_HOST=xxxx.connect.psdb.cloud
   DB_USER=xxxxxxxxxxxx
   DB_PASSWORD=pscale_pw_xxxxxxxxxxxx
   DB_NAME=retail-analytics
   DB_PORT=3306
   ```

3. Restart your app:
   ```bash
   python app.py
   ```

4. Open: http://localhost:8000
5. Click **"View Database"** button
6. Verify you see your data!

**✓ You should see**: Your tables and data loading from PlanetScale

---

### 6️⃣ Push to GitHub (5 minutes)

```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Add SQL Analyst with PlanetScale support"

# Create repository on GitHub (https://github.com/new)
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/sql-analyst.git
git branch -M main
git push -u origin main
```

**✓ You should see**: Your code on GitHub (without `.env` file!)

---

### 7️⃣ Deploy to Vercel (10 minutes)

1. Go to: https://vercel.com
2. **Sign up** with GitHub
3. Click **"Add New Project"**
4. **Import** your `sql-analyst` repository
5. In **"Environment Variables"**, add:
   ```
   GROQ_API_KEY = (your Groq key)
   DB_HOST = (your PlanetScale host)
   DB_USER = (your PlanetScale username)
   DB_PASSWORD = (your PlanetScale password)
   DB_NAME = retail-analytics
   DB_PORT = 3306
   ```
6. Click **"Deploy"**
7. **Wait 2-3 minutes**

**✓ You should see**: "Congratulations" with your live URL!

---

### 8️⃣ Test Your Live App (2 minutes)

1. Click on your Vercel URL (e.g., `https://sql-analyst-xxx.vercel.app`)
2. Click **"View Database"** button
3. Select a table
4. Verify data loads correctly

**✓ You should see**: Your SQL Analyst app working live! 🎉

---

## 🆘 Common Issues

| Problem | Solution |
|---------|----------|
| Can't connect to PlanetScale | Double-check host, username, password |
| `.env` file pushed to GitHub | Add to `.gitignore` and delete from repo |
| Vercel build fails | Check environment variables are set |
| Database empty in PlanetScale | Re-run import with `.sql` file |

---

## 📞 Need Help?

- PlanetScale Docs: https://planetscale.com/docs
- Vercel Docs: https://vercel.com/docs
- Check `DEPLOYMENT.md` for detailed explanations

---

**Total Time**: ~45 minutes to complete deployment! 🚀
