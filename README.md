# 🕷️ SPIDEY TODO

> A Spider-Man themed personal task manager with a neon glass UI,
> private per-browser storage, and a Python importer that reads any file
> line by line into your todo list.

---

## 📁 Project Structure

```
spidey-todo/
│
├── index.html          ← Main HTML — app shell & layout
├── style.css           ← All visual styles (glass, neon, wallpaper)
├── app.js              ← All app logic (tasks, storage, filters, import)
│
├── server.py           ← Flask web server for hosting
├── import.py           ← Python CLI importer (.txt / .pdf / .docx / .csv)
│
├── requirements.txt    ← All Python dependencies
├── setup.sh            ← One-command setup (Linux / Mac)
├── setup.bat           ← One-command setup (Windows)
├── Procfile            ← Deployment config for Render / Railway / Heroku
├── .gitignore          ← Git ignore rules (includes venv/)
│
├── wallpaper.jpg       ← Spider-Man background image
├── spider-logo.png     ← Spider logo (used in header)
│
└── README.md           ← You are here
```

---

## 🚀 Quick Start

### Option 1 — Open Locally (no Python needed)

Just double-click `index.html` — works in any modern browser instantly.

---

### Option 2 — Run with Flask (for hosting / file upload API)

**Linux / Mac:**
```bash
chmod +x setup.sh
./setup.sh
source venv/bin/activate
python server.py
```

**Windows:**
```bat
setup.bat
venv\Scripts\activate
python server.py
```

Then open **http://localhost:5000**

---

## 🐍 Virtual Environment (recommended)

Always use a virtual environment — this keeps SPIDEY TODO's dependencies
isolated from your global Python and prevents version conflicts.

### Why this matters

Installing packages globally can cause conflicts when different projects
need different versions of the same library. A virtual environment gives
this project its own private copy of every dependency.

### Manual setup (if you prefer not to use the setup scripts)

```bash
# 1. Create the virtual environment
python3 -m venv venv          # Linux / Mac
python  -m venv venv          # Windows

# 2. Activate it
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
python server.py

# 5. When you're done
deactivate
```

### VS Code tip

If VS Code shows the message:

> *"Would you like to create a virtual environment with these packages?"*

Click **Yes** — it will create the `venv/` folder and select it as your
Python interpreter automatically. Then open the integrated terminal and run:

```bash
pip install -r requirements.txt
python server.py
```

### Daily workflow

```bash
# Every time you work on the project:
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows

python server.py              # start the app
python import.py myfile.txt   # import a file

deactivate                    # when done
```

> **Note:** The `venv/` folder is in `.gitignore` — never commit it.
> Anyone cloning the repo just runs `setup.sh` / `setup.bat` to recreate it.

---

## 🌐 Hosting Guide

### Render.com (free tier available)

1. Push this folder to a GitHub repo
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repo
4. Set these values:

   | Field | Value |
   |---|---|
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `gunicorn server:app --bind 0.0.0.0:$PORT` |
   | **Environment** | Python 3 |

5. Click **Deploy** — live at `https://your-app.onrender.com`

> No virtual environment needed on hosting platforms — they isolate
> dependencies automatically per deployment.

---

### Railway.app

```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

Or connect your GitHub repo — Railway auto-detects the `Procfile`.

---

### Heroku

```bash
heroku login
heroku create spidey-todo
git push heroku main
heroku open
```

---

### Fly.io

```bash
fly launch        # auto-detects Flask
fly deploy
fly open
```

---

### VPS / Self-hosted (Ubuntu/Debian)

```bash
git clone <your-repo> /var/www/spidey-todo
cd /var/www/spidey-todo

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run as daemon
gunicorn server:app --bind 0.0.0.0:5000 --daemon --workers 2
```

**systemd service** (`/etc/systemd/system/spidey-todo.service`):
```ini
[Unit]
Description=Spidey TODO
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/spidey-todo
ExecStart=/var/www/spidey-todo/venv/bin/gunicorn server:app --bind 0.0.0.0:5000 --workers 2
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
systemctl enable spidey-todo
systemctl start  spidey-todo
```

---

### Windows Server

```bat
setup.bat
venv\Scripts\activate
waitress-serve --host=0.0.0.0 --port=5000 server:app
```

---

## 🔌 Server API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves `index.html` |
| `GET` | `/<filename>` | Serves static files (CSS, JS, images) |
| `GET` | `/api/tasks/<session_id>` | Get saved tasks for a session |
| `POST` | `/api/tasks/<session_id>` | Save / replace all tasks |
| `POST` | `/api/tasks/<session_id>/import` | Import lines as tasks |
| `POST` | `/api/upload` | Upload a file, get back parsed lines |
| `GET` | `/health` | Health check → `{"status":"ok"}` |

---

## 🐍 Python Importer CLI

```bash
# Activate venv first
source venv/bin/activate    # Linux / Mac
venv\Scripts\activate       # Windows

# Then run
python import.py my-tasks.txt
python import.py notes.pdf
python import.py report.docx
python import.py data.csv

# Set priority for all imported tasks
python import.py tasks.txt --priority high

# Inject directly into Chrome
python import.py tasks.txt --inject
```

### Supported file types

| Extension | How it's read |
|---|---|
| `.txt` | One task per line |
| `.pdf` | Text extracted with **pypdf** |
| `.docx` | Each paragraph = one task via **python-docx** |
| `.csv` | First column of every row |
| other | Treated as plain text |

---

## 📦 Dependencies (`requirements.txt`)

```
pypdf==4.3.1             # Read PDF files
python-docx==1.1.2       # Read .docx Word documents
websocket-client==1.8.0  # Chrome injection (--inject flag)
flask==3.0.3             # Web server
flask-cors==4.0.1        # Cross-origin requests
gunicorn==22.0.0         # Production server (Linux/Mac)
waitress==3.0.0          # Production server (Windows)
```

---

## 🕹️ App Features

| Feature | Description |
|---|---|
| **Private storage** | Unique Agent ID per browser — tasks in `localStorage`, no account |
| **Add tasks** | Type and press **SHOOT** or `Enter` |
| **Priority levels** | Low · Medium · High · Critical — colour-coded |
| **Due dates** | Overdue tasks glow red with ⚠ |
| **Notes** | Optional `// comment` per task |
| **Filters** | All · Active · Done · Overdue |
| **Search** | Live search across text and notes |
| **Progress bar** | Shows % complete |
| **Browser import** | Click 📎 in the app — pick `.txt` / `.pdf` / `.docx` |
| **Python import** | Run `import.py` from terminal |

---

## 🎨 Customising

Edit the CSS variables at the top of `style.css`:

```css
:root {
  --red-glow:     #ff2040;
  --glass-bg:     rgba(10, 5, 20, 0.35);
  --glass-border: rgba(232, 0, 28, 0.40);
}
```

To change the wallpaper, replace `wallpaper.jpg` with any image.

---

*With great power comes great responsibility — and great task management.*
