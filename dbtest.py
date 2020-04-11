import sqlite3

connect = sqlite3.connect("database.sqlite")  # или :memory: чтобы сохранить в RAM
connect.cursor().execute("""SELECT * FROM items WHERE id=1""")
data = connect.cursor().fetchall()
print(data)