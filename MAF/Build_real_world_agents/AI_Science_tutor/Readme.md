# 🧬 AI Science Tutor Agent — Professor Spark ⚡

An interactive AI-powered science tutor built using the **Agent Framework** and **OpenAIChatClient**.

Professor Spark creates fun, engaging, and memory-aware science conversations using session-based short-term memory.

---

# 🚀 Features

- ⚡ Conversational AI science tutor
- 🧠 Short-term memory using sessions
- 🧪 Suggests science experiments
- 📝 Generates quizzes and grades answers
- 🎯 Explains concepts using analogies
- 🗺️ Provides learning roadmaps

---

# 🏗️ Architecture

```text
Student Input
      ↓
OpenAIChatClient
      ↓
Professor Spark Agent
      ↓
Session Memory
      ↓
Educational Response
```

---

# 📂 Project Structure

```text
ai-science-tutor/
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

# 💬 Example Prompts

```text
Why is the sky blue?

Explain DNA like I'm 10

Quiz me on the solar system

Suggest an experiment about electricity
```

---

# 🧠 Memory Example

Professor Spark remembers previous quiz questions and conversation context automatically using:

```python
session = tutor.create_session()
```

---

# 🛠️ Technologies Used

- Python
- Agent Framework
- OpenAIChatClient
- AsyncIO
- dotenv

---

# 🔮 Future Improvements

- 🌐 Web UI
- 🎤 Voice support
- 🧠 Long-term memory
- 📊 Student progress tracking

---

# 👨‍🔬 Built With

Built using **Agent Framework + OpenAI**