
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIPY_CLIENT_ID='36ef80a168ff4294b3750b0360379b91'
SPOTIPY_CLIENT_SECRET='208307ba75a9419bbc77c0aea3e8f78b'

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

sp.trace = False

# find album by name
album = "Shapeofyou"
name = "Michael jackson"
results = sp.search(q = "artist:" + name, type = "artist")

# get the first album uri
#album_id = results['albums']['items'][0]['uri']
items = results['artists']['items']

if len(items) > 0:
    artist = items[0]
    print artist['name'], artist['images'][0]['url']
    print artist['uri']