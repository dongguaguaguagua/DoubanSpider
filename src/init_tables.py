import sqlite3

def init_doulists_table(db_path):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doulists (
            id TEXT PRIMARY KEY,
            title TEXT,
            cover_url TEXT,
            sharing_url TEXT,
            url TEXT,
            items_count INTEGER,
            followers_count INTEGER,
            owner_id TEXT,
            owner_uid TEXT,
            update_time TEXT
        )
        ''')
    conn.commit()
    conn.close()

def init_books_table(db_path):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id TEXT PRIMARY KEY,
            title TEXT,
            rating REAL,
            rating_count INTEGER,
            pubdate TEXT,
            pages INTEGER,
            cover_url TEXT,
            sharing_url TEXT,
            url TEXT,
            author TEXT,
            card_subtitle TEXT,
            book_subtitle TEXT,
            press TEXT,
            update_time TEXT
        )
        ''')
    conn.commit()
    conn.close()

def init_interests_table(db_path):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interests (
            id TEXT PRIMARY KEY,
            comment TEXT,
            rating REAL,
            sharing_url TEXT,
            create_time TEXT,
            user_id TEXT,
            user_gender TEXT,
            user_name TEXT,
            update_time TEXT
        )
        ''')
    conn.commit()
    conn.close()

def init_movies_table(db_path):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id TEXT PRIMARY KEY,
            title TEXT,
            rating REAL,
            rating_count INTEGER,
            pubdate TEXT,
            year TEXT,
            genres TEXT,
            durations TEXT,
            cover_url TEXT,
            sharing_url TEXT,
            countries TEXT,
            url TEXT,
            directors TEXT,
            actors TEXT,
            update_time TEXT
        )
        ''')
    conn.commit()
    conn.close()
