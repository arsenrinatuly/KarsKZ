import sqlite3

user_id = input("")
conn = sqlite3.connect('post.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM post WHERE id = ?', (user_id,))
posts = cursor.fetchall()

for post in posts:
    print(post)