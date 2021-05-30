import spotipy
from credentials import client_id, client_secret, redirect_uri
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

# gets users saved tracks
results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
	track = item['track']
	print(idx, track['artists'][0]['name'], " – ", track['name'])

# Analyse a specific playlist
playlist = sp.playlist_tracks("08r7gmYnqqZ7YBih2kyug2", limit=100)
i = 0
artistCounts = {}
artistLengths = {}
totalLength = 0
while i < playlist['total']:
	playlist = sp.playlist_tracks("08r7gmYnqqZ7YBih2kyug2", limit=100, offset=i)
	for track in playlist['items']:
		i += 1
		totalLength += track['track']['duration_ms']
		if track['track']['artists'][0]['name'] in artistCounts:
			artistCounts[track['track']['artists'][0]['name']] += 1
			artistLengths[track['track']['artists'][0]['name']] += track['track']['duration_ms']
		else:
			artistCounts[track['track']['artists'][0]['name']] = 1
			artistLengths[track['track']['artists'][0]['name']] = track['track']['duration_ms']

# dicts are now filled with song and length totals, putting them into lists to be sorted

artistSongCount = []
artistSongLengths = []
for artist in artistCounts:
	artistSongCount.append((artist, artistCounts[artist]))
for artist in artistLengths:
	artistSongLengths.append((artist, artistLengths[artist]))

artistSongLengths.sort(key=lambda tup: tup[1], reverse=True)
artistSongCount.sort(key=lambda tup: tup[1], reverse=True)
print(totalLength)
for idx, artist in enumerate(artistSongCount):
	print((str(idx) + ". ").ljust(5, " ") + artist[0].ljust(50, "-") + " " +  str(round((artist[1]/i)*100, 3)) + "\t" + (str(idx) + ". ").ljust(5, " ") + artistSongLengths[idx][0].ljust(50, "-") + " " + str(round((artistSongLengths[idx][1]/totalLength)*100, 3)))




#playlist_remove_all_occurrences_of_items(playlist_id, items, snapshot_id=None)
#Removes all occurrences of the given tracks from the given playlist
#
#Parameters:
#playlist_id - the id of the playlist
#items - list of track/episode ids to remove from the playlist
#snapshot_id - optional id of the playlist snapshot
#
#
#playlist(playlist_id, fields=None, market=None, additional_types=('track', ))
#Gets playlist by id.
#
#Parameters:
#playlist - the id of the playlist
#fields - which fields to return
#market - An ISO 3166-1 alpha-2 country code or the
#string from_token.
#additional_types - list of item types to return.
#valid types are: track and episode
#
#playlist_add_items(playlist_id, items, position=None)
#Adds tracks/episodes to a playlist
#
#Parameters:
#playlist_id - the id of the playlist
#items - a list of track/episode URIs, URLs or IDs
#position - the position to add the tracks