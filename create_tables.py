import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drops each table specified in the 'drop_table_queries' list.
    
    Parameters:
    - cur: Cursor object to execute database commands.
    - conn: Connection object to the database.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates each table specified in the 'create_table_queries' list.
    
    Parameters:
    - cur: Cursor object to execute database commands.
    - conn: Connection object to the database.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Reads the configuration file 'dwh.cfg' to get database connection parameters.
    - Establishes a connection to the Redshift database and obtains a cursor.
    - Drops existing tables if they exist.
    - Creates new tables as defined in the SQL queries.
    - Closes the database connection.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()