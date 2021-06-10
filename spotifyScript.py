import spotipy
from credentials import client_id, client_secret, redirect_uri
from spotipy.oauth2 import SpotifyOAuth

# This function gives the percentages of each artist in a playlist or list of playlists, by number of songs and lengths
# PARAM: playlistList: the list of playlists to analyse
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
def main():
	main_playlist_id = '4Wpg7A4AldVO2o5LoU1P8f'
	trial_playlist_id = '3LQNydHP8YdfakWeCZt3J4'
	scope = "playlist-modify-public user-read-playback-state"
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
	currentSong = sp.current_playback()
	sp.playlist_remove_all_occurrences_of_items(trial_playlist_id, [currentSong['item']['uri']])
	sp.playlist_remove_all_occurrences_of_items(main_playlist_id, [currentSong['item']['uri']])
	sp.playlist_add_items(main_playlist_id, [currentSong['item']['uri']])

if __name__ == '__main__':
	main()