# 🚀 Quick Setup Guide

## Step 1: Get Your Groq API Key (2 minutes)

1. **Visit**: [https://console.groq.com/keys](https://console.groq.com/keys)
2. **Sign up** with your email (it's free!)
3. **Create API Key**: Click "Create API Key"
4. **Copy the key**: It starts with `gsk_...`

> ⚠️ Save this key somewhere safe! You can only see it once.

## Step 2: Add Your API Key (30 seconds)

1. **Open** the file `.env` in your `d:\sql_analyst` folder
2. **Replace** `your_groq_api_key_here` with your actual key:
   ```
   GROQ_API_KEY=gsk_your_actual_key_here
   ```
3. **Save** the file

## Step 3: Run the Agent! (10 seconds)

Open PowerShell in `d:\sql_analyst` and run:

```powershell
# Activate virtual environment
.\sql_analyst\Scripts\activate

# Run the agent
python main.py
```

That's it! 🎉

## First Questions to Try

Once the agent starts, try asking:

```
You: How many customers do we have?
You: Show me the top 5 products by stock
You: Which country has the most customers?
You: What's the total revenue from all orders?
You: List customers from USA
```

## Troubleshooting

### "GROQ_API_KEY not found"
- Did you edit the `.env` file?
- Did you save it?
- Is the key correct? (starts with `gsk_`)

### "Can't connect to MySQL"
- Is MySQL running? Check Windows Services
- Is the password correct in `config.yaml`?

### "Module not found"
- Did you activate the virtual environment?
- Try: `pip install -r requirements.txt`

## Commands While Running

- **Ask a question**: Just type and press Enter
- **`stats`**: See how many tokens you've used
- **`exit`** or **`quit`**: End the session

## What to Expect

### First Question
- Takes 3-5 seconds
- Uses ~400-600 tokens
- Caches table schemas

### Subsequent Questions
- Takes 2-4 seconds
- Uses ~150-300 tokens (cache working!)
- Much faster!

## Token Limits

**Groq Free Tier**:
- ~6,000 tokens per minute
- Plenty for testing!

**Your Agent**:
- Simple questions: 150-250 tokens
- Complex questions: 600-900 tokens
- You can ask 8-15 questions per minute easily

## Next Steps

Once you're comfortable:
1. Try more complex questions
2. Check `README.md` for advanced features
3. Explore the code in `src/` folder
4. Modify prompts in `src/llm/prompts.py` to customize

---

**Need help?**
- Check `README.md` for detailed documentation
- Review `MIGRATION_COMPLETE.md` for database info
- Look at the implementation plan documents

**Have fun exploring your data!** 🎉
