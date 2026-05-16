# 📰 Playwright MCP News Agent

An AI-powered news-reading agent built using the **Agent Framework**, **OpenAIChatClient**, and **Playwright MCP**.

The agent browses websites like a human, opens articles, reads content, and generates clean summaries automatically.

---

# 🚀 Features

- 🌐 Navigates websites automatically
- 📰 Reads BBC News Sport headlines
- 📖 Opens and analyses articles
- ✨ Generates concise summaries
- 📊 Identifies overall news trends
- 🤖 Uses Playwright MCP browser automation

---

# 🏗️ Architecture

```text
User Prompt
      ↓
OpenAIChatClient
      ↓
Agent Framework
      ↓
MCPStdioTool
      ↓
Playwright MCP Server
      ↓
News Website Interaction
      ↓
Summarised Output
```

---

# 📂 Project Structure

```text
playwright-mcp-news-agent/
│
├── main.py
├── .env
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Create Virtual Environment

### Mac/Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 📦 requirements.txt

```text
agent-framework
python-dotenv
openai
```

---

# 🔐 Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

# ▶️ Run the Application

```bash
python main.py
```

---

# 💬 Example Task

```text
1. Go to BBC News
2. Navigate to Sport section
3. Read top 3 headlines
4. Summarise each article
5. Identify an overall trend
```

---

# 🛠️ Technologies Used

- Python
- Agent Framework
- OpenAIChatClient
- MCPStdioTool
- Playwright MCP
- AsyncIO

---

# 🔮 Future Improvements

- 🌐 Multi-site news support
- 📊 Sentiment analysis
- 🧠 Memory-enabled news agent
- 📧 Daily email summaries
- 🗣️ Voice interaction

---

# 👨‍💻 Built With

Built using **Agent Framework + Playwright MCP + OpenAI**