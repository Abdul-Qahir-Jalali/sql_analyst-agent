# 🚀 Quick Reference Card

## Starting the Application

### Web Interface (Recommended)
```powershell
cd d:\sql_analyst
.\sql_analyst\Scripts\activate
python app.py
```
Then visit: **http://localhost:8000**

### Command Line
```powershell
cd d:\sql_analyst
.\sql_analyst\Scripts\activate
python main.py
```

---

## Your Token Budget

**Daily Limit**: 100,000 tokens

| Type | Tokens | Daily Capacity |
|------|--------|---------------|
| Simple | 150-250 | 400-666 |
| Medium | 400-600 | 166-250 |
| Complex | 600-900 | 111-166 |

**You can ask ~200 questions per day!**

---

## Example Questions

Try asking:
- "How many customers do we have?"
- "Who are the top 5 customers by spending?"
- "Which product category has the highest sales?"
- "Show me orders from December 2025"
- "What's the average order value?"
- "List customers from USA"

---

## Database Info

**Name**: `retail_analytics`
**Tables**:
- `customers` (1,000 rows)
- `products` (200 rows)
- `orders` (10,000 rows)

**Connection**:
- Host: localhost
- User: root
- Password: (in config.yaml)

---

## Troubleshooting

**Server won't start?**
- Check `.env` has your Groq API key
- Make sure MySQL is running

**Can't connect to database?**
- Verify MySQL password in `config.yaml`
- Check MySQL service is running

**Module not found?**
- Activate virtual environment
- Run: `pip install -r requirements.txt`

---

## Files to Know

- `config.yaml` - Settings
- `.env` - API key (keep secret!)
- `app.py` - Web server
- `main.py` - CLI version
- `web/index.html` - UI design

---

## Useful Commands

**In Web Interface:**
- Type question and press Enter
- Click "Clear Chat" to start fresh
- Click "Reset Session" to clear cache

**In CLI:**
- `stats` - Show token usage
- `exit` - Quit

---

## Getting Help

**Documentation:**
- `README.md` - Complete guide
- `SETUP.md` - Quick start
- `WEB_INTERFACE_GUIDE.md` - Web UI details
- `walkthrough.md` - Full walkthrough

**Support:**
- Check error messages in terminal
- Review configuration files
- Consult documentation

---

**Made with ❤️ using FastAPI, LangGraph, Groq, and MySQL**
