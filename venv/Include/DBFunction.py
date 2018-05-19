import sqlite3

def addUser(id,name,password):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('insert into user (id, name,password) values (?,?,?)', (id, name, password))
    cursor.rowcount
    print "Operation done successfully"
    cursor.close()
    conn.commit()
    conn.close()

def deleUser(id):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('delete from user where id=?', (id,))
    cursor.close()
    conn.commit()
    conn.close()

def modUser(id, name, password):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('update user set name=? , password=? where id=?', (name, password, id))
    cursor.close()
    conn.commit()
    conn.close()

def seleUser(id):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('select * from user where id=?', (id,))
    values = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return values