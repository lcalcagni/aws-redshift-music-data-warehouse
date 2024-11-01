import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Loads data from S3 into staging tables on Redshift.

    Parameters:
    - cur: Cursor object to execute database commands.
    - conn: Connection object to the database.

    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()
        print("done loading staging table: ", query)


def insert_tables(cur, conn):
    """
    Inserts data from staging tables into the final analytics tables on Redshift.

    Parameters:
    - cur: Cursor object to execute database commands.
    - conn: Connection object to the database.

    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()
        print("done insering in table: ", query)



def main():
    """
    - Establishes a connection to the Redshift database and obtains a cursor.
    - Loads data into the staging tables.
    - Inserts data into the final tables.
    - Closes the database connection.

    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()