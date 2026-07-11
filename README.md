# Genesis Agent 🤖

A fully functional AI agent built from scratch in Python — no LangChain, no frameworks.
The project demonstrates how an AI agent can combine web search, webpage browsing, iterative reasoning, and self-evaluation using a simple Python architecture.

---

## What it does

Genesis Agent takes a goal/prompt from the user and works to complete it by:

- Deciding if web search is needed
- Searching the web using DDGS
- Browsing the top 3 URLs for deeper context
- Generating an answer using an LLM
- Judging its own answer (LLM as judge)
- Looping with feedback until the goal is completed

---

## How it works

```
User enters a goal/prompt
        ↓
needs_search()? → keyword check + LLM decision
        ↓
gather_context() → search + browse top 3 URLs
        ↓
LLM generates answer
        ↓
llm_judge() → done? ✅ or feedback? 🔄
        ↓
Loop until goal completed (max 5 iterations)
        ↓
Final answer printed
```

---

## Tech Stack

| Tool | Purpose | Cost |
|------|---------|------|
| [Groq](https://console.groq.com) | LLM API (LLaMA 3.3 70B) | Free |
| [DDGS](https://pypi.org/project/ddgs/) | Web search | Free |
| [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) | Web page parsing | Free |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | API key management | Free |

**Total cost: $0**

---

## Project Structure

```
genesis-agent/
├── .env.sample         ← API key template
├── .gitignore
├── requirements.txt
├── README.md
└── src/
    ├── utils/
    │   ├── __init__.py
    │   └── ai.py           ← LLM wrapper
    ├── tools/
    │   ├── __init__.py
    │   ├── search.py       ← DDGS web search
    │   ├── browse.py       ← URL reader
    │   └── judge.py        ← LLM as judge
    └── core/
        ├── 01_llm.py       ← Step 1: basic LLM call
        ├── 02_condition.py ← Step 2: LLM as judge pattern
        ├── 03_tools.py     ← Step 3: tools in action
        ├── 04_refactor.py  ← Step 4: clean architecture
        └── agent.py        ← Step 5: full agent loop
```

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/recxcoder/genesis-agent.git
cd genesis-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a free Groq API key
- Go to [console.groq.com](https://console.groq.com)
- Sign up for free
- Create an API key

### 4. Create your `.env` file
```bash
cp .env.sample .env
```
Then open `.env` and add your key:
```
GROQ_API_KEY=your_actual_key_here
```

---

## Run

```bash
python src/core/agent.py
```

You will be prompted to enter your goal:
```
Enter prompt: What are the latest AI breakthroughs in 2026?
```

---

## Example Usage

**Simple knowledge query:**
```
Enter prompt: Explain how a CPU works in simple terms

No search needed - using LLM knowledge directly
🔄 Iteration 1/5
😊 GOAL COMPLETED!
```

**Time-sensitive query:**
```
Enter prompt: What are the latest AI breakthroughs this month?

⚡ Time-sensitive query detected - forcing web search
🔍 Search needed - gathering context...
🌐 Browsing top 3 URLs...
🔄 Iteration 1/5
😊 GOAL COMPLETED!
```

---

## How it was built

This project was built incrementally — one step at a time with a Git commit at each milestone:

| Step | File | What it does |
|------|------|-------------|
| 0 | `core/01_llm.py` | Basic LLM call |
| 1 | `core/02_condition.py` | LLM as judge |
| 2 | `utils/ai.py` | LLM wrapper function |
| 3 | `tools/search.py` | DDGS web search |
| 4 | `tools/browse.py` | Fetch and parse web pages |
| 5 | `tools/judge.py` | Reusable LLM judge with feedback |
| 6 | `core/03_tools.py` | All tools working together |
| 7 | `core/04_refactor.py` | Clean architecture |
| 8 | `core/agent.py` | Full agent loop |

---

## Key learnings

- An agent is just: **LLM + tools + a while loop**
- The LLM judges its own output to decide when to stop
- Web search solves the knowledge cutoff problem
- Clean function structure makes the agent loop readable
- You don't need LangChain to build a real agent

---

## Reference

- Inspired by: [mfdtrade/agent-talk-2025](https://github.com/mfdtrade/agent-talk-2025)
- LLM provider: [Groq](https://groq.com)
- Model: LLaMA 3.3 70B Versatile
