import sqlite3

con = sqlite3.connect('sample.db')
cur = con.cursor()

#sql = 'create table fruits(name text,prince text);'
# cur.execute(sql)
'''
sql = 'select * from fruits'
sql = "insert into fruits values('apple','100yen')"
cur.executemany("insert into fruits values(?,?)", [
                ('orange', '150yen'), ('banana', '2')])
con.commit()
'''
sql = 'select * from fruits'
cur.execute(sql)
for row in cur:
    print(row)

con.close()
