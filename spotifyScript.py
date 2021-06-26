import spotipy
import sys
from credentials import client_id, client_secret, redirect_uri
from spotipy.oauth2 import SpotifyOAuth

# This function gives the percentages of each artist in a playlist or list of playlists, by number of songs and lengths
# PARAM: playlistList: the list of playlists to analyse, a list of playlist IDs
def analysePlaylistArtists(playlistList):
	scope = ""
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

	artistCounts = {}
	artistLengths = {}
	totalLength = 0
	songCount = 0
	for thisPlaylist in playlistList:
	# Analyse a specific playlist
		playlist = sp.playlist_tracks(thisPlaylist, limit=100)

		i = 0
		while i < playlist['total']:
			playlist = sp.playlist_tracks(thisPlaylist, limit=100, offset=i)
			for track in playlist['items']:
				songCount += 1
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
		print((str(idx) + ". ").ljust(5, " ") + artist[0].ljust(50, "-") + " " +  str(round((artist[1]/songCount)*100, 3)) + "\t" + (str(idx) + ". ").ljust(5, " ") + artistSongLengths[idx][0].ljust(50, "-") + " " + str(round((artistSongLengths[idx][1]/totalLength)*100, 3)))

# Moves the currently playing song from a preset "trial" playlist to a preset "main" playlist.
def commitSong(main_playlist_id, trial_playlist_id):
	scope = "playlist-modify-public playlist-modify-private user-read-playback-state"
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
	currentSong = sp.current_playback()
	if currentSong is not None:
		sp.playlist_remove_all_occurrences_of_items(trial_playlist_id, [currentSong['item']['uri']])
		sp.playlist_remove_all_occurrences_of_items(main_playlist_id, [currentSong['item']['uri']])
		sp.playlist_add_items(main_playlist_id, [currentSong['item']['uri']])

# Remove the currently playing song from the current playlist
def removeSong():
	scope = "playlist-modify-public playlist-modify-private user-read-playback-state"
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
	currentSong = sp.current_playback()
	if currentSong is not None:
		sp.playlist_remove_all_occurrences_of_items(currentSong['context']['uri'], [currentSong['item']['uri']])

# Add the currently playing song to a specified playlist
def addSong(playlistUri):
	scope = "playlist-modify-public playlist-modify-private user-read-playback-state"
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
	currentSong = sp.current_playback()
	if currentSong is not None:
		sp.playlist_add_items(playlistUri, [currentSong['item']['uri']])

# arguments are assumed to be well formed, the program giving an error is hardly worse than giving an error that I wrote
def main(args):
	if len(args) == 0:
		commitSong('4Wpg7A4AldVO2o5LoU1P8f', '3LQNydHP8YdfakWeCZt3J4')
	elif args[0] == 'commit':
		commitSong(args[1], args[2])
	elif args[0] == 'delete':
		removeSong()
	elif args[0] == 'add':
		addSong(args[1])
	elif args[0] == 'analyse':
		analysePlaylistArtists(args[1::])

if __name__ == '__main__':
	main(sys.argv[1::])