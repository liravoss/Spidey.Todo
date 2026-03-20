<div align="center">

```
███████╗██████╗ ██╗██████╗ ███████╗██╗   ██╗    ████████╗ ██████╗ ██████╗  ██████╗ 
██╔════╝██╔══██╗██║██╔══██╗██╔════╝╚██╗ ██╔╝    ╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗
███████╗██████╔╝██║██║  ██║█████╗   ╚████╔╝        ██║   ██║   ██║██║  ██║██║   ██║
╚════██║██╔═══╝ ██║██║  ██║██╔══╝    ╚██╔╝         ██║   ██║   ██║██║  ██║██║   ██║
███████║██║     ██║██████╔╝███████╗   ██║           ██║   ╚██████╔╝██████╔╝╚██████╔╝
╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝   ╚═╝           ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝ 
```

**`🕷️ Your private mission board. No account. No tracking. Just tasks.`**

![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

</div>

---

```
  //                                                          \\
 //   W I T H  G R E A T  P O W E R  C O M E S               \\
//    G R E A T  T A S K  M A N A G E M E N T                  \\
```

---

## 🕸️ What Is This

A **Spider-Man themed personal task manager** built with pure HTML, CSS, and JavaScript.  
Tasks live in your browser — private, local, yours. No login. No cloud. No nonsense.

Import any `.txt`, `.pdf`, or `.docx` file and every line becomes a task.  
Run it locally or deploy it anywhere in minutes.

---

## ⚡ Features

| | Feature | Description |
|---|---|---|
| 🔒 | **Private by default** | Unique Agent ID per browser · Tasks stored in `localStorage` |
| 🎯 | **Priority levels** | Low · Medium · High · Critical — each colour-coded |
| ⏰ | **Due dates** | Overdue tasks glow red with a ⚠ warning |
| 📝 | **Notes** | Optional comment on every task |
| 🔍 | **Live search** | Filter across task text and notes instantly |
| 📊 | **Progress bar** | Shows % of missions completed |
| 📎 | **File import** | Upload `.txt` / `.pdf` / `.docx` — each line = one task |
| 🐍 | **Python importer** | CLI tool to read any file and push tasks to the app |
| 🗑️ | **Clear All** | Wipe everything with one click + confirmation modal |
| 🌐 | **Hostable** | Flask server included — deploy to Render, Railway, Heroku |

---

## 📁 Project Structure

```
spidey-todo/
│
├── 🌐  index.html          ← App shell & layout
├── 🎨  style.css           ← Neon glass UI · Spider-Man theme
├── ⚙️  app.js              ← All logic · storage · filters · import
│
├── 🐍  server.py           ← Flask web server (for hosting)
├── 📥  import.py           ← CLI file importer
│
├── 📋  requirements.txt    ← Python dependencies
├── 🚀  Procfile            ← Render / Railway / Heroku deploy config
├── 🪟  setup.bat           ← One-click Windows setup
├── 🐧  setup.sh            ← One-click Linux/Mac setup
│
├── 🖼️  wallpaper.jpg       ← Spider-Man background
├── 🕷️  spider-logo.png     ← Spider logo
└── 📖  README.md
```

---

## 🚀 Quick Start

### Open Instantly (no install)
```
Just double-click index.html
```

### Run with Flask
```bash
# Windows
setup.bat

# Linux / Mac
chmod +x setup.sh && ./setup.sh

# Then
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

python server.py
# → open http://localhost:5000
```

---

## 🐍 Python File Importer

```bash
# Activate venv first, then:

python import.py my-tasks.txt          # plain text — one task per line
python import.py roadmap.pdf           # PDF — each line becomes a task
python import.py notes.docx            # Word doc — each paragraph = task
python import.py data.csv              # CSV — first column of each row

python import.py tasks.txt --priority high     # set priority for all
python import.py tasks.txt --inject            # push straight into Chrome
```

---

## 🌐 Deploy in 5 Minutes

### Render.com (recommended · free tier)

```
1. Push this repo to GitHub
2. render.com → New Web Service → connect repo
3. Build command : pip install -r requirements.txt
4. Start command : gunicorn server:app --bind 0.0.0.0:$PORT
5. Deploy → live at https://your-app.onrender.com
```

### Railway / Heroku
```bash
# The Procfile handles everything automatically
railway up
# or
git push heroku main
```

---

## 🎨 Tech Stack

```
Frontend  →  Vanilla HTML + CSS + JavaScript  (zero frameworks)
Backend   →  Python · Flask · Gunicorn
Storage   →  Browser localStorage  (private · no server needed)
PDF       →  PDF.js  (loaded from CDN on demand)
DOCX      →  Mammoth.js  (loaded from CDN on demand)
Fonts     →  Orbitron · Rajdhani · Share Tech Mono  (Google Fonts)
```

---

## 🔒 Privacy

```
✓  No account required
✓  No data sent to any server
✓  No tracking, no analytics
✓  Each browser gets its own isolated task list
✓  Incognito mode = temporary list, cleared on close
```

---

<div align="center">

```
 ░██████╗██████╗░██╗██████╗░███████╗██╗░░░██╗  ████████╗░█████╗░██████╗░░█████╗░
 ██╔════╝██╔══██╗██║██╔══██╗██╔════╝╚██╗░██╔╝  ╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗
 ╚█████╗░██████╔╝██║██║░░██║█████╗░░░╚████╔╝░  ░░░██║░░░██║░░██║██║░░██║██║░░██║
 ░╚═══██╗██╔═══╝░██║██║░░██║██╔══╝░░░░╚██╔╝░░  ░░░██║░░░██║░░██║██║░░██║██║░░██║
 ██████╔╝██║░░░░░██║██████╔╝███████╗░░░██║░░░  ░░░██║░░░╚█████╔╝██████╔╝╚█████╔╝
 ╚═════╝░╚═╝░░░░░╚═╝╚═════╝░╚══════╝░░░╚═╝░░░  ░░░╚═╝░░░░╚════╝░╚═════╝░░╚════╝░
```

*Made with 🕷️ and way too much CSS*

</div>