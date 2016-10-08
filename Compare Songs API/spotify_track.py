import re


class SpotifyTrack:

	def __init__(self, body_dict):
		b = body_dict

		# General Track
		self.id = b["id"]
		self.name = b["name"]
		self.duration_ms = b["duration_ms"]
		self.explicit = b["explicit"]

		self.album_name = b["album"]["name"]
		self.track_numer = b["track_number"]
		self.disc_number = b["disc_number"]

		self.artist = b["artists"][0]["name"]

		# Sanitized
		self.sanitized_name1 = re.sub(r'\([^)]*\)', '', self.name)
		self.sanitized_name2 = self.sanitized_name1.split('-')[0]


if __name__ == "__main__":
	main()