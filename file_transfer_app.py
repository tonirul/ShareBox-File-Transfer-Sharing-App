import os, sqlite3, random, string, webbrowser, threading, time, socket
from flask import Flask, request, redirect, url_for, session, send_from_directory, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from jinja2 import DictLoader

# ------------------- Flask Setup -------------------
app = Flask(__name__)
app.secret_key = "super-secret-key"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ------------------- Database -------------------
DB_FILE = "app.db"
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT UNIQUE,
                     password TEXT,
                     role TEXT,
                     ref_code TEXT,
                     assigned_admin INTEGER)""")
        c.execute("""CREATE TABLE IF NOT EXISTS files (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     filename TEXT,
                     uploader_id INTEGER)""")
        conn.commit()
init_db()

# ------------------- Utility -------------------
def generate_ref_code():
    return "ADM" + ''.join(random.choices(string.digits, k=6))

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

# ------------------- Templates -------------------
TEMPLATES = {
"base.html": """
<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ title if title else 'ShareBox' }}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>
:root[data-theme='light'] { --bg:#f0f2f5; --text:#111; --card:#fff; --btn:#4f46e5; --btnText:#fff; --accent:#6366f1; }
:root[data-theme='dark'] { --bg:#1f2937; --text:#f3f4f6; --card:#374151; --btn:#10b981; --btnText:#111; --accent:#3b82f6; }
body { font-family:'Inter',Arial,sans-serif; background:var(--bg); color:var(--text); margin:0; }
header { background:var(--accent); color:#fff; display:flex; align-items:center; justify-content:space-between; padding:1rem 2rem; box-shadow:0 4px 8px rgba(0,0,0,0.2); border-bottom-left-radius:12px; border-bottom-right-radius:12px;}
header img { height:40px; margin-right:1rem; }
header .title { font-weight:700; font-size:1.6rem; }
.topbar button { margin-left:0.5rem; padding:0.5rem 1rem; border:none; border-radius:8px; cursor:pointer; background:var(--btn); color:var(--btnText); font-weight:600; transition:0.2s; }
.topbar button:hover { opacity:0.85; }
.container { max-width:960px; margin:2rem auto; display:flex; flex-direction:column; gap:1.5rem; }
.card { background:var(--card); padding:2rem; border-radius:16px; box-shadow:0 4px 16px rgba(0,0,0,0.15); transition:0.3s; }
.card:hover { box-shadow:0 6px 24px rgba(0,0,0,0.2); transform: translateY(-3px); }
form { display:flex; flex-direction:column; gap:1rem; }
input, select { padding:0.7rem; border-radius:8px; border:1px solid #ccc; font-size:1rem; }
button { padding:0.8rem; border:none; border-radius:8px; cursor:pointer; background:var(--btn); color:var(--btnText); font-weight:600; font-size:1rem; transition:0.2s; }
button:hover { opacity:0.9; }
.flash { padding:10px; border-radius:8px; margin-bottom:0.5rem; text-align:center; font-weight:600; font-size:0.95rem; }
.flash.success { background:#d1fae5; color:#064e3b; }
.flash.danger { background:#fee2e2; color:#991b1b; }
h2 { text-align:center; margin-bottom:1rem; }

.file-list { display:flex; flex-direction:column; gap:1.5rem; }
.file-card { display:flex; flex-direction:column; gap:0.8rem; }
.file-card p { margin:0; word-break:break-word; font-size:1.05rem; }
.file-card img, .file-card video, .file-card audio { border-radius:8px; max-height:300px; object-fit:contain; width:100%; }
.action-btn { width:100%; padding:0.6rem 0; font-size:1rem; border-radius:10px; font-weight:600; cursor:pointer; }
.action-btn.download { background:#3b82f6; color:#fff; margin-bottom:0.5rem; }
.action-btn.delete { background:#ef4444; color:#fff; }
</style>
</head>
<body>
<header>
  <div style="display:flex;align-items:center">
    <img src="/static/logo.svg" alt="Logo">
    <span class="title">ShareBox</span>
  </div>
  <div class="topbar">
    {% if session.get('user') %}<a href='{{ url_for('logout') }}'><button>Logout</button></a>{% endif %}
    <button onclick="toggleTheme()">🌙/☀️</button>
  </div>
</header>
<div class="container">
  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      {% for category, msg in messages %}
        <div class="flash {{ category }}">{{ msg }}</div>
      {% endfor %}
    {% endif %}
  {% endwith %}
  {% block content %}{% endblock %}
</div>
<script>
function toggleTheme(){
  let root=document.documentElement;
  let current=root.getAttribute('data-theme');
  let next=(current==='light')?'dark':'light';
  root.setAttribute('data-theme',next);
  localStorage.setItem('theme',next);
}
window.onload=function(){
  let saved=localStorage.getItem('theme');
  if(saved){ document.documentElement.setAttribute('data-theme',saved); }
}
</script>
</body>
</html>
""",

"register.html": """{% extends "base.html" %} {% block content %}
<div class="card">
<h2>Create Account</h2>
<form method="post">
    <input type="text" name="username" placeholder="Username" required>
    <input type="password" name="password" placeholder="Password" required>
    <select name="role" id="role_select" required onchange="toggleRefCode()">
        <option value="">-- Select Role --</option>
        <option value="admin">Admin</option>
        <option value="user">User</option>
    </select>
    <div id="refCodeField" style="display:none;">
        <input type="text" name="assigned_admin" placeholder="Enter Admin Reference Code">
    </div>
    <button type="submit">Register</button>
</form>
<p style='text-align:center; margin-top:1rem;'>Already have an account? <a href='{{ url_for('login') }}'>Login</a></p>
</div>
<script>
function toggleRefCode(){
    let role=document.getElementById("role_select").value;
    document.getElementById("refCodeField").style.display=(role==='user')?'block':'none';
}
</script>
{% endblock %}""",

"login.html": """{% extends "base.html" %} {% block content %}
<div class="card">
<h2>Login</h2>
<form method="post">
  <input type="text" name="username" placeholder="Username" required>
  <input type="password" name="password" placeholder="Password" required>
  <button type="submit">Login</button>
</form>
<p style='text-align:center; margin-top:1rem;'><a href="{{ url_for('register') }}">Register</a> | <a href="{{ url_for('forget_password') }}">Forget Password?</a></p>
</div>
{% endblock %}""",

"index.html": """{% extends "base.html" %} {% block content %}
<h2>Welcome {{ session['user']['username'] }}</h2>

{% if session['user']['role']=='admin' %}
<div class="card">
<p>Your reference code: <strong>{{ session['user']['ref_code'] }}</strong></p>
<form method="post" enctype="multipart/form-data">
  <input type="file" name="file" multiple required>
  <button type="submit">Upload Files</button>
</form>
</div>
{% endif %}

<div class="file-list">
  {% for f in files %}
  <div class="card file-card">
    <!-- Row 1: File Name -->
    <p><strong>{{ f[1] }}</strong></p>

    <!-- Row 2: Preview (No PDF preview) -->
    {% if f[1].endswith(('.png','.jpg','.jpeg','.gif')) %}
      <img src="{{ url_for('preview', file_id=f[0]) }}">
    {% elif f[1].endswith(('.mp4','.webm','.ogg')) %}
      <video controls>
        <source src="{{ url_for('preview', file_id=f[0]) }}" type="video/{{ f[1].split('.')[-1] }}">
      </video>
    {% elif f[1].endswith(('.mp3','.wav','.ogg')) %}
      <audio controls style="width:100%;">
        <source src="{{ url_for('preview', file_id=f[0]) }}" type="audio/{{ f[1].split('.')[-1] }}">
      </audio>
    {% endif %}

    <!-- Row 3: Download -->
    <a href="{{ url_for('download', file_id=f[0]) }}" download>
      <button class="action-btn download">Download</button>
    </a>

    <!-- Row 4: Delete (admin only) -->
    {% if session['user']['role']=='admin' %}
    <button class="action-btn delete" onclick="deleteFile({{ f[0] }}, this)">Delete</button>
    {% endif %}
  </div>
  {% endfor %}
</div>

<script>
function deleteFile(fileId, btn){
    if(!confirm("Are you sure you want to delete this file?")) return;
    fetch('/delete_ajax/' + fileId, {method:'POST'})
    .then(res => res.json())
    .then(data => {
        if(data.success){
            btn.closest('.file-card').remove();
        } else {
            alert("Failed to delete file.");
        }
    });
}
</script>
{% endblock %}""",

"forget.html": """{% extends "base.html" %} {% block content %}
<div class="card">
<h2>Forget Password</h2>
<form method="post">
    <input type="text" name="username" placeholder="Enter your username" required>
    <button type="submit">Next</button>
</form>
<p style='text-align:center; margin-top:1rem;'><a href="{{ url_for('login') }}">Back to Login</a></p>
</div>
{% endblock %}""",

"reset.html": """{% extends "base.html" %} {% block content %}
<div class="card">
<h2>Reset Password</h2>
<form method="post">
    <input type="password" name="password" placeholder="Enter new password" required>
    <button type="submit">Reset</button>
</form>
</div>
{% endblock %}"""
}

app.jinja_loader = DictLoader(TEMPLATES)

# ------------------- Routes -------------------
@app.route('/')
def home():
    if not session.get('user'): return redirect(url_for('login'))
    uid = session['user']['id']
    role = session['user']['role']
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        if role=='admin':
            c.execute("SELECT id,filename FROM files WHERE uploader_id=?", (uid,))
        else:
            admin_id = session['user']['assigned_admin']
            c.execute("SELECT id,filename FROM files WHERE uploader_id=?", (admin_id,))
        files = c.fetchall()
    return render_template('index.html', files=files)

@app.route('/', methods=['POST'])
def upload():
    if not session.get('user') or session['user']['role'] != 'admin':
        return redirect(url_for('login'))
    uploaded_files = request.files.getlist("file")
    count = 0
    with sqlite3.connect(DB_FILE) as conn:
        for f in uploaded_files:
            if f.filename:
                path = os.path.join(UPLOAD_FOLDER, f.filename)
                f.save(path)
                conn.execute("INSERT INTO files(filename,uploader_id) VALUES(?,?)", 
                             (f.filename, session['user']['id']))
                count +=1
        conn.commit()
    flash(f"{count} file(s) uploaded successfully!", "success")
    return redirect(url_for('home'))

@app.route('/download/<int:file_id>')
def download(file_id):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT filename FROM files WHERE id=?", (file_id,))
        row = c.fetchone()
    return send_from_directory(UPLOAD_FOLDER, row[0], as_attachment=True)

@app.route('/preview/<int:file_id>')
def preview(file_id):
    # Used for images, videos, audio previews (no forced download)
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT filename FROM files WHERE id=?", (file_id,))
        row = c.fetchone()
    return send_from_directory(UPLOAD_FOLDER, row[0])

@app.route('/delete_ajax/<int:file_id>', methods=['POST'])
def delete_file_ajax(file_id):
    if session['user']['role'] != 'admin': return {'success': False}
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT filename FROM files WHERE id=?", (file_id,))
        row = c.fetchone()
        if row: os.remove(os.path.join(UPLOAD_FOLDER, row[0]))
        c.execute("DELETE FROM files WHERE id=?", (file_id,))
        conn.commit()
    return {'success': True}

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']; password=request.form['password']
        with sqlite3.connect(DB_FILE) as conn:
            c=conn.cursor(); c.execute("SELECT * FROM users WHERE username=?",(username,))
            row=c.fetchone()
        if row and check_password_hash(row[2],password):
            session['user']={'id':row[0],'username':row[1],'role':row[3],'ref_code':row[4],'assigned_admin':row[5]}
            return redirect(url_for('home'))
        flash("Invalid credentials","danger")
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        u = request.form['username']; p = request.form['password']; role = request.form['role']
        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            if role=='admin':
                ref_code = generate_ref_code()
                try:
                    c.execute("INSERT INTO users(username,password,role,ref_code) VALUES(?,?,?,?)",
                              (u, generate_password_hash(p), role, ref_code))
                    conn.commit()
                    flash(f"Admin created! Reference code: {ref_code}", "success")
                    return redirect(url_for('login'))
                except sqlite3.IntegrityError:
                    flash("Username already exists!", "danger")
            else:
                assigned_ref = request.form.get('assigned_admin')
                c.execute("SELECT id FROM users WHERE ref_code=? AND role='admin'", (assigned_ref,))
                admin_row = c.fetchone()
                if not admin_row:
                    flash("Invalid Admin Reference Code", "danger")
                    return redirect(url_for('register'))
                try:
                    c.execute("INSERT INTO users(username,password,role,assigned_admin) VALUES(?,?,?,?)",
                              (u, generate_password_hash(p), role, admin_row[0]))
                    conn.commit()
                    flash("User created!", "success")
                    return redirect(url_for('login'))
                except sqlite3.IntegrityError:
                    flash("Username already exists!", "danger")
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))

@app.route('/forget', methods=['GET','POST'])
def forget_password():
    if request.method=='POST':
        username = request.form['username'].strip()
        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            c.execute("SELECT id FROM users WHERE username=?", (username,))
            user = c.fetchone()
        if user:
            session['reset_user'] = user[0]
            flash("Username found. Enter new password below.", "success")
            return redirect(url_for('reset_password'))
        else:
            flash("Username not found.", "danger")
    return render_template('forget.html')

@app.route('/reset', methods=['GET','POST'])
def reset_password():
    if 'reset_user' not in session: return redirect(url_for('forget_password'))
    if request.method=='POST':
        new_pass = request.form['password']
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("UPDATE users SET password=? WHERE id=?",
                         (generate_password_hash(new_pass), session['reset_user']))
            conn.commit()
        session.pop('reset_user')
        flash("Password updated! You can now login.", "success")
        return redirect(url_for('login'))
    return render_template('reset.html')

# ------------------- Launch Browser -------------------
def open_browser(ip):
    time.sleep(1)
    webbrowser.open(f"http://{ip}:5000")

if __name__=="__main__":
    local_ip = get_local_ip()
    threading.Thread(target=open_browser, args=(local_ip,)).start()
    app.run(host="0.0.0.0", port=5000, debug=True)
