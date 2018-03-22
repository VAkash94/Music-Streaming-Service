
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint

SPOTIPY_CLIENT_ID='36ef80a168ff4294b3750b0360379b91'
SPOTIPY_CLIENT_SECRET='208307ba75a9419bbc77c0aea3e8f78b'

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

sp.trace = False

# find album by name
album = "XSCAPE"
results = sp.search(q = "album:" + album, type = "album")
# pprint.pprint(results)
# get the first album uri
album_id = results['albums']['items'][0]['uri']

# get album tracks
tracks = sp.album_tracks(album_id)
# pprint.pprint(tracks)
count = 0
for track in tracks['items']:
    print(track['name'], track['artists'][0]['name'], album)
    if len(track['artists']) > 1:
        print(track['artists'][1]['name'])
        count += 1

print count
