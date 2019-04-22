# COUNTING ORGANIZATIONS
# This application will read the mailbox data (mbox.txt) and count the number of email messages per organization 
# (i.e. domain name of the email address) using a database with the following schema to maintain the counts.

import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('''CREATE TABLE COUNTS(org TEXT, count INTEGER)''')
fname = input('Enter file name: ')
if len(fname) < 1 : fname = 'mbox.txt'
fhandle = open(fname)
for line in fhandle:
    if not line.startswith('From ') : continue
    pieces = line.split()
    email = pieces[1].split('@')
    org = email[1]
    cur.execute('SELECT count from Counts WHERE org = ?', (org,))
    row = cur.fetchone()
    if row is None:
        cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (org,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (org,))
    conn.commit()

sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(row[0], row[1])

cur.close()