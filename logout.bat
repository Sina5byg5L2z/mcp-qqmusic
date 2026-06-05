@echo off
cd /d "%~dp0"
uv run python -c "import os; f='credential.json'; os.remove(f) if os.path.exists(f) else None; print('Done.')"
pause
