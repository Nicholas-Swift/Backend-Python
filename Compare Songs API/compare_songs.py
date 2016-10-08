import httplib2
import urllib
import json
from spotify_track import SpotifyTrack
from itunes_track import ItunesTrack
from fuzzywuzzy import fuzz


# Paths
SPOTIFY_SEARCH_BASE_URL = "https://api.spotify.com"
SPOTIFY_SEARCH_PATH_URL = "/v1/search"
#SPOTIFY_SEARCH_QUERY = "?q=paper%20kites&type=track" # search + "&type=track"

SPOTIFY_TRACK_BASE_URL = "https://api.spotify.com"
SPOTIFY_TRACK_PATH_URL = "/v1/tracks/"
#SPOTIFY_TRACK_QUERY = "41yIvlFgvGwxq8qTqAR7eG" # id

ITUNES_SEARCH_BASE_URL = "https://itunes.apple.com"
ITUNES_SEARCH_PATH_URL = "/search"
#ITUNES_SEARCH_QUERY = "?term=jack+johnson&limit=20"

ITUNES_TRACK_BASE_URL = "https://itunes.apple.com"
ITUNES_TRACK_PATH_URL = "/lookup"
#ITUNES_TRACK_QUERY = "?id=879273565&entity=song" #id

NN_NAME_CONST = 1
NN_EXPLICIT_NAME_CONST = 1
NN_EXPLICIT_CONST = 2
NN_ALBUM_CONST = 1
NN_EXPLICIT_ALBUM_CONST = 0.2
NN_ARTIST_CONST = 1
NN_SANITIZED_1_CONST = 1.2
NN_SANITIZED_2_CONST = 1.2
NN_DURATION_CONST = 2
NN_TRACK_CONST = 1
NN_DISC_CONST = 1.4


class CompareSongs:

	# Parse json
	def __parse_json(self, body):
		print(body)
		parsed_body = json.loads(body)
		return(parsed_body)

	# Make call
	def __request(self, body):
		http = httplib2.Http()
		response, body = http.request(body, "GET")
		return((response, body))

	# Get Spotify Track
	def get_spotify_track(self, track_id):
		search_url = SPOTIFY_TRACK_BASE_URL + SPOTIFY_TRACK_PATH_URL + track_id
		response, body = self.__request(search_url)
		parsed_body = self.__parse_json(body)
		spotify_track = SpotifyTrack(parsed_body)
		return(spotify_track)

	# Get Itunes Track
	def get_itunes_track(self, track_id):
		search_url = ITUNES_TRACK_BASE_URL + ITUNES_TRACK_PATH_URL + "?id=" + str(track_id) + "&entity=song"
		response, body = self.__request(search_url)
		parsed_body = self.__parse_json(body)["results"][0]
		itunes_track = ItunesTrack(parsed_body)
		return(itunes_track)

	# Search Spotify Tracks
	def __search_spotify_tracks(self, body):
		# Set up search
		track_param = urllib.quote(body.encode('utf-8'))
		search_url = SPOTIFY_SEARCH_BASE_URL + SPOTIFY_SEARCH_PATH_URL + "?q=" + str(track_param) + "&type=track"

		# Make a request
		response, body = self.__request(search_url)
		j = self.__parse_json(body)

		# Set up a spotify tracks
		spotify_track_list = []
		for track in j["tracks"]["items"]:
			spotify_track = SpotifyTrack(track)
			spotify_track_list.append(spotify_track)
		return(spotify_track_list)

	def __search_itunes_tracks(self, body):
		# Set up search
		track_param = urllib.quote(body.encode('utf-8'))
		search_url = ITUNES_SEARCH_BASE_URL + ITUNES_SEARCH_PATH_URL + "?term=" + track_param + "&entity=song&limit=20"

		print(search_url)
		# Make a request
		response, body = self.__request(search_url)
		j = self.__parse_json(body)

		# Set up a spotify tracks
		itunes_track_list = []
		for track in j["results"]:
			itunes_track = ItunesTrack(track)
			itunes_track_list.append(itunes_track)

		return(itunes_track_list)

	def __compare_track(self, spotify_track_id, itunes_track_id):

		# Setup Tracks
		spotify_track = self.get_spotify_track(spotify_track_id)
		itunes_track = self.get_itunes_track(itunes_track_id)

		# Do the ratios
		name_ratio = fuzz.partial_ratio(spotify_track.name, itunes_track.name)
		explicit_name_ratio = fuzz.partial_ratio(spotify_track.name, itunes_track.censored_name)
		explicit_ratio = 100 if spotify_track.explicit == itunes_track.explicit else 0
		album_ratio = fuzz.partial_ratio(spotify_track.album_name, itunes_track.album_name)
		explicit_album_ratio = fuzz.partial_ratio(spotify_track.name, itunes_track.album_censored_name)
		artist_ratio = fuzz.partial_ratio(spotify_track.artist, itunes_track.artist)

		sanitized_1_ratio = fuzz.partial_ratio(spotify_track.sanitized_name1, itunes_track.sanitized_name1)
		sanitized_2_ratio = fuzz.partial_ratio(spotify_track.sanitized_name2, itunes_track.sanitized_name2)

		duration_ratio = abs(spotify_track.duration_ms - itunes_track.duration_ms) / 1000
		if duration_ratio > 20:
			duration_ratio = 0
		elif duration_ratio > 15:
			duration_ratio = 20
		elif duration_ratio > 10:
			duration_ratio = 50
		elif duration_ratio > 5:
			duration_ratio = 80
		else:
			duration_ratio = 100

		track_ratio = abs(spotify_track.track_numer - itunes_track.track_numer)
		if track_ratio > 4:
			track_ratio = 0
		elif track_ratio > 3:
			track_ratio = 20
		elif track_ratio > 2:
			track_ratio = 40
		elif track_ratio > 1:
			track_ratio = 80
		else:
			track_ratio = 100

		disc_ratio = abs(spotify_track.disc_number - itunes_track.disc_number)
		if disc_ratio > 4:
			disc_ratio = 0
		elif disc_ratio > 3:
			disc_ratio = 20
		elif disc_ratio > 2:
			disc_ratio = 40
		elif disc_ratio > 1:
			disc_ratio = 80
		else:
			disc_ratio = 100

		if duration_ratio == 100:
			if artist_ratio >= 80:
				if sanitized_1_ratio >= 80:
					return("done")

		name_ratio *= NN_NAME_CONST
		explicit_name_ratio *= NN_EXPLICIT_NAME_CONST
		explicit_ratio *= NN_EXPLICIT_CONST
		album_ratio *= NN_ALBUM_CONST
		explicit_album_ratio *= NN_EXPLICIT_ALBUM_CONST
		artist_ratio *= NN_ARTIST_CONST
		sanitized_1_ratio *= NN_SANITIZED_1_CONST
		sanitized_2_ratio *= NN_SANITIZED_2_CONST
		duration_ratio *= NN_DURATION_CONST
		track_ratio *= NN_TRACK_CONST
		disc_ratio *= NN_DISC_CONST

		total_ratio = (name_ratio + explicit_name_ratio + duration_ratio + explicit_ratio + album_ratio + explicit_album_ratio + sanitized_1_ratio + sanitized_2_ratio + track_ratio + disc_ratio + artist_ratio) / 11

		# Print for debugging
		print("Spotify.. track: " + spotify_track.name + " . album: " + spotify_track.album_name + ". artist: " + spotify_track.artist)
		print("Itunes... track: " + itunes_track.name + " . album: " + itunes_track.album_name + ". artist: " + itunes_track.artist)
		print("name_ratio............ " + str(name_ratio))
		print("explicit_name_ratio... " + str(explicit_name_ratio))
		print("duration_ratio........ " + str(duration_ratio))
		print("explicit_ratio........ " + str(explicit_ratio))
		print("album_ratio........... " + str(album_ratio))
		print("explicit_album_ratio.. " + str(explicit_album_ratio))
		print("track_ratio........... " + str(track_ratio))
		print("sanitized_1_ratio..... " + str(sanitized_1_ratio))
		print("sanitized_2_ratio..... " + str(sanitized_2_ratio))
		print("disc_ratio............ " + str(disc_ratio))
		print("artist_ratio.......... " + str(artist_ratio))
		print("total_ratio........... " + str(total_ratio))

		print("\n\n\n")

		return(total_ratio)

	def search_itunes_from_spotify(self, spotify_track_id):
		total_ratio = 0
		best_match = 0

		spotify_track = self.get_spotify_track(spotify_track_id)
		itunes_tracks = self.__search_itunes_tracks(spotify_track.name)
		for itunes_track in itunes_tracks:
			num = self.__compare_track(spotify_track.id, itunes_track.id)
			if type(num) == str:
				best_match = itunes_track.id
				return(best_match)
			else:
				if num > total_ratio:
					total_ratio = num
					best_match = itunes_track.id
		if itunes_tracks == []:
			itunes_tracks = self.__search_itunes_tracks(spotify_track.sanitized_name2)
			for itunes_track in itunes_tracks:
				num = self.__compare_track(spotify_track.id, itunes_track.id)
				if type(num) == str:
					best_match = itunes_track.id
					return(best_match)
				else:
					if num > total_ratio:
						total_ratio = num
						best_match = itunes_track.id

		print("best_match: " + str(best_match))
		return(best_match)

	def search_spotify_from_itunes(self, itunes_track_id):
		total_ratio = 0
		best_match = 0

		itunes_track = self.get_itunes_track(itunes_track_id)
		spotify_tracks = self.__search_spotify_tracks(itunes_track.name)
		for spotify_track in spotify_tracks:
			num = self.__compare_track(spotify_track.id, itunes_track.id)
			if type(num) == str:
				best_match = spotify_track.id
				return(best_match)
			else:
				if num > total_ratio:
					total_ratio = num
					best_match = spotify_track.id
		if spotify_tracks == []:
			spotify_tracks = self.__search_spotify_tracks(itunes_track.sanitized_name2)
			for spotify_track in spotify_tracks:
				num = self.__compare_track(spotify_track.id, itunes_track.id)
				if type(num) == str:
					best_match = spotify_track.id
					return(best_match)
				else:
					if num > total_ratio:
						total_ratio = num
						best_match = spotify_track.id

		print("best_match: " + str(best_match))
		return(best_match)


if __name__ == "__main__":
	main()

