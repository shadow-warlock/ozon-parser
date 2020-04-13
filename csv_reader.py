import csv
import sqlite3

with open('data/datav1.csv') as csvfile, open('data/final.csv', 'w') as out:
    reader = csv.reader(csvfile, delimiter=';')
    writer = csv.writer(out, delimiter=';')
    ids = []
    for row in reader:
        if row[0].split(",")[0] not in ids:
            writer.writerow(row)
            ids.append(row[0].split(",")[0])
        else:
            print("copy")
    connect = sqlite3.connect("database.sqlite")  # или :memory: чтобы сохранить в RAM
    data = connect.cursor().execute("""SELECT * FROM items WHERE data like '%Телевизор%' and id not in (""" + ",".join(ids) + """)""").fetchall()
    unloader = list(map(lambda x:x[0], data))
    print(unloader)
    print(len(unloader))
    connect.close()