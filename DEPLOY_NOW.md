# Quick Deployment Checklist

## ✅ Step 1: Push to GitHub

### 1.1 Initialize Git Repository
```bash
cd d:\sql_analyst
git init
```

### 1.2 Add All Files
```bash
git add .
```

### 1.3 Commit
```bash
git commit -m "SQL Analyst with SQLite - ready to deploy"
```

### 1.4 Create Repository on GitHub
1. Go to: https://github.com/new
2. Repository name: `sql-analyst` (or any name you like)
3. Keep it Public or Private (your choice)
4. **Don't** initialize with README
5. Click "Create repository"

### 1.5 Push to GitHub
```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/sql-analyst.git
git branch -M main
git push -u origin main
```

---

## ✅ Step 2: Deploy to Vercel

### 2.1 Sign Up
1. Go to: https://vercel.com
2. Click "Sign Up"
3. Choose "Continue with GitHub" (easiest)
4. Authorize Vercel to access your GitHub

### 2.2 Import Project
1. Click "Add New Project"
2. Select your `sql-analyst` repository
3. Click "Import"

### 2.3 Configure Project
**Framework Preset**: Other (leave as default)

**Environment Variables** - Click "Add" and enter:
```
Name: GROQ_API_KEY
Value: (paste your actual Groq API key)
```

### 2.4 Deploy
1. Click "Deploy"
2. Wait 2-3 minutes ☕
3. You'll see "Congratulations!"

### 2.5 Test Your Live App
1. Click on your Vercel URL
2. Try asking: "How many customers do we have?"
3. Click "View Database" button
4. Success! 🎉

---

## 🆘 Quick Troubleshooting

**Git not found?**
```bash
# Install Git from: https://git-scm.com/download/win
```

**GitHub credentials?**
- Use GitHub Desktop for easier push
- Or set up SSH key: https://docs.github.com/en/authentication

**Vercel build fails?**
- Check that `retail_analytics.db` is in your repo
- Verify GROQ_API_KEY is set correctly
- Check Vercel logs for specific error

---

## 📝 Commands Summary

```bash
# All commands in order:
cd d:\sql_analyst
git init
git add .
git commit -m "SQL Analyst with SQLite"
git remote add origin https://github.com/YOUR_USERNAME/sql-analyst.git
git branch -M main
git push -u origin main
```

Then go to Vercel.com and import!
