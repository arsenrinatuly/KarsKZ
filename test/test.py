import sqlite3

conn = sqlite3.connect('post.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM post')
posts = cursor.fetchall() 

for i in posts:
    print(i)