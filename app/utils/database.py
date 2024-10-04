import sqlite3


def get_connection():
    return sqlite3.connect('database.db')

async def create_db():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL UNIQUE,
            assistant_id TEXT NOT NULL,
            thread_id TEXT NOT NULL
        )
    ''')
    con.commit()
    con.close()
    
    
async def insert_user(phone, assistant_id, thread_id):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute('''
        INSERT INTO users (phone, assistant_id, thread_id) 
        VALUES (?, ?, ?)
    ''', (phone, assistant_id, thread_id))
    con.commit()
    con.close()
    

async def get_user(phone):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE phone = ?
    ''', (phone,))
    user = cursor.fetchone()
    con.close()
    
    return user