# 🧙‍♂️ Spellbook App

A simple yet powerful web application built with Flask for managing spells — perfect for fantasy fans, tabletop RPG players, or anyone wanting to organize custom magical abilities.

## ✨ Features

- ✅ User Registration and Login (with Flask-Login & Flask-Bcrypt)
- 📖 Create, Read, Update, and Delete (CRUD) spells
- 🖼️ Image upload for each spell
- 🔒 Spells tied to user accounts (only authors can edit/delete)
- 🌐 Public spell list for non-logged-in users (teaser experience)
- 🧑‍💻 Admin-like control for users over their own spellbook
- ➡️ Dynamic footer and animation using JavaScript

## 🔧 Technologies Used

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Bcrypt
- SQLite
- Bootstrap
- HTML/Jinja2 Templates
- JavaScript (jQuery)

## 🚀 Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/spellbook-app.git
   cd spellbook-app

2. **Create a virtual environment and activate it:**   
    ```bash
    python -m venv .venv
    source .venv/bin/activate        # On Windows: .venv\Scripts\activate
   
3. **Install dependencies:**
    ```bash
   pip install -r requirements.txt
   
4. **Create the database:**
    ```bash
   flask shell
    >>> from spellbook import db
    >>> db.create_all()
    >>> exit()
   
5. **Run the App**
    ```bash
   flask run
   
## 📁  Project Structure

```
spellbook_app/
│
├── spellbook/
│   ├── __init__.py        # App factory & setup
│   ├── models.py          # SQLAlchemy models (User, Spell)
│   ├── routes.py          # Flask routes / views
│   ├── templates/         # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── login.html, register.html, account.html
│   │   ├── spells.html, create_spell.html, edit_spell.html
│   └── static/
│       └── images/        # Uploaded spell images
├── config.py              # App config (SECRET_KEY, DB URI, etc.)
├── run.py                 # Entry point
└── README.md
```

## 🛡️ Security Notes
- Passwords are securely hashed using Flask-Bcrypt.
- File uploads are saved only in a specific folder (static/images) with filename sanitization.
- Users can only edit/delete their own spells.

## 💡 Ideas for Expansion
- Add tags or categories to spells
- Search or filter spells
- Image compression

## ⚖️ License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.



