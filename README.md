# 📂 ShareBox – File Transfer & Sharing App

ShareBox is a simple **Flask-based file sharing app** with role-based access:
- **Admins** can upload and delete files.
- **Users** can view and download files uploaded by their assigned admin.
- Supports image, video, and audio previews.
- Secure password hashing and reset system.
- Clean responsive UI with light/dark mode toggle.

---

## 🚀 Features
- 🔑 User registration with roles (Admin / User)
- 👩‍💻 Admin reference code system for linking users
- 📂 File upload/download (with previews for media)
- 🗑️ File deletion (admin only, via AJAX)
- 🌗 Light/Dark theme toggle (saved in local storage)
- 🔐 Secure authentication (hashed passwords)
- 🔄 Forget & Reset password workflow
- 🌍 Auto-detects local IP and opens browser automatically

---

## 🛠️ Requirements

- Python **3.8+** (tested with 3.8, 3.9, 3.10, 3.11)
- No external database needed – uses **SQLite3** (built-in with Python)
- Dependencies:
  - `Flask`
  - `Werkzeug` (comes with Flask)
  - `Jinja2` (comes with Flask)

---

## 📥 Installation

1. **Clone or download** this repository:
   ```bash
   git clone https://github.com/yourusername/sharebox.git
   cd sharebox
Create a virtual environment (recommended):

bash
Copy code
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
Install dependencies:

bash
Copy code
pip install flask
(Werkzeug and Jinja2 will be installed automatically.)

Verify installation:

bash
Copy code
python -m flask --version
▶️ Usage
Run the app:

bash
Copy code
python file_transfer_app.py
On startup, the app:

Creates a SQLite database file (app.db) if not present

Creates an uploads/ folder for storing files

Detects your local IP

Automatically opens your browser to http://<your-ip>:5000

Register an Admin account:

Go to http://127.0.0.1:5000/register

Select Admin

Copy the generated Admin Reference Code

Register a User account:

Go to http://127.0.0.1:5000/register

Select User

Enter the Admin Reference Code to link the account

Login and start sharing files!

📂 File Management
Admins:

Upload multiple files

Delete files

Share reference code with users

Users:

Can only view and download files from their assigned admin

Supported previews:

Images: .png, .jpg, .jpeg, .gif

Videos: .mp4, .webm, .ogg

Audio: .mp3, .wav, .ogg

Other file types can still be downloaded but won’t show previews.

🔧 Project Structure
bash
Copy code
file_transfer_app.py   # Main Flask app
app.db                 # SQLite database (auto-created)
uploads/               # Uploaded files (auto-created)
static/logo.svg        # App logo
🔒 Security Notes
Passwords are stored hashed using Werkzeug.

Sessions use Flask’s secret_key.

For production:

Change app.secret_key to a secure random value.

Run with a production-ready server (e.g., Gunicorn, uWSGI, nginx).

Consider using HTTPS.

🐛 Troubleshooting
Port already in use:
Change port in file_transfer_app.py:

python
Copy code
app.run(host="0.0.0.0", port=8080, debug=True)
Database reset:
Delete app.db and restart app to start fresh.

File not found on preview/download:
Ensure files exist inside the uploads/ folder.

📜 License
MIT License – feel free to use and modify.

💡 Future Enhancements
Email verification & password reset links

File sharing via direct links

Search & filter files

Admin dashboard with analytics
