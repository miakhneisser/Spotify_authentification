import psycopg2
from config import get_configuration
from typing import Dict, List
from datetime import date, datetime, timedelta


class PostgreSQLArtistsRepository(object):
    def __init__(self, postgresql_settings: Dict):
        self.conn = psycopg2.connect(host = postgresql_settings['host'], database = postgresql_settings['database'], user = postgresql_settings['user'], port = postgresql_settings['port'], password = postgresql_settings['password'])
        self.cur = self.conn.cursor()
        self.create_artist()
        self.create_new_releases_artist()
        self.create_new_releases()

    def create_artist(self) -> None:
        print('-------CREATE ARTIST TABLE----------')
        """ Connect to the PostgreSQL database server """
        try:
            self.cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables where table_name=%s)", ('artists',))
            if (self.cur.fetchone()[0] == True):
                print('TABLE ARTISTS ALREADY EXISTS')
                return

    	    # execute a statement
            add_table_query = """CREATE TABLE artists (
                                id_artist VARCHAR(50) NOT NULL PRIMARY KEY,
                                artists.name VARCHAR(50) NOT NULL,
                                artists.href_api VARCHAR(150) NOT NULL,
                                artists.href_spotify VARCHAR(150) NOT NULL,
                                artists.type VARCHAR(20) NOT NULL,
                                artists.uri VARCHAR(150) NOT NULL );"""
            self.cur.execute(add_table_query)
            self.conn.commit()

            #self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_new_releases_artist(self) -> None:
        print('-------CREATE NEW RELEASES ARTIST TABLE----------')
        """ Connect to the PostgreSQL database server """
        try:
            self.cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables where table_name=%s)", ('new_releases_artist',))
            if (self.cur.fetchone()[0] == True):
                print('TABLE NEW RELEASES ARTIST ALREADY EXISTS')
                return
    	    # execute a statement
            add_table_query = """CREATE TABLE new_releases_artist (
                                id_new_releases VARCHAR(50) NOT NULL,
                                id_artist VARCHAR(50) NOT NULL,
                                PRIMARY KEY (id_new_releases, id_artist) );"""
            self.cur.execute(add_table_query)
            self.conn.commit()

            #self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_new_releases(self) -> None:
        print('-------CREATE New Releases TABLE----------')
        """ Connect to the PostgreSQL database server """
        try:
            self.cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables where table_name=%s)", ('new_releases',))
            if (self.cur.fetchone()[0] == True):
                print('TABLE New Releases ALREADY EXISTS')
                return

    	    # execute a statement
            add_table_query = """CREATE TABLE new_releases (
                                id_new_releases VARCHAR(50) NOT NULL PRIMARY KEY,
                                album_type VARCHAR(20) NOT NULL,
                                available_markets VARCHAR(350) NOT NULL,
                                href_api VARCHAR(150) NOT NULL,
                                href_spotify VARCHAR(150) NOT NULL,
                                name VARCHAR(150) NOT NULL,
                                release_date DATE NOT NULL,
                                type VARCHAR(50) NOT NULL,
                                uri VARCHAR(150) NOT NULL );"""
            self.cur.execute(add_table_query)
            self.conn.commit()

            #self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def add_artist(self, artists: List) -> None:
        print('-------ADD ARTISTSSSSS----------')
        """ Connect to the PostgreSQL database server """
        for artist in artists:
            try:
                self.cur.execute("SELECT * FROM artists WHERE id_artist = %s", (artist['id'],))
                if (self.cur.fetchone() is not None):
                    print('id already exists')
                    continue

        	    # execute a statement
                insert_query = """INSERT INTO artists (id_artist, name, href_api, href_spotify, type, uri) VALUES (%s, %s, %s, %s, %s, %s)"""
                self.cur.execute(insert_query, (artist['id'], artist['name'], artist['href'], artist['external_urls']['spotify'], artist['type'], artist['uri']))
                self.conn.commit()

                #self.cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

    def add_new_releases(self, new_releases: List) -> None:
        print('-------ADD NEW RELEASES----------')
        """ Connect to the PostgreSQL database server """
        for new_release in new_releases:
            try:
                self.cur.execute("SELECT * FROM new_releases WHERE id_new_releases = %s", (new_release['id_new_releases'],))
                if (self.cur.fetchone() is not None):
                    print('id already exists')
                    continue

        	    # execute a statement
                insert_query = """INSERT INTO new_releases (id_new_releases, album_type, available_markets, href_api, href_spotify, name, release_date, type, uri) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                self.cur.execute(insert_query, (new_release['id_new_releases'], new_release['album_type'], new_release['available_markets'], new_release['href_api'], new_release['href_spotify'], new_release['name'], new_release['release_date'], new_release['type'], new_release['uri']))
                self.conn.commit()

                new_release_artists = [{'id_new_releases': new_release['id_new_releases'], 'id_artist': artist['id']} for artist in new_release['artists']]
                self.add_new_releases_artists(new_release_artists)
                self.add_artist(new_release['artists'])

                #self.cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

    def add_new_releases_artists(self, new_releases_artists: List) -> None:
        print('-------ADD ARTISTSSSSS----------')
        """ Connect to the PostgreSQL database server """
        for new_release_artist in new_releases_artists:
            try:
                self.cur.execute("SELECT * FROM new_releases_artist WHERE id_new_releases = %s AND id_artist =%s", (new_release_artist['id_new_releases'], new_release_artist['id_artist']))
                if (self.cur.fetchone() is not None):
                    print('primary key (id_new_releases, id_artist) already exists')
                    continue

        	    # execute a statement
                insert_query = """INSERT INTO new_releases_artist (id_new_releases, id_artist) VALUES (%s, %s)"""
                self.cur.execute(insert_query, (new_release_artist['id_new_releases'], new_release_artist['id_artist']))
                self.conn.commit()

                #self.cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

    def get_artists_new_releases(self) -> List:
        today = date.today().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")

        select_query = "SELECT artists.id_artist, artists.name, artists.href_api, artists.href_spotify, artists.type, artists.uri FROM (SELECT releases.id_new_releases, new_releases_artist.id_artist FROM (SELECT * FROM new_releases WHERE release_date = %(date)s) AS releases LEFT JOIN new_releases_artist ON releases.id_new_releases = new_releases_artist.id_new_releases) AS selected_artists LEFT JOIN artists ON artists.id_artist = selected_artists.id_artist;"
        self.cur.execute(select_query, {'date': '2020-10-22'})
        artists = self.cur.fetchall()
        return {artist[0]: {'id_artist': artist[0], 'name': artist[1], 'href_api': artist[2], 'href_spotify': artist[3], 'type': artist[4], 'uri': artist[5]} for artist in  artists}
