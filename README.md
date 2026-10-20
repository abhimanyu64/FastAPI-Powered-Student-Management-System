# Student Database Project (Backend + Frontend)

## Requirements
- Python 3.10+
- A modern browser

## Run on Windows PowerShell

Open PowerShell in this extracted project folder.

### 1. Install backend dependencies
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 2. Start the backend
Keep this terminal open:
```powershell
python -m uvicorn backend.main:app --reload
```
Backend API: http://127.0.0.1:8000
Interactive API docs: http://127.0.0.1:8000/docs

### 3. Start the frontend
Open a **second** PowerShell terminal in this same project folder and run:
```powershell
python -m http.server 5500 --directory frontend
```
Open http://127.0.0.1:5500 in your browser.

The SQLite database file (`students.db`) is created automatically in the project root when the backend starts.
