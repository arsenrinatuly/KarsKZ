from flask import Flask, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Секретный ключ для сессий

# Функция для подключения к базе данных SQLite
def get_db_connection():
    conn = sqlite3.connect('users.db')  # Создаем или открываем базу данных
    conn.row_factory = sqlite3.Row  # Позволяет обращаться к колонкам по имени
    return conn

# Инициализация базы данных (если она еще не создана)
def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    conn.commit()
    conn.close()

init_db()

# Главная страница
@app.route('/')
def index():
    if 'username' in session:
        return f'Hello, {session["username"]}!'
    return 'Hello, Guest! <a href="/login">Login</a>'

# Страница логина
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid credentials. <a href="/login">Try again</a>'

    return '''
        <form method="post">
            Username: <input type="text" name="username">
            Password: <input type="password" name="password">
            <input type="submit" value="Login">
        </form>
    '''

# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()

        return 'Registration successful! <a href="/login">Login</a>'

    return '''
        <form method="post">
            Username: <input type="text" name="username">
            Password: <input type="password" name="password">
            <input type="submit" value="Register">
        </form>
    '''

# Страница выхода
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
