import sqlite3

connect = sqlite3.connect("database.sqlite")  # или :memory: чтобы сохранить в RAM
data = connect.cursor().execute("""SELECT * FROM items""").fetchall()
print(data[0][1])
