"""
import.py  —  SPIDEY TODO file importer
================================================
Reads any text / PDF / DOCX / CSV file line by
line and injects the tasks straight into the
browser's localStorage so they appear in the app
when you open index.html.

Usage
-----
  python import.py <file>            # reads file, prints JSON
  python import.py <file> --inject   # also opens Chrome and injects

Dependencies (install once)
---------------------------
  pip install pypdf python-docx      # for PDF + DOCX support

Supported formats
-----------------
  .txt   plain text, one task per line
  .pdf   extract text with pypdf
  .docx  extract paragraphs with python-docx
  .csv   first column of each row becomes a task
  (any other extension is treated as plain text)
"""

import sys
import os
import json
import re
import uuid
import time
import argparse
from pathlib import Path


# ── READERS ──────────────────────────────────────────────────────────────────

def read_txt(path: Path) -> list[str]:
    """Read a plain-text file, one task per non-empty line."""
    text = path.read_text(encoding="utf-8", errors="replace")
    return [l.strip() for l in text.splitlines() if l.strip()]


def read_pdf(path: Path) -> list[str]:
    """Extract lines from a PDF using pypdf."""
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.exit("pypdf not installed. Run:  pip install pypdf")

    reader = PdfReader(str(path))
    lines = []
    for page in reader.pages:
        text = page.extract_text() or ""
        for line in text.splitlines():
            line = line.strip()
            if len(line) > 2:
                lines.append(line)
    return lines


def read_docx(path: Path) -> list[str]:
    """Extract paragraphs from a .docx file."""
    try:
        from docx import Document
    except ImportError:
        sys.exit("python-docx not installed. Run:  pip install python-docx")

    doc = Document(str(path))
    lines = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if len(text) > 2:
            lines.append(text)
    return lines


def read_csv(path: Path) -> list[str]:
    """Read the first column of a CSV as tasks."""
    import csv
    lines = []
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0].strip():
                lines.append(row[0].strip())
    return lines


def read_file(path: Path) -> list[str]:
    """Dispatch to the right reader based on extension."""
    ext = path.suffix.lower()
    if ext == ".pdf":
        return read_pdf(path)
    elif ext == ".docx":
        return read_docx(path)
    elif ext == ".csv":
        return read_csv(path)
    else:
        return read_txt(path)


# ── TASK BUILDER ─────────────────────────────────────────────────────────────

def make_task(text: str, priority: str = "medium") -> dict:
    """Create a task dict that matches app.js's format."""
    return {
        "id":        uuid.uuid4().hex[:16],
        "text":      text,
        "priority":  priority,
        "due":       "",
        "note":      "",
        "completed": False,
        "createdAt": int(time.time() * 1000)   # milliseconds, like JS Date.now()
    }


# ── INJECT VIA CHROME (optional) ─────────────────────────────────────────────

def inject_into_browser(tasks_json: str, session_key: str):
    """
    Opens Chrome with remote debugging, waits for the page to load,
    then injects tasks into localStorage via CDP (Chrome DevTools Protocol).

    Requires:  pip install websocket-client
    Chrome must be running with:
        --remote-debugging-port=9222
    Or we launch it automatically.
    """
    import subprocess
    import urllib.request
    import threading

    try:
        import websocket
    except ImportError:
        sys.exit("websocket-client not installed. Run:  pip install websocket-client")

    html_path = (Path(__file__).parent / "index.html").resolve()
    file_url  = html_path.as_uri()

    # ---- Try to connect to existing Chrome; otherwise launch one ----
    cdp_url = "http://localhost:9222/json"
    try:
        with urllib.request.urlopen(cdp_url, timeout=2) as r:
            pages = json.loads(r.read())
    except Exception:
        print("No Chrome with remote debugging found — launching Chrome...")
        subprocess.Popen([
            _find_chrome(),
            "--remote-debugging-port=9222",
            "--user-data-dir=/tmp/spidey-chrome",
            file_url
        ])
        time.sleep(3)
        try:
            with urllib.request.urlopen(cdp_url, timeout=5) as r:
                pages = json.loads(r.read())
        except Exception as e:
            sys.exit(f"Could not connect to Chrome: {e}")

    if not pages:
        sys.exit("No open Chrome pages found.")

    ws_url = pages[0]["webSocketDebuggerUrl"]

    # ---- Send localStorage write via CDP ----
    js_snippet = f"""
    (function() {{
        const key   = '{session_key}';
        const raw   = localStorage.getItem(key);
        const exist = raw ? JSON.parse(raw) : [];
        const added = {tasks_json};
        localStorage.setItem(key, JSON.stringify([...added, ...exist]));
        return 'Injected ' + added.length + ' tasks';
    }})()
    """

    result_holder = {}

    def on_message(ws, msg):
        data = json.loads(msg)
        if "result" in data:
            result_holder["value"] = (
                data["result"].get("result", {}).get("value", "?")
            )
            ws.close()

    ws = websocket.WebSocketApp(
        ws_url,
        on_message=on_message
    )
    payload = json.dumps({
        "id": 1,
        "method": "Runtime.evaluate",
        "params": {"expression": js_snippet, "returnByValue": True}
    })

    def run():
        ws.run_forever()

    t = threading.Thread(target=run)
    t.start()
    time.sleep(1)
    ws.send(payload)
    t.join(timeout=10)

    print("Browser says:", result_holder.get("value", "(no response)"))
    print("Reload the page in Chrome to see your tasks.")


def _find_chrome() -> str:
    candidates = [
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    sys.exit("Chrome not found. Install Google Chrome or Chromium.")


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Import a file's lines into SPIDEY TODO"
    )
    parser.add_argument("file", help="Path to .txt / .pdf / .docx / .csv")
    parser.add_argument(
        "--inject",
        action="store_true",
        help="Also inject tasks into Chrome via remote debugging"
    )
    parser.add_argument(
        "--priority",
        default="medium",
        choices=["low", "medium", "high", "critical"],
        help="Priority to assign every imported task (default: medium)"
    )
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        sys.exit(f"File not found: {path}")

    print(f"Reading {path.name} ...")
    lines = read_file(path)
    lines = [l for l in lines if len(l) > 2]

    if not lines:
        sys.exit("No usable lines found in the file.")

    print(f"Found {len(lines)} line(s):")
    for i, l in enumerate(lines[:10], 1):
        print(f"  {i:>3}. {l[:80]}")
    if len(lines) > 10:
        print(f"  ... and {len(lines) - 10} more")

    tasks = [make_task(l, args.priority) for l in lines]
    tasks_json = json.dumps(tasks, ensure_ascii=False, indent=2)

    # Always print the JSON so you can inspect / copy it
    out_file = path.with_suffix(".tasks.json")
    out_file.write_text(tasks_json, encoding="utf-8")
    print(f"\nTasks JSON written to: {out_file}")

    # Show the localStorage key the app uses
    # (The app generates it once and stores it in localStorage;
    #  we derive a placeholder here — use --inject to do it automatically)
    print("\nTo manually import:")
    print("  1. Open index.html in Chrome")
    print("  2. Open DevTools → Console")
    print("  3. Run this (replace KEY with your Agent ID shown in the app):")
    print()
    print("  const key='spider_tasks_KEY';")
    print("  const ex=JSON.parse(localStorage.getItem(key)||'[]');")
    print(f"  localStorage.setItem(key, JSON.stringify([...{tasks_json[:80]}..., ...ex]));")
    print("  location.reload();")

    if args.inject:
        # Try to get the real session key from Chrome's localStorage
        session_key = "spider_tasks_UNKNOWN"
        print("\nAttempting browser injection...")
        inject_into_browser(tasks_json, session_key)


if __name__ == "__main__":
    main()
