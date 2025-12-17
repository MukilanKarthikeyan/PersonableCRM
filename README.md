# PersonableCRM
A personal CRM tool to build and  manage your network. never forget to reach out and find the msot relevant poeple


┌─────────────────────────────┐
│           Frontend          │
│  (Next.js: Research UI)     │
└──────────────┬──────────────┘
               │ REST
┌──────────────▼──────────────┐
│          FastAPI            │
│  - Agent Orchestrator       │
│  - CRM API                  │
│  - Lux Client               │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│           Lux API           │
│  - Web Search               │
│  - Scraping                 │
│  - Extraction               │
│  - Reasoning                │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│        SQLite DB            │
│  Contacts / Sources / Logs  │
└─────────────────────────────┘


Below is a **clean, copy-pasteable, Windows 11–specific setup guide** that assumes **zero prior setup** beyond having a computer. This is written as if it will live in your repo as `README.md` and should work for **anyone who clones the repository**.

I’ll be explicit about:

* What to install
* Where to install it
* Exact commands (PowerShell)
* Common Windows pitfalls

No cloud infra, no Docker required for v0.

---

# Lux CRM — Local Setup Guide (Windows 11)

This guide walks you through setting up and running the **Lux-powered personal research CRM** locally on **Windows 11**, using only a **Lux API key**.

---

## 0. System Requirements

### Required

* Windows 11 (64-bit)
* Internet connection
* Lux API key (from OpenAGI)

### Recommended

* 16 GB RAM
* Chrome or Edge (Lux handles browsing internally)

---

## 1. Install Required Tools

### 1.1 Install Git

1. Download Git for Windows:
   👉 [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Run the installer
3. Accept defaults **except**:

   * When asked about terminal: select **“Use Git from the Windows Command Prompt”**
4. Finish installation

Verify:

```powershell
git --version
```

---

### 1.2 Install Python 3.10+

1. Download Python from:
   👉 [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)

2. **IMPORTANT**:

   * ✅ Check **“Add Python to PATH”**
   * Choose Python **3.10 or 3.11**

3. Install

Verify:

```powershell
python --version
```

If this fails, restart your computer.

---

### 1.3 Install Node.js (LTS)

1. Download Node.js LTS:
   👉 [https://nodejs.org/](https://nodejs.org/)

2. Install with defaults

Verify:

```powershell
node --version
npm --version
```

---

## 2. Clone the Repository

Open **PowerShell** (not Command Prompt):

```powershell
git clone https://github.com/YOUR_USERNAME/lux-crm.git
cd lux-crm
```

Your folder should now look like:

```
lux-crm/
├── backend/
├── frontend/
├── .env.example
└── README.md
```

---

## 3. Backend Setup (FastAPI + Lux)

### 3.1 Create Python Virtual Environment

From the repo root:

```powershell
cd backend
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

You should now see `(venv)` in your terminal.

---

### 3.2 Install Backend Dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

If anything fails, re-run the command once.

---

### 3.3 Configure Environment Variables

Go back to repo root:

```powershell
cd ..
```

Create `.env` file:

```powershell
copy .env.example .env
```

Edit `.env` using Notepad:

```powershell
notepad .env
```

Add your Lux API key:

```env
LUX_API_KEY=your_lux_api_key_here
```

Save and close.

---

### 3.4 Initialize Database

The database is SQLite and auto-created on first run.
No manual setup needed.

---

### 3.5 Start Backend Server

```powershell
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

You should see:

```
Uvicorn running on http://127.0.0.1:8000
```

Leave this terminal open.

---

## 4. Frontend Setup (Next.js UI)

Open **a new PowerShell window**.

### 4.1 Navigate to Frontend

```powershell
cd lux-crm\frontend
```

---

### 4.2 Install Frontend Dependencies

```powershell
npm install
```

This may take 1–2 minutes.

---

### 4.3 Start Frontend

```powershell
npm run dev
```

You should see:

```
Local: http://localhost:3000
```

---

## 5. Using the Application

### 5.1 Open UI

Open browser:

```
http://localhost:3000
```

---

### 5.2 Run a Research Agent

1. Enter a query like:

   ```
   Robotics PhD students working on SLAM
   ```

2. Click **Start Agent**

3. Lux agent will:

   * Search the web
   * Visit pages
   * Extract people + emails
   * Populate the local CRM

⏳ This can take 30–120 seconds depending on query.

---

### 5.3 View Results

Navigate to:

```
http://localhost:3000/contacts
```

You should see:

* Names
* Emails
* Affiliations
* Fields
* Source URLs

---

## 6. Common Windows Issues & Fixes

### ❌ `python` not recognized

**Fix**:

* Reinstall Python
* Ensure “Add Python to PATH” is checked
* Restart computer

---

### ❌ `uvicorn` not found

**Fix**:

```powershell
pip install uvicorn
```

Ensure virtual environment is activated.

---

### ❌ Frontend can’t reach backend

Ensure:

* Backend is running on port `8000`
* Frontend uses `http://localhost:8000`

---

## 7. Stopping the App

To stop backend or frontend:

```powershell
Ctrl + C
```

---

## 8. What This Setup Gives You

✅ Fully local research CRM
✅ Lux-powered autonomous agents
✅ No cloud services required
✅ SQLite-based persistent storage
✅ UI-driven agent execution
✅ Windows-native setup

---

## 9. Recommended Next Steps (Optional)

* Add email drafting agent
* Add approval workflow
* Add vector search
* Add scheduling / refresh jobs
* Package as Docker later

---

If you want, next I can:

* Convert this into a **one-command installer**
* Add **Docker for Windows**
* Add **agent progress streaming**
* Or turn this into a **research-grade open-source release**

Just say the word.
