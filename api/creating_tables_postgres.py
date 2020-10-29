import psycopg2
import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)))))

from config import get_configuration

def create_tables():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host = "localhost", database = "spotify", user = "postgres", password = "postgres", port = "5432")
        cur = conn.cursor()

        table_artists = """ CREATE TABLE artistss (
                                        id VARCHAR(50) NOT NULL PRIMARY KEY,
                                        name VARCHAR(50) NOT NULL,
                                        href_api VARCHAR(150) NOT NULL,
                                        href_spotify VARCHAR(150) NOT NULL,
                                        type VARCHAR(20) NOT NULL,
                                        uri VARCHAR(150) NOT NULL ); """
        table_new_releases = """ """
        table_new_releases_artists = """ """

        cur.execute(table_artists)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    create_tables()
