import csv

with open('data/datav1.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')
    for row in spamreader:
        print(' TEST DELIMETER '.join(row))
