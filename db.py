import sqlite3
con = sqlite3.connect('scam.db')
cursor = con.cursor()
def CreateDB():
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, id INT, phone INT)")
    con.commit()
def AddUser(name, id):
    cursor.execute(f'INSERT INTO users VALUES ("{name}", {id}, 0)')
    con.commit()
def AddNumber(number, id):
    cursor.execute(f"UPDATE users SET phone={number} where id={id}")
    con.commit()