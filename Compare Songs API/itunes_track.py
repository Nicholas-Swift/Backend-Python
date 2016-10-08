import re


class ItunesTrack:

	def __init__(self, body_dict):
		b = body_dict

		# General Track
		self.id = b["trackId"]
		self.name = b["trackName"]
		self.duration_ms = b["trackTimeMillis"]
		if b["trackExplicitness"] == "notExplicit":
			self.explicit = False;
		else:
			self.explicit = True
		self.album_name = b["collectionName"]
		self.track_numer = b["trackNumber"]
		self.disc_number = b["discNumber"]

		self.artist = b["artistName"]

		# Sanitized
		self.sanitized_name1 = re.sub(r'\([^)]*\)', '', self.name)
		self.sanitized_name2 = self.sanitized_name1.split('-')[0]

		# Itunes Specific
		self.censored_name = b["trackCensoredName"]
		self.album_censored_name = b["collectionCensoredName"]


if __name__ == "__main__":
	main()