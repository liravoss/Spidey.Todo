/* ─────────────────────────────────────────
   SPIDEY TODO  —  app.js
   All app logic: session, tasks, render,
   filters, file import (PDF / DOCX / TXT)
   ───────────────────────────────────────── */

'use strict';

// ── CLOCK ────────────────────────────────
function updateClock() {
  const n = new Date();
  document.getElementById('clock').textContent =
    n.toLocaleTimeString('en-US', { hour12: false });
  document.getElementById('date-display').textContent =
    n.toLocaleDateString('en-US', {
      weekday: 'long', year: 'numeric',
      month: 'long', day: 'numeric'
    }).toUpperCase();
}
setInterval(updateClock, 1000);
updateClock();

// ── SESSION ID ────────────────────────────
function getSessionId() {
  let id = localStorage.getItem('spider_session_id');
  if (!id) {
    const arr = new Uint8Array(6);
    crypto.getRandomValues(arr);
    id = Array.from(arr)
      .map(b => b.toString(16).padStart(2, '0'))
      .join('')
      .toUpperCase();
    id = `SPD-${id.slice(0,4)}-${id.slice(4,8)}-${id.slice(8)}`;
    localStorage.setItem('spider_session_id', id);
  }
  return id;
}
const SESSION_ID = getSessionId();
document.getElementById('session-display').textContent = SESSION_ID;

// ── STORAGE ───────────────────────────────
const TASKS_KEY = 'spider_tasks_' + SESSION_ID;
let tasks = [];

function loadFromStorage() {
  try {
    const raw = localStorage.getItem(TASKS_KEY);
    if (raw) tasks = JSON.parse(raw);
  } catch (e) {
    tasks = [];
  }
}

function saveToStorage() {
  localStorage.setItem(TASKS_KEY, JSON.stringify(tasks));
}

// ── STATE ─────────────────────────────────
let activeFilter = 'all';
let searchQuery  = '';

// ── ADD TASK ─────────────────────────────
document.getElementById('add-btn')
  .addEventListener('click', addTask);

document.getElementById('task-input')
  .addEventListener('keydown', e => { if (e.key === 'Enter') addTask(); });

function addTask() {
  const input = document.getElementById('task-input');
  const text  = input.value.trim();
  if (!text) { shakeInput(); return; }

  const task = {
    id:        Date.now().toString(36) + Math.random().toString(36).slice(2),
    text,
    priority:  document.getElementById('priority-select').value,
    due:       document.getElementById('due-input').value,
    note:      document.getElementById('note-input').value.trim(),
    completed: false,
    createdAt: Date.now()
  };

  tasks.unshift(task);
  saveToStorage();

  input.value = '';
  document.getElementById('due-input').value  = '';
  document.getElementById('note-input').value = '';

  renderTasks();
  updateStats();
  showToast('Mission logged ✓');
}

function shakeInput() {
  const inp = document.getElementById('task-input');
  inp.style.borderColor = 'var(--red-glow)';
  inp.style.boxShadow   = '0 0 15px rgba(232,0,28,0.4)';
  setTimeout(() => {
    inp.style.borderColor = '';
    inp.style.boxShadow   = '';
  }, 800);
}

// ── FILTERS ───────────────────────────────
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn')
      .forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeFilter = btn.dataset.filter;
    renderTasks();
  });
});

document.getElementById('search-input')
  .addEventListener('input', e => {
    searchQuery = e.target.value.toLowerCase();
    renderTasks();
  });

function getFiltered() {
  const now = Date.now();
  return tasks.filter(t => {
    if (searchQuery &&
        !t.text.toLowerCase().includes(searchQuery) &&
        !(t.note || '').toLowerCase().includes(searchQuery)) return false;

    if (activeFilter === 'active')    return !t.completed;
    if (activeFilter === 'completed') return  t.completed;
    if (activeFilter === 'overdue')
      return !t.completed && t.due && new Date(t.due).getTime() < now;
    return true;
  });
}

// ── RENDER ────────────────────────────────
function renderTasks() {
  const container = document.getElementById('tasks-container');
  const empty     = document.getElementById('empty-state');
  container.innerHTML = '';

  const filtered = getFiltered();
  if (filtered.length === 0) {
    empty.style.display = 'block';
  } else {
    empty.style.display = 'none';
    filtered.forEach(task => container.appendChild(createCard(task)));
  }
  updateStats();
}

function createCard(task) {
  const now      = Date.now();
  const isOverdue = task.due && !task.completed &&
                    new Date(task.due).getTime() < now;

  const card = document.createElement('div');
  card.className =
    `task-card glass p-${task.priority}${task.completed ? ' completed-card' : ''}`;
  card.dataset.id = task.id;

  // Check circle
  const circle = document.createElement('div');
  circle.className = 'check-circle' + (task.completed ? ' checked' : '');
  circle.innerHTML = '<div class="check-mark"></div>';
  circle.addEventListener('click', () => toggleTask(task.id));

  // Body
  const body   = document.createElement('div');
  body.className = 'task-body';

  const textEl = document.createElement('div');
  textEl.className = 'task-text';
  textEl.textContent = task.text;

  const meta = document.createElement('div');
  meta.className = 'task-meta';

  const prio = document.createElement('span');
  prio.className = `priority-badge pb-${task.priority}`;
  prio.textContent = task.priority.toUpperCase();
  meta.appendChild(prio);

  if (task.due) {
    const dueEl = document.createElement('span');
    dueEl.className = 'task-due' + (isOverdue ? ' overdue' : '');
    const d = new Date(task.due);
    dueEl.textContent =
      (isOverdue ? '⚠ OVERDUE: ' : '⏰ ') +
      d.toLocaleString('en-US', {
        month: 'short', day: 'numeric',
        hour: '2-digit', minute: '2-digit'
      });
    meta.appendChild(dueEl);
  }

  body.appendChild(textEl);
  body.appendChild(meta);

  if (task.note) {
    const noteEl = document.createElement('div');
    noteEl.className = 'task-note';
    noteEl.textContent = '// ' + task.note;
    body.appendChild(noteEl);
  }

  // Delete button
  const actions = document.createElement('div');
  actions.className = 'task-actions';
  const del = document.createElement('button');
  del.className = 'action-btn del';
  del.title = 'Delete';
  del.textContent = '✕';
  del.addEventListener('click', () => deleteTask(task.id, card));
  actions.appendChild(del);

  card.appendChild(circle);
  card.appendChild(body);
  card.appendChild(actions);
  return card;
}

function toggleTask(id) {
  const t = tasks.find(x => x.id === id);
  if (t) {
    t.completed = !t.completed;
    saveToStorage();
    renderTasks();
  }
}

function deleteTask(id, card) {
  card.classList.add('fall-out');
  setTimeout(() => {
    tasks = tasks.filter(x => x.id !== id);
    saveToStorage();
    renderTasks();
    showToast('Mission removed');
  }, 360);
}

// ── STATS ─────────────────────────────────
function updateStats() {
  const now    = Date.now();
  const total  = tasks.length;
  const done   = tasks.filter(t => t.completed).length;
  const overdue = tasks.filter(
    t => !t.completed && t.due && new Date(t.due).getTime() < now
  ).length;
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;

  document.getElementById('stat-total').textContent   = total;
  document.getElementById('stat-active').textContent  = total - done;
  document.getElementById('stat-done').textContent    = done;
  document.getElementById('stat-overdue').textContent = overdue;
  document.getElementById('progress-bar').style.width = pct + '%';
  document.getElementById('progress-label').textContent = pct + '% Complete';
}

// ── TOAST ─────────────────────────────────
let toastTimer;
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), 2400);
}

// ── FILE IMPORT (browser-side) ────────────
const fileInput  = document.getElementById('file-import');
const fileLabel  = document.getElementById('file-label-text');
const importBtn  = document.getElementById('import-btn');
let importedLines = [];

fileInput.addEventListener('change', async e => {
  const file = e.target.files[0];
  if (!file) return;
  fileLabel.textContent = '⏳ Reading: ' + file.name;
  importBtn.style.display = 'none';
  importedLines = [];

  try {
    if (file.name.endsWith('.txt')) {
      const text = await file.text();
      importedLines = text.split('\n')
        .map(l => l.trim())
        .filter(l => l.length > 2);

    } else if (file.name.endsWith('.pdf')) {
      importedLines = await readPDF(file);

    } else if (file.name.endsWith('.docx')) {
      importedLines = await readDOCX(file);
    }

    if (importedLines.length > 0) {
      fileLabel.textContent =
        `✓ ${importedLines.length} lines found — click IMPORT`;
      importBtn.style.display = 'block';
    } else {
      fileLabel.textContent = '⚠ No readable lines found in ' + file.name;
    }
  } catch (err) {
    fileLabel.textContent = '⚠ Error: ' + err.message;
  }
  e.target.value = '';
});

importBtn.addEventListener('click', () => {
  let added = 0;
  importedLines.forEach(line => {
    if (line.length < 3) return;
    tasks.unshift({
      id:        Date.now().toString(36) + Math.random().toString(36).slice(2) + added,
      text:      line,
      priority:  'medium',
      due:       '',
      note:      '',
      completed: false,
      createdAt: Date.now()
    });
    added++;
  });

  if (added > 0) {
    saveToStorage();
    renderTasks();
    updateStats();
    showToast(`${added} missions imported ✓`);
  }

  fileLabel.textContent = '📎 Import tasks from .txt / .pdf / .docx — or run import.py';
  importBtn.style.display = 'none';
  importedLines = [];
});

/* Load PDF.js on demand, then extract lines */
async function readPDF(file) {
  if (!window.pdfjsLib) {
    await loadScript(
      'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js'
    );
    window.pdfjsLib.GlobalWorkerOptions.workerSrc =
      'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
  }

  const buf = await file.arrayBuffer();
  const pdf = await window.pdfjsLib.getDocument({ data: buf }).promise;
  const lines = [];

  for (let i = 1; i <= pdf.numPages; i++) {
    const page    = await pdf.getPage(i);
    const content = await page.getTextContent();

    // ── Sort items by vertical position (y) then horizontal (x) ──
    // PDF.js returns items in internal order which is often scrambled.
    // Grouping by Y coordinate reassembles the visual reading order.
    const items = content.items
      .filter(item => item.str.trim().length > 0)
      .map(item => ({
        text: item.str.trim(),
        x: Math.round(item.transform[4]),
        y: Math.round(item.transform[5])
      }));

    // Group into rows by Y (items within 4px are on the same line)
    const rows = [];
    items.forEach(item => {
      const existing = rows.find(r => Math.abs(r.y - item.y) <= 4);
      if (existing) {
        existing.items.push(item);
      } else {
        rows.push({ y: item.y, items: [item] });
      }
    });

    // Sort rows top-to-bottom (higher Y = higher on page in PDF coords)
    rows.sort((a, b) => b.y - a.y);

    // Within each row sort left-to-right, then join into a single string
    rows.forEach(row => {
      row.items.sort((a, b) => a.x - b.x);
      const line = row.items.map(i => i.text).join(' ').trim();
      if (line.length > 2) lines.push(line);
    });
  }

  // Remove obvious separator lines (all dashes/equals)
  return lines.filter(l => !/^[-=*_.]{3,}$/.test(l));
}

/* Load Mammoth.js on demand, then extract lines */
async function readDOCX(file) {
  if (!window.mammoth) {
    await loadScript(
      'https://cdnjs.cloudflare.com/ajax/libs/mammoth/1.6.0/mammoth.browser.min.js'
    );
  }
  const buf    = await file.arrayBuffer();
  const result = await window.mammoth.extractRawText({ arrayBuffer: buf });
  return result.value
    .split('\n')
    .map(l => l.trim())
    .filter(l => l.length > 2);
}

function loadScript(src) {
  return new Promise((res, rej) => {
    const s = document.createElement('script');
    s.src = src;
    s.onload = res;
    s.onerror = rej;
    document.head.appendChild(s);
  });
}

// ── BOOT ──────────────────────────────────
loadFromStorage();
renderTasks();
// Re-check overdue every minute
setInterval(renderTasks, 60_000);

// ── CLEAR ALL ─────────────────────────────
document.getElementById('clear-all-btn')
  .addEventListener('click', () => {
    if (tasks.length === 0) { showToast('No missions to clear'); return; }
    showConfirm();
  });

document.getElementById('confirm-yes')
  .addEventListener('click', () => {
    tasks = [];
    saveToStorage();
    renderTasks();
    updateStats();
    hideConfirm();
    showToast('All missions wiped ✓');
  });

document.getElementById('confirm-no')
  .addEventListener('click', hideConfirm);

document.getElementById('confirm-overlay')
  .addEventListener('click', e => {
    if (e.target === document.getElementById('confirm-overlay')) hideConfirm();
  });

function showConfirm() {
  document.getElementById('confirm-overlay').classList.add('visible');
}
function hideConfirm() {
  document.getElementById('confirm-overlay').classList.remove('visible');
}