#!/bin/bash
# ─────────────────────────────────────────────
#  SPIDEY TODO — setup.sh
#  Run this once to create a virtual environment
#  and install all dependencies cleanly.
#
#  Usage:
#    chmod +x setup.sh
#    ./setup.sh
# ─────────────────────────────────────────────

set -e  # exit on any error

echo ""
echo "🕷️  SPIDEY TODO — Environment Setup"
echo "─────────────────────────────────────"

# ── Step 1: Create virtual environment ──
if [ -d "venv" ]; then
  echo "✓ Virtual environment already exists (venv/)"
else
  echo "→ Creating virtual environment..."
  python3 -m venv venv
  echo "✓ Virtual environment created at venv/"
fi

# ── Step 2: Activate it ──
echo "→ Activating virtual environment..."
source venv/bin/activate

# ── Step 3: Upgrade pip ──
echo "→ Upgrading pip..."
pip install --upgrade pip --quiet

# ── Step 4: Install dependencies ──
echo "→ Installing dependencies from requirements.txt..."
pip install -r requirements.txt --quiet

echo ""
echo "✅ Setup complete!"
echo ""
echo "─────────────────────────────────────"
echo "  To activate the environment:"
echo "    source venv/bin/activate"
echo ""
echo "  To start the server:"
echo "    python server.py"
echo ""
echo "  To import a file:"
echo "    python import.py yourfile.txt"
echo ""
echo "  To deactivate when done:"
echo "    deactivate"
echo "─────────────────────────────────────"
