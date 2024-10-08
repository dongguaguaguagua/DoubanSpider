import sqlite3
from datetime import datetime

def insert_books(db_path, data):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # 插入数据
    for subject in data.get('subjects', {}):
        id = subject.get('id')
        title = subject.get('title')
        rating = subject.get('rating', {}).get('value') if subject.get('rating') else None
        rating_count = subject.get('rating', {}).get('count') if subject.get('rating') else None
        pubdate = ', '.join(subject.get('pubdate', []))
        pages = ', '.join(subject.get('pages', []))
        cover_url = subject.get('cover_url')
        sharing_url = subject.get('sharing_url')
        url = subject.get('url')
        author = ', '.join(subject.get('author', []))
        card_subtitle = subject.get('card_subtitle')
        book_subtitle = subject.get('book_subtitle')
        press = ', '.join(subject.get('press', []))
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        is_visited = 0

        # 先插入一行数据，设置 is_visited = 0 ,然后如果插入的id冲突
        # 就表示已经存在过，那么不要更改 is_visited 的值，其余都更改一遍。
        cursor.execute('''
        INSERT INTO books (id, title, rating, rating_count, pubdate, pages, cover_url, sharing_url, url, author, card_subtitle, book_subtitle, press, is_visited, update_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (id)
        DO UPDATE SET
            title = excluded.title,
            rating = excluded.rating,
            rating_count = excluded.rating_count,
            pubdate = excluded.pubdate,
            pages = excluded.pages,
            cover_url = excluded.cover_url,
            sharing_url = excluded.sharing_url,
            url = excluded.url,
            author = excluded.author,
            card_subtitle = excluded.card_subtitle,
            book_subtitle = excluded.book_subtitle,
            press = excluded.press,
            update_time = excluded.update_time;
        ''', (id, title, rating, rating_count, pubdate, pages, cover_url, sharing_url, url, author, card_subtitle, book_subtitle, press, is_visited, update_time))

    conn.commit()
    conn.close()


def insert_small_books(db_path, data):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    for subject in data.get('subjects', {}):
        id = subject.get('id')
        title = subject.get('title')
        rating = subject.get('rating', {}).get('value') if subject.get('rating') else None
        rating_count = subject.get('rating', {}).get('count') if subject.get('rating') else None
        url = subject.get('url')
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        is_visited = 0

        cursor.execute('''
        INSERT INTO books (id, title, rating, rating_count, url, is_visited, update_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (id)
        DO UPDATE SET
            title = excluded.title,
            rating = excluded.rating,
            rating_count = excluded.rating_count,
            url = excluded.url,
            update_time = excluded.update_time;
        ''', (id, title, rating, rating_count, url, is_visited, update_time))

    conn.commit()
    conn.close()

def insert_movies(db_path, data):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # 插入数据
    for subject in data.get('subjects', {}):
        id = subject.get('id')
        title = subject.get('title')
        rating = subject.get('rating', {}).get('value') if subject.get('rating') else None
        rating_count = subject.get('rating', {}).get('count') if subject.get('rating') else None
        pubdate = ', '.join(subject.get('pubdate', []))
        year = subject.get('year')
        genres = ', '.join(subject.get('genres', []))
        durations = ', '.join(subject.get('durations', []))
        cover_url = subject.get('cover_url')
        sharing_url = subject.get('sharing_url')
        countries = ', '.join(subject.get('countries', []))
        url = subject.get('url')
        directors = ', '.join([director.get('name') for director in subject.get('directors', [])])
        actors = ', '.join([actor.get('name') for actor in subject.get('actors', [])])
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        is_visited = 0

        cursor.execute('''
        INSERT INTO movies (id, title, rating, rating_count, pubdate, year, genres, durations, cover_url, sharing_url, countries, url, directors, actors, is_visited, update_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (id)
        DO UPDATE SET
            title = excluded.title,
            rating = excluded.rating,
            rating_count = excluded.rating_count,
            pubdate = excluded.pubdate,
            year = excluded.year,
            genres = excluded.genres,
            durations = excluded.durations,
            cover_url = excluded.cover_url,
            sharing_url = excluded.sharing_url,
            countries = excluded.countries,
            url = excluded.url,
            directors = excluded.directors,
            actors = excluded.actors,
            update_time = excluded.update_time;
        ''', (id, title, rating, rating_count, pubdate, year, genres, durations, cover_url, sharing_url, countries, url, directors, actors, is_visited, update_time))

    conn.commit()
    conn.close()

def insert_doulists(db_path, data):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    for subject in data.get('doulists', {}):
        id = subject.get('id')
        title = subject.get('title')
        cover_url = subject.get('cover_url')
        sharing_url = subject.get('sharing_url')
        url = subject.get('url')
        items_count = subject.get('items_count')
        followers_count = subject.get('followers_count')
        owner_id = subject.get('owner', {}).get('id') if subject.get('owner') else None
        owner_uid = subject.get('owner', {}).get('uid') if subject.get('owner') else None
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        is_visited = 0

        cursor.execute('''
        INSERT INTO doulists (id, title, cover_url, sharing_url, url, items_count, followers_count, owner_id, owner_uid, is_visited, update_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (id)
        DO UPDATE SET
            title = excluded.title,
            cover_url = excluded.cover_url,
            sharing_url = excluded.sharing_url,
            url = excluded.url,
            items_count = excluded.items_count,
            followers_count = excluded.followers_count,
            owner_id = excluded.owner_id,
            owner_uid = excluded.owner_uid,
            update_time = excluded.update_time;
        ''', (id, title, cover_url, sharing_url, url, items_count, followers_count, owner_id, owner_uid, is_visited, update_time))

    conn.commit()
    conn.close()


def insert_interests(db_path, data):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    for subject in data.get('interests', {}):
        id = subject.get('id')
        comment = subject.get('comment')
        rating = subject.get('rating', {}).get('value') if subject.get('rating') else None
        sharing_url = subject.get('sharing_url')
        create_time = subject.get('create_time')
        user_id = subject.get('user', {}).get('id') if subject.get('user') else None
        user_gender = subject.get('user', {}).get('gender') if subject.get('user') else None
        user_name = subject.get('user', {}).get('name') if subject.get('user') else None
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        is_visited = check_user_exists(db_path, user_id)

        cursor.execute('''
        INSERT INTO interests (id, comment, rating, sharing_url, create_time, user_id, user_gender, user_name, is_visited, update_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (id)
        DO UPDATE SET
            comment = excluded.comment,
            rating = excluded.rating,
            sharing_url = excluded.sharing_url,
            create_time = excluded.create_time,
            user_id = excluded.user_id,
            user_gender = excluded.user_gender,
            user_name = excluded.user_name,
            update_time = excluded.update_time;
        ''', (id, comment, rating, sharing_url, create_time, user_id, user_gender, user_name, is_visited, update_time))

    conn.commit()
    conn.close()

def check_user_exists(db_path, user_id):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM interests WHERE user_id = ?", (user_id,))
    user_exists = cursor.fetchone()[0] > 0
    conn.commit()
    conn.close()

    if user_exists:
        return 1
    return 0
