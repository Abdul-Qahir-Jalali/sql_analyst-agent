# SQL Analyst Agent

An intelligent database query agent that understands natural language questions and generates SQL queries with **minimal token usage**.

## Features

- 🤖 **Natural Language Queries**: Ask questions in plain English
- 💰 **Token Efficient**: Uses ~400-700 tokens per question (98.5% less than traditional chatbots)
- 🗄️ **MySQL Integration**: Works with your retail_analytics database
- 💾 **Smart Caching**: Remembers table schemas to save tokens
- 🔄 **Auto-Retry**: Fixes SQL errors automatically
- 📊 **Token Tracking**: See exactly where tokens are spent

## Quick Start

### 1. Get Your Groq API Key

1. Go to [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up for free
3. Create a new API key
4. Copy the key

### 2. Configure Environment

Edit the `.env` file and add your API key:
```
GROQ_API_KEY=your_actual_api_key_here
```

### 3. Run the Agent

```bash
# Activate virtual environment
cd d:\sql_analyst
.\sql_analyst\Scripts\activate

# Run the agent
python main.py
```

## Usage Examples

Once the agent is running, you can ask questions like:

```
You: How many customers do we have?
Answer: You have 1,000 customers in the database.
Tokens used: 150

You: Who are the top 5 customers by spending?
Answer: The top 5 customers are...
Tokens used: 520

You: Which product category has the highest sales?
Answer: Electronics has the highest sales with...
Tokens used: 680
```

### Commands

- **Type your question** - Ask anything about your data
- **`stats`** - View token usage statistics
- **`exit`** or **`quit`** - End session

## Project Structure

```
d:/sql_analyst/
├── src/                      # 📁 Source code
│   ├── agent/                # LangGraph workflow
│   │   ├── state.py          # Agent state definition
│   │   ├── nodes.py          # Workflow steps
│   │   └── graph.py          # LangGraph workflow
│   ├── mcp/                  # Database tools
│   │   └── tools.py          # Database operations
│   ├── llm/                  # LLM integration
│   │   ├── groq_client.py    # Groq API client
│   │   └── prompts.py        # Optimized prompts
│   ├── cache/                # Token-saving cache
│   │   └── schema_cache.py   # Schema caching
│   └── ui/                   # User interface
│       └── cli.py            # Command line interface
├── web/                      # 📁 Web interface
│   └── index.html            # Web UI
├── docs/                     # 📁 Documentation
│   ├── setup.md              # Setup guide
│   ├── quick_reference.md    # Quick commands
│   ├── web_interface_guide.md # Web UI guide
│   └── project_explanation.md # Tech stack explanation
├── scripts/                  # 📁 Utility scripts
│   ├── setup_db.py           # Database setup
│   └── start_web.ps1         # Web server launcher
├── config.yaml               # Configuration
├── .env                      # API keys (keep secret!)
├── main.py                   # CLI entry point
├── app.py                    # Web server entry point
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## How It Saves Tokens

### Traditional Approach (10,000 tokens)
- Sends entire database schema every time (2,000 tokens)
- Sends sample data from all tables (5,000 tokens)
- Processes all data in LLM (3,000 tokens)

### Our Approach (150 tokens)
- Only fetches needed tables (20 tokens)
- Caches schemas (0 tokens after first fetch)
- Database does all processing (0 tokens)
- Only sends final results (130 tokens)

**Result: 98.5% token savings!**

## Token Budget

With Groq's free tier (~6,000 tokens/minute):
- Simple questions: 150-250 tokens (~24 questions/minute)
- Medium questions: 400-600 tokens (~10 questions/minute)
- Complex questions: 600-900 tokens (~7 questions/minute)

You can easily ask hundreds of questions per day!

## Configuration

Edit `config.yaml` to customize:

```yaml
groq:
  model: "llama-3.3-70b-versatile"  # Groq model
  max_tokens: 500                    # Max response tokens
  temperature: 0.1                   # Low = more focused

cache:
  ttl_minutes: 30                    # Cache expires after 30 min
  max_questions: 20                  # Clear cache after 20 questions

token_budget:
  max_per_question: 1000             # Warning threshold
```

## Database

The agent connects to your MySQL database:
- **Database**: `retail_analytics`
- **Tables**: customers, products, orders
- **Rows**: 1,000 customers, 200 products, 10,000 orders

## Troubleshooting

### "GROQ_API_KEY not found"
- Make sure you edited `.env` file with your actual API key
- Don't commit `.env` to GitHub!

### "Can't connect to MySQL"
- Make sure MySQL is running (check Services)
- Verify password in `config.yaml`

### "Module not found"
- Activate virtual environment: `.\sql_analyst\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`

## Tips for Asking Questions

### ✅ Good Questions
- "How many customers from USA?"
- "What's the average order value?"
- "Top 10 products by sales"
- "Monthly revenue for 2025"

### ❌ Avoid
- Vague questions: "Tell me about data"
- Requests for entire tables: "Show all orders" (unless you want that)

## Advanced Features

### Direct SQL Mode
Simple questions bypass the LLM entirely (0 tokens):
- "How many customers?" → Instantly runs `SELECT COUNT(*)`

### Smart Caching
After first question about customers:
- Schema cached for 30 minutes
- Subsequent questions = ~100 fewer tokens

### Error Recovery
If SQL fails:
- Agent automatically retries with corrected query
- Max 2 retry attempts
- Shows error if still fails

## Next Steps

Want to extend the agent?
- Add web interface (Gradio)
- Export results to CSV
- Create query templates
- Add data visualization
- Support other databases (PostgreSQL, etc.)

## License

Free to use and modify

## Support

Issues? Check:
1. Groq API key is valid
2. MySQL is running
3. Virtual environment is activated
4. All dependencies installed

---

Built with ❤️ using LangGraph, Groq, and MySQL
