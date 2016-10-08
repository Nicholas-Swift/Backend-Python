import httplib2
import urllib
import json
import re
from flask import Flask
from compare_songs import CompareSongs

app = Flask(__name__)

# General Welcome
@app.route("/")
def welcome():
	result_string = "Hey! You can check out /hello/<name>, /spotify/<id>, /itunes/<id>. Hello just says hello. Spotify will return the itunes song equivalent. Itunes will return the spotify song equivalent."
	return("Hello World!")

# Name
@app.route('/hello/<name>')
def hello(name):
	result_string = 'Hello, ' + str(name) + '!'
	return(result_string)

# Search Spotify by id and return itunes
@app.route('/spotify/<id>')
def spotify(id):
	cs = CompareSongs()

	spotify_track = cs.get_spotify_track(id)
	my_itunes_id = cs.search_itunes_from_spotify(id)

	if my_itunes_id == 0:
		data = {}
		data['code'] = '404'
		data['status'] = 'Could not find a similar track'

		json_data = json.dumps(data)
		return(json_data)
	else:
		itunes_track = cs.get_itunes_track(my_itunes_id)

		data = {}
		data['code'] = '200'
		data['status'] = 'Successfully found a similar track'
		data['spotifySong'] = {'id': spotify_track.id, 'name': spotify_track.name, 'album': spotify_track.album_name, 'artist': spotify_track.artist}
		data['itunesSong'] = {'id': itunes_track.id, 'name': itunes_track.censored_name, 'album': itunes_track.album_censored_name, 'artist': itunes_track.artist}

		json_data = json.dumps(data)
		return(json_data)

# Search Itunes by id and return spotify
@app.route('/itunes/<id>')
def itunes(id):
	cs = CompareSongs()

	itunes_track = cs.get_itunes_track(id)
	my_spotify_id = cs.search_spotify_from_itunes(id)

	if my_spotify_id == 0:
		data = {}
		data['code'] = '404'
		data['status'] = 'Could not find a similar track'

		json_data = json.dumps(data)
		return(json_data)
	else:
		spotify_track = cs.get_spotify_track(my_spotify_id)

		data = {}
		data['code'] = '200'
		data['status'] = 'Successfully found a similar track'
		data['spotifySong'] = {'id': spotify_track.id, 'name': spotify_track.name, 'album': spotify_track.album_name, 'artist': spotify_track.artist}
		data['itunesSong'] = {'id': itunes_track.id, 'name': itunes_track.censored_name, 'album': itunes_track.album_censored_name, 'artist': itunes_track.artist}

		json_data = json.dumps(data)
		return(json_data)


if __name__ == "__main__":
    app.run()
