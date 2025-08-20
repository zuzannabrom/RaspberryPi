from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'zuziabrom'  # Change this to a secret key of your choice

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Route to display the index page
@app.route('/')
def home():
    username = session.get('username')
    return render_template('index.html', username=username)

# Route to login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['username'] = username
            return redirect(url_for('home'))
        return 'Invalid login credentials. Try again.'
    return render_template('login.html')

# Route to register a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email=?', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return '''
                <script>
                    alert("E-mail jest już zajęty. Wybierz inny.");
                    window.location.href = "/register";
                </script>
            '''

        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

# Route to logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# === Nowe trasy ===

@app.route('/nauczyciel_wokalny')
def nauczyciel_wokalny():
    username = session.get('username')
    return render_template('nauczyciel_wokalny.html', username=username)

@app.route('/o_projekcie')
def o_projekcie():
    username = session.get('username')
    return render_template('o_projekcie.html', username=username)

@app.route('/kontakt')
def kontakt():
    username = session.get('username')
    return render_template('kontakt.html', username=username)

@app.route('/omnie')
def omnie():
    username = session.get('username')
    return render_template('omnie.html', username=username)

@app.route('/skala')
def skala():
    username = session.get('username')
    return render_template('skala.html', username=username)

# ===================

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
