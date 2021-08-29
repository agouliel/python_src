import sqlite3
import datetime

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("create table test(d date, ts timestamp)")

today = datetime.date.today()
now = datetime.datetime.now()

cur.execute("insert into test(d, ts) values (?, ?)", (today, now))
cur.execute("select d, ts from test")
row = cur.fetchone()
print (row[0], type(row[0]))
print (row[1], type(row[1]))
print(cur.description)

cur.execute('select current_date as "d [date]", current_timestamp as "ts [timestamp]"')
row = cur.fetchone()
print (row[0], type(row[0]))
print (row[1], type(row[1]))
print(cur.description)

con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cur = con.cursor()
cur.execute("create table test(d date, ts timestamp)")

today = datetime.date.today()
now = datetime.datetime.now()

cur.execute("insert into test(d, ts) values (?, ?)", (today, now))
cur.execute("select d, ts from test")
row = cur.fetchone()
print (row[0], type(row[0]))
print (row[1], type(row[1]))
print(cur.description)

cur.execute('select current_date as "d [date]", current_timestamp as "ts [timestamp]"')
row = cur.fetchone()
print (row[0], type(row[0]))
print (row[1], type(row[1]))
print(cur.description)

