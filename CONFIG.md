# Configuration Guide

## Environment Variables

### Development
```bash
export SECRET_KEY="dev-secret-key-change-this"
python app.py
```

### Production
Set a strong, random secret key:
```bash
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
python app.py
```

On Windows:
```powershell
$env:SECRET_KEY = (python -c "import secrets; print(secrets.token_hex(32))")
python app.py
```

## Flask Configuration

Edit `app.py` to customize:

### Debug Mode
```python
app.run(debug=False)  # Turn off for production
```

### Port
```python
app.run(port=3000)  # Use port 3000 instead of 5000
```

### Host
```python
app.run(host='0.0.0.0')  # Make accessible from other computers
```

## Database Configuration

Default: SQLite database file (`database.db`)

To use a different location:
```python
# In app.py, change the database path
db_path = "path/to/database.db"
conn = sqlite3.connect(db_path)
```

## Input Validation Limits

Current limits (edit in `app.py`):
- Username: 3-20 characters
- Email: Standard email format
- Password: Minimum 6 characters
- Topic: Maximum 50 characters

To change, modify the validation functions:
```python
def validate_username(username):
    if len(username) < 5:  # Change 3 to 5
        return "Username must be 5+ characters"
```

## Styling Customization

Edit `static/style.css`:

### Colors
```css
/* Green accent color */
color: #16a34a;

/* Change to custom color */
color: #your-color-here;
```

### Font
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", ...;

/* Change to any font */
font-family: 'Arial', sans-serif;
```

### Spacing
```css
padding: 24px;  /* Change to 16px or 32px */
gap: 24px;      /* Adjust spacing between elements */
```

## Study Notes Generation

Customize the generated notes template in `app.py`:

```python
def generate_study_notes(topic):
    topic_title = topic.strip().title()
    return {
        "topic": topic_title,
        "definition": f"Your custom template here...",
        # ... more fields
    }
```

## Security Configuration

### Session Configuration
```python
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True  # No JavaScript access
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour timeout
```

### CORS (if needed)
```python
from flask_cors import CORS
CORS(app)
```

## Logging

Add logging for debugging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# In your routes:
logger.info(f"User {username} logged in")
logger.error(f"Database error: {e}")
```

## Database Backup

Manually backup your database:
```bash
cp database.db database.db.backup  # macOS/Linux
copy database.db database.db.backup  # Windows
```

Or use your OS file manager to copy the file.

## Performance Tuning

### Enable Database Indexing
```python
# In init_generated_notes_table()
cur.execute("CREATE INDEX IF NOT EXISTS idx_user_created ON generated_notes(user, created_at)")
```

### Pagination for Large Datasets
```python
def get_notes_paginated(user, page=1, per_page=10):
    offset = (page - 1) * per_page
    cur.execute(
        "SELECT * FROM generated_notes WHERE user=? ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (user, per_page, offset)
    )
```

## Advanced Features

### Email Notifications (Future)
```python
from flask_mail import Mail
mail = Mail(app)
```

### Rate Limiting (Future)
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: session.get('user'))
```

### Analytics (Future)
```python
def log_activity(user, action):
    # Log user actions for analytics
    pass
```

## Testing

Run basic tests:
```python
# test_app.py
import app
client = app.app.test_client()
response = client.get('/')
assert response.status_code == 200
```

## Deployment Checklist

- [ ] Set strong SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Use production database
- [ ] Enable HTTPS
- [ ] Set secure session cookies
- [ ] Backup database regularly
- [ ] Monitor logs
- [ ] Test all features
- [ ] Document any custom changes

## Troubleshooting Configuration

### App won't start
Check debug output:
```bash
python app.py 2>&1 | head -50
```

### Database locked
Too many connections. Increase timeout:
```python
conn = sqlite3.connect("database.db", timeout=10.0)
```

### Memory issues
Limit query results:
```python
LIMIT 100  # Instead of unlimited
```

## Resources

- Flask Docs: https://flask.palletsprojects.com/
- SQLite Docs: https://www.sqlite.org/docs.html
- Werkzeug Security: https://werkzeug.palletsprojects.com/security/
- CSS Tips: https://developer.mozilla.org/en-US/docs/Web/CSS/

---

**Last Updated:** 2026
**Version:** 1.0.0
