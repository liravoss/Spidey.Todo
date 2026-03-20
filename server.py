"""
server.py  —  SPIDEY TODO web server
======================================
Serves the app over HTTP so it can be hosted
on any machine, VPS, or cloud platform.

Usage
-----
  Development (local):
      python server.py

  Production (Linux / Mac):
      gunicorn server:app --bind 0.0.0.0:5000

  Production (Windows):
      waitress-serve --host=0.0.0.0 --port=5000 server:app

  Then open:  http://localhost:5000

Environment variables (optional)
---------------------------------
  PORT   — port to listen on (default: 5000)
  HOST   — host to bind to  (default: 0.0.0.0)
  DEBUG  — set to "true" for dev mode

Deploy to common platforms
---------------------------
  Render.com:
      Start command: gunicorn server:app --bind 0.0.0.0:$PORT

  Railway.app:
      Start command: gunicorn server:app --bind 0.0.0.0:$PORT

  Heroku:
      Procfile:  web: gunicorn server:app --bind 0.0.0.0:$PORT

  Fly.io:
      fly launch  (auto-detects Flask)

  Self-hosted VPS:
      gunicorn server:app --bind 0.0.0.0:5000 --daemon
"""

import os
import json
import time
import uuid
from pathlib import Path
from flask import (
    Flask, send_from_directory, request,
    jsonify, abort
)
from flask_cors import CORS

# ── APP SETUP ────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent
app = Flask(__name__, static_folder=str(BASE_DIR))
CORS(app)  # allow cross-origin requests (useful when embedding)

# Simple in-memory store for server-side task persistence
# (tasks are ALSO stored in the browser's localStorage — this is a bonus
#  server-side backup that survives browser clears)
_server_tasks: dict[str, list] = {}   # session_id → [task, ...]


# ── STATIC FILES ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve index.html at the root URL."""
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    """Serve CSS, JS, images, etc."""
    return send_from_directory(BASE_DIR, filename)


# ── API — server-side task backup ────────────────────────────────────────────
# The browser uses localStorage as the primary store.
# These endpoints provide an optional server-side backup/sync layer.

@app.route("/api/tasks/<session_id>", methods=["GET"])
def get_tasks(session_id: str):
    """Return all tasks for a session."""
    tasks = _server_tasks.get(session_id, [])
    return jsonify(tasks)


@app.route("/api/tasks/<session_id>", methods=["POST"])
def save_tasks(session_id: str):
    """Replace all tasks for a session (called by the browser on every save)."""
    data = request.get_json(silent=True)
    if not isinstance(data, list):
        abort(400, "Expected a JSON array of tasks")
    _server_tasks[session_id] = data
    return jsonify({"saved": len(data)})


@app.route("/api/tasks/<session_id>/import", methods=["POST"])
def import_tasks(session_id: str):
    """
    Accept a JSON list of task-text strings, convert them to task objects,
    and prepend them to the session's task list.

    Body:  { "lines": ["Task one", "Task two", ...], "priority": "medium" }
    """
    body     = request.get_json(silent=True) or {}
    lines    = body.get("lines", [])
    priority = body.get("priority", "medium")

    if priority not in ("low", "medium", "high", "critical"):
        priority = "medium"

    new_tasks = [
        {
            "id":        uuid.uuid4().hex[:16],
            "text":      str(line).strip(),
            "priority":  priority,
            "due":       "",
            "note":      "",
            "completed": False,
            "createdAt": int(time.time() * 1000)
        }
        for line in lines if str(line).strip()
    ]

    existing = _server_tasks.get(session_id, [])
    _server_tasks[session_id] = new_tasks + existing

    return jsonify({"imported": len(new_tasks), "total": len(_server_tasks[session_id])})


@app.route("/api/upload", methods=["POST"])
def upload_and_parse():
    """
    Accept a file upload, parse it line by line (txt/pdf/docx/csv),
    and return the lines as JSON so the browser can add them as tasks.

    Form field: file
    """
    if "file" not in request.files:
        abort(400, "No file field in request")

    f    = request.files["file"]
    name = f.filename or ""
    data = f.read()

    lines = _parse_bytes(data, name)
    lines = [l.strip() for l in lines if l.strip() and len(l.strip()) > 2]

    return jsonify({"lines": lines, "count": len(lines)})


# ── FILE PARSER (server-side) ─────────────────────────────────────────────────

def _parse_bytes(data: bytes, filename: str) -> list[str]:
    """Parse raw file bytes into a list of text lines."""
    ext = Path(filename).suffix.lower()

    if ext == ".pdf":
        return _parse_pdf(data)
    elif ext == ".docx":
        return _parse_docx(data)
    elif ext == ".csv":
        return _parse_csv(data)
    else:
        # Plain text / fallback
        return data.decode("utf-8", errors="replace").splitlines()


def _parse_pdf(data: bytes) -> list[str]:
    try:
        from pypdf import PdfReader
        import io
        reader = PdfReader(io.BytesIO(data))
        lines = []
        for page in reader.pages:
            text = page.extract_text() or ""
            lines.extend(text.splitlines())
        return lines
    except ImportError:
        return ["[pypdf not installed — plain text only]"]


def _parse_docx(data: bytes) -> list[str]:
    try:
        from docx import Document
        import io
        doc = Document(io.BytesIO(data))
        return [p.text for p in doc.paragraphs]
    except ImportError:
        return ["[python-docx not installed — plain text only]"]


def _parse_csv(data: bytes) -> list[str]:
    import csv
    import io
    reader = csv.reader(io.StringIO(data.decode("utf-8", errors="replace")))
    return [row[0] for row in reader if row]


# ── HEALTH CHECK ─────────────────────────────────────────────────────────────

@app.route("/health")
def health():
    return jsonify({"status": "ok", "app": "spidey-todo"})


# ── ENTRY POINT ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port  = int(os.environ.get("PORT",  5000))
    host  = os.environ.get("HOST",  "0.0.0.0")
    debug = os.environ.get("DEBUG", "false").lower() == "true"

    print(f"""
  🕷️  SPIDEY TODO server starting...
  ───────────────────────────────────
  Local:    http://localhost:{port}
  Network:  http://{host}:{port}
  Debug:    {debug}
  ───────────────────────────────────
  Press Ctrl+C to stop
    """)

    app.run(host=host, port=port, debug=debug)
