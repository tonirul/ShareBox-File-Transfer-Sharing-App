# 📂 ShareBox – File Transfer & Sharing App

A **Flask-based file sharing application** with **user roles (Admin/User)**, secure file uploads, previews, and downloads.  
Everything is stored in a local **SQLite database**, and the app auto-opens in your browser after running.  

---

## 🚀 Features

- 👩‍💼 **Admin**
  - Register with unique **reference code**
  - Upload multiple files at once
  - View, preview, download, and delete files

- 👤 **User**
  - Register using an **Admin reference code**
  - View and download files uploaded by assigned admin

- 🔑 **Authentication**
  - User registration & login system
  - Passwords securely stored using hashing
  - Forgot/reset password functionality

- 📁 **File Management**
  - Supports images, videos, and audio with in-browser preview
  - Secure file download
  - Admin-only file deletion

- 🎨 **Modern UI**
  - Light/Dark mode toggle 🌙/☀️
  - Responsive card-based design

- 🖥️ **Ease of Use**
  - Auto-detects your local IP
  - Automatically opens browser on start

---

## 📦 Requirements

### ✅ Already Included (no need to install separately)
- `os`, `sqlite3`, `random`, `string`, `webbrowser`, `threading`, `time`, `socket` (built-in with Python)

### 📥 Need to Install
You need Python **3.8+** and the following pip packages:

```bash
pip install flask werkzeug
(Flask already includes Jinja2, so no need to install it separately.)

▶️ How to Run
Clone or Download this repository

bash
 
git clone https://github.com/yourusername/sharebox.git
cd sharebox
Run the app

bash
 
python file_transfer_app.py
The app will:

Start a Flask server at http://<your-local-ip>:5000

Auto-open your default browser

📝 Usage Guide
1. Register as Admin
Go to Register

Choose Admin role

After registering, you’ll see a unique reference code (e.g., ADM123456)

2. Register as User
Choose User role

Enter Admin’s reference code

Now this user will be linked to that admin’s files

3. Admin Functions
Upload files (images, audio, video, docs)

Delete files

Share files with linked users

4. User Functions
View all files uploaded by their assigned admin

Download or preview (if supported)

5. Password Reset
Forgot password → enter username

Reset password with a new one

📂 Project Structure
bash
 
project/
│── file_transfer_app.py   # Main application
│── app.db                 # SQLite database (auto-created on first run)
│── uploads/               # Uploaded files (auto-created)
│── static/logo.svg        # App logo
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
