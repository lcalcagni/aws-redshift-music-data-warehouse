import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS fact_songplays;"
user_table_drop = "DROP TABLE IF EXISTS dim_users;"
song_table_drop = "DROP TABLE IF EXISTS dim_songs;"
artist_table_drop = "DROP TABLE IF EXISTS dim_artists;"
time_table_drop = "DROP TABLE IF EXISTS dim_time;"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events (
    artist          VARCHAR,
    auth            VARCHAR,
    firstName       VARCHAR,
    gender          CHAR(1),
    itemInSession   INTEGER,
    lastName        VARCHAR,
    length          FLOAT,
    level           VARCHAR,
    location        VARCHAR,
    method          VARCHAR,
    page            VARCHAR,
    registration    BIGINT,
    sessionId       INTEGER SORTKEY DISTKEY,
    song            VARCHAR,
    status          INTEGER,
    ts              BIGINT,
    userAgent       VARCHAR,
    userId          INTEGER
);
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
    num_songs           INTEGER,
    artist_id           VARCHAR,
    artist_latitude     FLOAT,
    artist_longitude    FLOAT,
    artist_location     VARCHAR,
    artist_name         VARCHAR,
    song_id             VARCHAR,
    title               VARCHAR,
    duration            FLOAT,
    year                INTEGER
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS fact_songplays (
    songplay_id     INTEGER IDENTITY(0,1) PRIMARY KEY,
    start_time      TIMESTAMP NOT NULL SORTKEY,
    user_id         INTEGER NOT NULL DISTKEY,
    level           VARCHAR,
    song_id         VARCHAR,
    artist_id       VARCHAR,
    session_id      INTEGER,
    location        VARCHAR,
    user_agent      VARCHAR
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_users (
    user_id         INTEGER PRIMARY KEY SORTKEY,
    first_name      VARCHAR,
    last_name       VARCHAR,
    gender          CHAR(1),
    level           VARCHAR
) DISTSTYLE ALL;
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_songs (
    song_id         VARCHAR PRIMARY KEY SORTKEY,
    title           VARCHAR,
    artist_id       VARCHAR,
    year            INTEGER,
    duration        FLOAT
) DISTSTYLE ALL;
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_artists (
    artist_id       VARCHAR PRIMARY KEY SORTKEY,
    name            VARCHAR,
    location        VARCHAR,
    latitude        FLOAT,
    longitude       FLOAT
) DISTSTYLE ALL;
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_time (
    start_time      TIMESTAMP PRIMARY KEY SORTKEY,
    hour            INTEGER,
    day             INTEGER,
    week            INTEGER,
    month           INTEGER,
    year            INTEGER,
    weekday         VARCHAR
) DISTSTYLE ALL;
""")

# STAGING TABLES

staging_events_copy = ("""
COPY staging_events FROM {}
IAM_ROLE {}
REGION 'us-west-2'
FORMAT AS JSON {};
""").format(config.get('S3', 'LOG_DATA'),
            config.get('IAM_ROLE', 'ARN'),
            config.get('S3', 'LOG_JSONPATH'))

staging_songs_copy = ("""
COPY staging_songs FROM {}
IAM_ROLE {}
REGION 'us-west-2'
FORMAT AS JSON 'auto';
""").format(config.get('S3', 'SONG_DATA'),
            config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO fact_songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT DISTINCT
    TIMESTAMP 'epoch' + se.ts/1000 * INTERVAL '1 second'   AS start_time,
    se.userId       AS user_id,
    se.level        AS level,
    ss.song_id      AS song_id,
    ss.artist_id    AS artist_id,
    se.sessionId    AS session_id,
    se.location     AS location,
    se.userAgent    AS user_agent
FROM staging_events se
LEFT JOIN staging_songs ss
    ON se.song = ss.title AND se.artist = ss.artist_name
WHERE se.page = 'NextSong';
""")

user_table_insert = ("""
INSERT INTO dim_users (user_id, first_name, last_name, gender, level)
SELECT DISTINCT
    se.userId       AS user_id,
    se.firstName    AS first_name,
    se.lastName     AS last_name,
    se.gender       AS gender,
    se.level        AS level
FROM staging_events se
WHERE se.userId IS NOT NULL;
""")

song_table_insert = ("""
INSERT INTO dim_songs (song_id, title, artist_id, year, duration)
SELECT DISTINCT
    ss.song_id      AS song_id,
    ss.title        AS title,
    ss.artist_id    AS artist_id,
    ss.year         AS year,
    ss.duration     AS duration
FROM staging_songs ss
WHERE ss.song_id IS NOT NULL;
""")

artist_table_insert = ("""
INSERT INTO dim_artists (artist_id, name, location, latitude, longitude)
SELECT DISTINCT
    ss.artist_id            AS artist_id,
    ss.artist_name          AS name,
    ss.artist_location      AS location,
    ss.artist_latitude      AS latitude,
    ss.artist_longitude     AS longitude
FROM staging_songs ss
WHERE ss.artist_id IS NOT NULL;
""")

time_table_insert = ("""
INSERT INTO dim_time (start_time, hour, day, week, month, year, weekday)
SELECT DISTINCT
    sp.start_time                           AS start_time,
    EXTRACT(hour FROM sp.start_time)        AS hour,
    EXTRACT(day FROM sp.start_time)         AS day,
    EXTRACT(week FROM sp.start_time)        AS week,
    EXTRACT(month FROM sp.start_time)       AS month,
    EXTRACT(year FROM sp.start_time)        AS year,
    EXTRACT(weekday FROM sp.start_time)     AS weekday
FROM fact_songplays sp;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, artist_table_create, song_table_create, time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, user_table_drop, artist_table_drop, song_table_drop, time_table_drop, songplay_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [user_table_insert, song_table_insert, artist_table_insert, songplay_table_insert, time_table_insert]
