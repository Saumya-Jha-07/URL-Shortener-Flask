import sqlite3

DB_NAME = "url_db.db"


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
                CREATE TABLE IF NOT EXISTS  urls (
                   id INTEGER  PRIMARY KEY AUTOINCREMENT , 
                   original_url TEXT NOT NULL ,
                   shorten_url TEXT NOT NULL ,
                   visit_count INTEGER DEFAULT 0   
                   )
        ''')

def insert_url(full_url , short_code):
    
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
                INSERT INTO urls (original_url , shorten_url)
                     VALUES (?,?)
        ''' , (full_url,short_code))

def get_url(short_code):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.execute('''
                SELECT * FROM urls 
                     WHERE shorten_url = ? 
        ''' , (short_code, ))
        return cur.fetchone()

def increment_visit_count(short_code):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
                UPDATE urls 
                     SET visit_count = visit_count + 1
                    WHERE shorten_url = ?
        ''' , (short_code, ) )

def get_all_urls():
    with sqlite3.connect(DB_NAME) as conn:
        curr = conn.execute('''
                SELECT original_url , shorten_url , visit_count FROM urls
                            ORDER BY id DESC
        ''')
        return curr.fetchall()

def delete_url(short_code):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
                DELETE FROM urls 
                     WHERE shorten_url = ?
        ''' , (short_code , ))