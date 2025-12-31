# 🚀 SQL Analyst Agent - Web Interface Guide

## Quick Start

### Step 1: Make Sure You Have Your API Key Set

Check that your `.env` file has your Groq API key:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

### Step 2: Start the Web Server

**Option A: Using PowerShell Script (Easiest)**
```powershell
cd d:\sql_analyst
.\sql_analyst\Scripts\activate
.\start_web.ps1
```

**Option B: Direct Command**
```powershell
cd d:\sql_analyst
.\sql_analyst\Scripts\activate
python app.py
```

### Step 3: Open Your Browser

Once the sever starts, visit:
```
http://localhost:8000
```

You'll see a beautiful, colorful interface! 🎨

---

## What You'll See

### 🎨 **Vibrant Design**
- **Animated gradient background** (purple, pink, blue, cyan)
- **Bright orange header** with patterns
- **Green stats bar** showing your usage
- **Colorful chat bubbles** 
- **Smooth animations** everywhere

### 📊 **Stats Display**
Top bar shows:
- **Questions Asked**: How many questions you've asked
- **Tokens Used**: Total tokens consumed
- **Avg Tokens/Q**: Average per question
- **Remaining Today**: Out of your 100,000 daily limit

### 💬 **Chat Interface**
- **Your questions**: Purple gradient bubbles on the right
- **Agent answers**: White bubbles with blue border on the left
- **SQL queries**: Black code boxes with green text
- **Token badges**: Pink gradient showing tokens used

### 🎯 **Example Questions**
Click any example to try it instantly:
- 📊 How many customers do we have?
- 💰 Who are the top 5 customers by spending?
- 📦 Which product category has the highest sales?
- 🗓️ Show me orders from December 2025

---

## Features

### ⚡ **Real-Time Stats**
Stats update after every question showing exactly how many tokens you're using.

### 🔄 **Session Management**
- **Clear Chat**: Clears conversation history
- **Reset Session**: Resets token counters and cache (starts fresh)

### 💾 **Smart Caching**
After asking about a table once, subsequent questions about it use fewer tokens.

### 🎨 **Color Scheme**
- **Primary**: Orange/Red gradients (#ff6b6b to #ffa500)
- **Secondary**: Green gradients (#11998e to #38ef7d)
- **Accent**: Purple/Blue gradients (#667eea to #764ba2)
- **Highlights**: Pink (#f093fb) and Cyan (#4facfe)
- **NO dark blues or dull colors!** ✨

---

## Token Budget

With your **100,000 tokens/day**:

| Question Type | Tokens | Questions Possible |
|--------------|--------|-------------------|
| Simple | 150-250 | 400-666 |
| Medium | 400-600 | 166-250 |
| Complex | 600-900 | 111-166 |

**You can easily ask 200+ questions per day!**

The interface shows you exactly how many tokens you have left.

---

## Keyboard Shortcuts

- **Enter**: Send your question
- **Ctrl+C**: Stop the server (in terminal)

---

## Troubleshooting

### Server won't start

**Error: "GROQ_API_KEY not found"**
- Check your `.env` file has the correct API key

**Error: "Can't connect to MySQL"**
- Make sure MySQL is running (check Windows Services)
- Verify password in `config.yaml`

**Error: "Port 8000 already in use"**
- Close any other programs using port 8000
- Or change port in `app.py`: `uvicorn.run(app, port=8001)`

### Page won't load

- Make sure the server is running
- Check the terminal for error messages
- Try: `http://127.0.0.1:8000` instead

### Styles look broken

- Hard refresh: Ctrl+F5
- Clear browser cache

---

## Stopping the Server

Press **Ctrl+C** in the terminal where the server is running.

---

## Tips for Best Experience

1. **Ask clear questions**: "How many X?" works better than vague questions
2. **Watch your tokens**: The remaining counter shows what you have left
3. **Use examples**: Click the example buttons to see what kinds of questions work well
4. **Check SQL**: Review the generated SQL to learn query patterns
5. **Clear cache if needed**: If results seem stale, reset the session

---

## What Makes This Interface Special

### 🎨 Beautiful Design
- Modern gradient animations
- Smooth transitions
- High contrast colors
- Glassmorphic effects

### ⚡ Fast & Efficient
- Real-time updates
- Minimal token usage
- Smart caching
- Local database processing

### 📱 Responsive
- Works on desktop and tablets
- Adapts to screen size
- Touch-friendly buttons

### 🔍 Transparent
- Shows SQL queries
- Displays token usage
- Reveals what the agent is doing

---

## Next Steps

**Try it now!**
1. Start the server
2. Open http://localhost:8000
3. Click an example question
4. Watch the magic happen! ✨

**Advanced:**
- Customize colors in `web/index.html` (CSS section)
- Modify API responses in `app.py`
- Add more example questions

---

Enjoy your beautiful SQL analyst! 🚀🎨
