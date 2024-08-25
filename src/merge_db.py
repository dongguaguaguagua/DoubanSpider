import sqlite3

# 连接到两个源数据库
conn = sqlite3.connect('movies3.db')

# 连接到目标数据库
conn_merged = sqlite3.connect('merged.db')

# 创建游标对象
cur1 = conn.cursor()
cur_merged = conn_merged.cursor()

# 创建目标数据库的movie表结构
cur_merged.execute('''
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
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

# 从第一个数据库中插入数据
cur1.execute('SELECT * FROM movies')
rows1 = cur1.fetchall()
cur_merged.executemany('''
INSERT INTO movies (id, title, rating, rating_count, pubdate, year, genres, durations, cover_url,
                   sharing_url, countries, url, directors, actors, update_time)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(id) DO UPDATE SET
    title=excluded.title,
    rating=excluded.rating,
    rating_count=excluded.rating_count,
    pubdate=excluded.pubdate,
    year=excluded.year,
    genres=excluded.genres,
    durations=excluded.durations,
    cover_url=excluded.cover_url,
    sharing_url=excluded.sharing_url,
    countries=excluded.countries,
    url=excluded.url,
    directors=excluded.directors,
    actors=excluded.actors,
    update_time=excluded.update_time
WHERE excluded.update_time > movies.update_time
''', rows1)


# 提交更改并关闭连接
conn_merged.commit()
conn.close()
conn_merged.close()
