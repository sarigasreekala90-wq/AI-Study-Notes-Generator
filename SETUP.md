# Setup and Installation Guide

## Quick Start (5 minutes)

### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Then open http://localhost:5000 in your browser.

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```
Then open http://localhost:5000 in your browser.

## Detailed Installation

### Step 1: Prerequisites
- Python 3.8 or higher
- pip (comes with Python)
- Git (optional, for cloning)

### Step 2: Clone or Download Project
```bash
git clone <repo-url>
cd ai-study-proj
```

Or download the ZIP file and extract it.

### Step 3: Create Virtual Environment
Virtual environments isolate project dependencies from your system Python.

**Windows:**
```bash
python -m venv venv
```

**macOS/Linux:**
```bash
python3 -m venv venv
```

### Step 4: Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt.

### Step 5: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Werkzeug (password hashing)
- Click, Jinja2, MarkupSafe, itsdangerous, blinker (Flask dependencies)

### Step 6: Run the Application
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 7: Access the Application
Open your browser and go to: `http://localhost:5000`

## Troubleshooting

### Python not found
Make sure Python is installed and added to PATH:
```bash
python --version
```

### "No module named flask"
Make sure you:
1. Activated the virtual environment (see Step 4)
2. Installed requirements (see Step 5)

### Port 5000 already in use
Change the port in app.py:
```python
if __name__ == "__main__":
    app.run(debug=True, port=5001)
```

### Database errors
Delete `database.db` and restart the app:
```bash
del database.db  # Windows
rm database.db   # macOS/Linux
python app.py
```

### Styles not loading
Clear browser cache:
- Windows: Ctrl + Shift + Delete
- macOS: Cmd + Shift + Delete
- Then hard refresh: Ctrl + F5 (Cmd + Shift + R on Mac)

## Environment Variables (Optional)

For added security, create a `.env` file:
```
SECRET_KEY=your-very-secure-secret-key-here
```

Then load it in your app (already implemented).

## Database Inspection

Check what's in the database:
```bash
python check_db.py
```

This displays all users, notes, and generated notes in a formatted table.

## Project Structure
```
ai-study-proj/
├── app.py                 # Main Flask application
├── check_db.py            # Database inspection tool
├── requirements.txt       # Python dependencies
├── database.db           # SQLite database (created after first run)
├── static/
│   ├── style.css         # Styling (2000+ lines)
│   └── script.js         # JavaScript functionality (400+ lines)
├── templates/
│   ├── home.html         # Landing page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   └── dashboard.html    # Main dashboard
└── .gitignore           # Git exclusions for version control
```

## File Sizes (Approximate)
- app.py: ~400 lines
- script.js: ~400 lines
- style.css: ~600 lines
- HTML files: ~150-300 lines each

## Deactivating Virtual Environment
When you're done:
```bash
deactivate
```

## Tips

1. **Always activate the venv** before running the app
2. **Use `debug=True`** only during development
3. **Change the secret key** before deploying to production
4. **Back up your database** before making major changes
5. **Test thoroughly** after making changes

## Useful Commands
```bash
# See what's installed
pip list

# Update a package
pip install --upgrade package_name

# Freeze dependencies (create requirements.txt)
pip freeze > requirements.txt

# Delete venv (when done with project)
rm -r venv  # macOS/Linux
rmdir /s venv  # Windows
```

## Next Steps

1. Create an account by registering
2. Generate some notes to test
3. Explore all features (copy, download, delete, search)
4. Inspect the database with `python check_db.py`
5. Read the code comments to understand how it works
6. Modify and customize as needed!

## Support

- Check the main README.md for project overview
- Review code comments for implementation details
- Check browser console (F12) for JavaScript errors
- Use `python check_db.py` to debug database issues

Happy coding! 🎓
