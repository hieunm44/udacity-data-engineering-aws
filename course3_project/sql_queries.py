import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = """DROP TABLE IF EXISTS "user"
                    """
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= """
    CREATE TABLE IF NOT EXISTS staging_events (
        artist TEXT,
        auth TEXT,
        firstName TEXT,
        gender TEXT,
        ItemInSession INT,
        lastName TEXT,
        length FLOAT,
        level TEXT,
        location TEXT,
        method TEXT,
        page TEXT,
        registration FLOAT,
        sessionId INT,
        song TEXT,
        status INT,
        ts BIGINT, 
        userAgent TEXT, 
        userId INT)
"""

staging_songs_table_create = """
    CREATE TABLE IF NOT EXISTS staging_songs (
        song_id TEXT,
        title TEXT,
        duration FLOAT,
        year INT,
        artist_id TEXT,
        artist_name TEXT,
        artist_latitude FLOAT,
        artist_longitude FLOAT,
        artist_location TEXT,
        num_songs INT,
        PRIMARY KEY (song_id)
        )
"""

songplay_table_create = """
    CREATE TABLE IF NOT EXISTS songplay (
        songplay_id INT,
        start_time  TIMESTAMP NOT NULL SORTKEY DISTKEY,
        user_id INT NOT NULL,
        level TEXT,
        song_id TEXT,
        artist_id TEXT,
        session_id INT,
        location TEXT,
        user_agent TEXT,
        PRIMARY KEY (songplay_id)
        )
"""

user_table_create = """
    CREATE TABLE IF NOT EXISTS "user" (
        user_id TEXT NOT NULL,
        first_name TEXT,
        last_name TEXT,
        gender TEXT,
        level TEXT,
        PRIMARY KEY (user_id)
        )
"""

song_table_create = """
    CREATE TABLE IF NOT EXISTS song (
        song_id TEXT NOT NULL,
        title TEXT,
        artist_id TEXT NOT NULL,
        year INT,
        duration FLOAT,
        PRIMARY KEY (song_id)
        )
"""

artist_table_create = """
    CREATE TABLE IF NOT EXISTS artist (
        artist_id TEXT NOT NULL,
        name TEXT,
        location TEXT,
        latitude FLOAT,
        longitude FLOAT,
        PRIMARY KEY (artist_id)
        )
"""

time_table_create = """
    CREATE TABLE IF NOT EXISTS time (
        start_time TIMESTAMP DISTKEY SORTKEY,
        hour INT,
        day INT,
        week INT,
        month INT,
        year INT,
        weekday INT,
        PRIMARY KEY (start_time)
        )
"""

# STAGING TABLES

staging_events_copy = """
    COPY staging_events from {}
                        iam_role {}
                        format as json {}
                        region 'us-west-2'
""".format(
    config['S3']['LOG_DATA'], 
    config['IAM_ROLE']['ARN'], 
    config['S3']['LOG_JSONPATH'])

staging_songs_copy = """
    COPY staging_songs from {}
                       iam_role {}
                       format as json 'auto'
                       region 'us-west-2'
""".format(
    config['S3']['SONG_DATA'],
    config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = """
    INSERT INTO songplay (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT TIMESTAMP 'epoch' + (e.ts / 1000) * INTERVAL '1 second' as start_time, 
        e.userId as user_id, 
        e.level as level, 
        s.song_id as song_id, 
        s.artist_id as artist_id, 
        e.sessionId as session_id, 
        e.location as location, 
        e.userAgent as user_agent
    FROM staging_events e
    JOIN staging_songs  s
    ON e.song = s.title 
    AND e.artist = s.artist_name 
    WHERE e.page = 'NextSong' 
    AND e.length = s.duration
"""

user_table_insert = """
    INSERT INTO user (user_id, first_name, last_name, gender, level)
    SELECT
        DISTINCT (userId) as user_id,
        firstName as first_name,
        lastName as last_name,
        gender,
        level
    FROM staging_events
    WHERE userId is NOT NULL
    AND page = 'NextSong'
"""

song_table_insert = """
    INSERT INTO songs 
    SELECT 
        DISTINCT (song_id) as song_id,
        title,
        artist_id,
        year,
        duration
    FROM staging_songs
"""

artist_table_insert = """
    INSERT INTO artists 
    SELECT 
        DISTINCT (artist_id) as artist_id,
        artist_name,
        artist_location,
        artist_latitude,
        artist_longitude
    FROM staging_songs
"""

time_table_insert = """
    INSERT INTO time
        WITH temp_time AS (SELECT TIMESTAMP 'epoch' + (ts/1000 * INTERVAL '1 second') as start_time FROM staging_events)
        SELECT DISTINCT start_time,
        extract(hour from start_time),
        extract(day from start_time),
        extract(week from start_time),
        extract(month from start_time),
        extract(year from start_time),
        extract(weekday from start_time)
        FROM temp_time
"""

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
