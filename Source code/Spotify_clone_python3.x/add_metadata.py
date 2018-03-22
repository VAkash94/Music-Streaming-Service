from cassandra.cluster import Cluster

KEY_SPACE = "application"
INSERT = """INSERT INTO songs (id, name, artist, album) VALUES (uuid(), %s, %s, %s)"""
CREATE = """CREATE TABLE songs (id uuid PRIMARY KEY, name text, artist list<text>, album text)"""


class Metadata:
    def __init__(self):
        self.cluster = Cluster()
        self.session = self.cluster.connect()
        self.session.execute("USE " + KEY_SPACE)

    def add_data(self, id, name, artists, album):
        artist_list = artists.strip().split(":")
        artist_name = []
        for artist in artist_list:
            artist_name.append(artist)

        if not self.is_song_exist(id, name, artists, album):
            self.session.execute(INSERT, (name, artist_name, album))

    def add_data_from_file(self, file_path):
        with open(file_path) as input_file:
            for line in input_file:
                record = line.strip().split(",")
                track_name = record[0]
                artist_name = []
                artist_list = record[1].strip().split(":")
                for artist in artist_list:
                    artist_name.append(artist)
                album_name = record[2]
                if not self.is_song_exist(track_name, artist_name, album_name):
                    self.session.execute(INSERT, (track_name, artist_name, album_name))

    def get_record(self):
        rows = self.session.execute('SELECT id, name, artist, album FROM songs')
        return rows

    def create_table(self):
        self.session.execute(CREATE)

    def execute_query(self, query):
        return self.session.execute(query)

    def is_song_exist(self, name, artists, album):
        rows = self.get_record()
        for row in rows:
            if row.name == name and row.artist == artists:
                print("{} by {} already exists in the database".format(name, artists))
                return True
        return False


def test():
    metadata = Metadata()
    # metadata.create_table()
    # metadata.add_data_from_file("./input/songs")
    rows = metadata.get_record()
    for row in rows:
        print(row.id, row.name, row.artist, row.album)


if __name__ == '__main__':
    test()