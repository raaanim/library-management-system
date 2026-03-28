# Library Management System – Installation Instructions

This guide explains how to set up the development environment for the project.

All installation commands must be executed **after activating the virtual environment**. Otherwise, packages will be installed globally on the system.

## 1. Create a virtual environment

```bash
python3 -m venv .venv
```

## 2. Activate the virtual environment

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows (Command Prompt)

```cmd
.venv\Scripts\activate.bat
```

After activation, the terminal will display the prefix `(.venv)` at the beginning of the line, indicating that the virtual environment is active.

If PowerShell blocks script execution, run the following command once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Exit the virtual environment

To deactivate the virtual environment:

```bash
deactivate
```

After this command, the `(.venv)` prefix will disappear, indicating that you have returned to the system Python environment.

## 3. Upgrade pip

With the virtual environment active, upgrade `pip`:

```bash
pip install --upgrade pip
```

## 4. Install production dependencies

```bash
pip install -r requirements.txt
```

## 5. Install development dependencies

```bash
pip install -r requirements_dev.txt
```

## 6. Verify installation

To check that the packages were installed correctly:

```bash
pip list
```

## 7. Fix Flask import issues

Open the project folder in Visual Studio Code.

Select the Python interpreter:

Ctrl + Shift + P
Python: Select Interpreter

Then select:

.venv/bin/python

## 8. Running the project (Flask)

Make sure the virtual environment is activated before running the app.

### Linux / macOS

```
flask --app src.app run
```

or

```
export FLASK_APP=src.app
export FLASK_ENV=development
flask run
```

### Windows (Command Prompt)

```
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

### Windows (PowerShell)

```
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
flask run
```

## Database Migrations with Flask-Migrate

Run the following commands from the project root directory and inside your virtual environment `(venv)`.

### 1. Initialize the migrations folder (only once)

```
flask --app src.app db init
```

### 2. Generate the first migration (analyzes your models)

```
flask --app src.app db migrate -m "initial migration"
```

### 3. Apply the migration to the database

```
flask --app src.app db upgrade
```

## Recommended Visual Studio Code extensions

- Python
- Pylance
- Python Debugger
- Python Environments
- SQLite Viewer
  
