from cassandra.cluster import Cluster
from add_metadata import Metadata
import uuid

cluster = Cluster()
session = cluster.connect()


session.execute("CREATE KEYSPACE userinfo WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };")
session.execute("USE userinfo")
session.execute("CREATE TABLE profile(username text PRIMARY KEY, playlist map<text,frozen<list<uuid>>>, currently_playing uuid, last_played uuid);")
session.execute("create table login(username text PRIMARY KEY, password text);")


session.execute("CREATE KEYSPACE application WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };")

session.execute("USE application;")

metadata = Metadata()
metadata.create_table()
metadata.add_data_from_file("./input/songs")

session.execute("USE application;")

rows = session.execute("SELECT * FROM songs LIMIT 6;")
rows = list(rows)
with open("./input/todays_hits", 'w') as output_file:
    for row in rows:
        sid = row.id
        output_file.write(str(sid) + "\n")
session.execute("CREATE TABLE todays_hits (id uuid PRIMARY KEY, name text, artist list<text>, album text)")

select_hits_query = "select id, album, artist, name from application.songs where id = ?"

insert_hits_query = "Insert into application.todays_hits(id, album, artist, name) values (?, ?, ?, ?)"

select_hits_prepared_statement = session.prepare(select_hits_query)
hits_prepared_statement = session.prepare(insert_hits_query)
with open("./input/todays_hits") as input_file:
    for line in input_file:
        song_id = line.strip()
        row = session.execute(select_hits_prepared_statement, [uuid.UUID(song_id)])
        session.execute(hits_prepared_statement, [row[0].id, row[0].album, row[0].artist, row[0].name])


session.execute("USE application")
session.execute("create index name_index on songs(name)")
session.execute("create index album_index on songs(album)")
session.execute("create index artist_index on songs(artist)")


print("=====================\nSetup completed.....\n=====================\n")