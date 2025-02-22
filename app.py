import sqlite3
import os
from flask import (
    Flask,
    render_template,
    redirect,
    request,
    url_for,
    session
)



app = Flask(__name__)
app.secret_key = 'naggets123'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])



@app.route('/', methods=['GET','POST'])
def get_main():
        conn = sqlite3.connect('post.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM post')
        publick: list = cursor.fetchall()
        conn.close()
        return render_template('base.html', publick = publick)


@app.route('/profile', methods=['GET','POST'])
def get_profile():
    login = session.get('login', "Guest")
    return render_template('profile.html', login = login)


@app.route('/create_post', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title', type=str)
        description = request.form.get('description', type=str)
        price = request.form.get('price', type=int)
        image_filename = None   
        image_path = None  

        image_file = request.files.get('path_photo')
        if image_file and image_file.filename:
            image_filename = image_file.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(image_path)
            print("Имя файла:", image_filename)
            print("Путь к файлу:", image_path)
            print("Файл существует?", os.path.exists(image_path))
        else:
            print("Файл не выбран или отсутствует имя файла")

        conn = sqlite3.connect('post.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO post (title, description, price, path_photo) VALUES (?, ?, ?, ?)', (title,description,price, image_filename))
        conn.commit()
        conn.close()
        return redirect(url_for('get_main'))
    return render_template('create_post.html')


@app.route('/log', methods=['GET', 'POST'])
def get_log():
    if request.method == 'POST':
        login = request.form.get('login', type=str)
        password = request.form.get('password', type=str)
        session['login'] = request.form.get('login')
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE login = ? AND password = ?', (login, password))
        user = cursor.fetchone()  
        if user:
            return redirect(url_for('get_main'))
        else:
            error_message = "Неверный логин или пароль"
            return render_template('log.html', error=error_message)

        conn.close()

    return render_template('log.html')





@app.route('/reg', methods=['GET','POST'])
def get_reg():
    if request.method == 'POST':
        login = request.form.get('login', type=str)
        email = request.form.get('email', type=str)
        password = request.form.get('password', type=str)
        session['login'] = request.form.get('login')
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO users (login, email, password) VALUES (?, ?, ?)', (login, email, password))
        conn.commit()
        conn.close()
        return redirect(url_for('get_main'))

    return render_template('reg.html')




if __name__ == '__main__':
    app.run(debug=True)
