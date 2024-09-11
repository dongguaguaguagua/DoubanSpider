from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
import json
import sqlite3

def add_url_params(url, params):
    url_parts = list(urlparse(url))
    query = dict(parse_qs(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query, doseq=True)

    return urlunparse(url_parts)

def load_config():
    with open('config.json','r',encoding='utf8') as file:
        config = json.load(file)
    return config

def save_data(data, fileName):
    with open(fileName, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def get_total_movies_count(db_path):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM movies')
    total_count = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return total_count

def get_total_books_count(db_path):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM books')
    total_count = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return total_count

def init_book_table(db_path):
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

def init_movie_table(db_path):
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
