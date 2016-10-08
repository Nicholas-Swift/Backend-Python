import httplib2
import urllib
import json
import base64


class GoogleTranslateAPI:

	# Variables
	BASE_URL = "https://www.googleapis.com"
	PATH_URL = "/language/translate/v2"

	# Init
	def __init__(self, api_key):
		self.api_key = api_key

	# Google Translate Request
	def __request(self, text, language):
		url = GoogleTranslateAPI.BASE_URL + GoogleTranslateAPI.PATH_URL
		data = urllib.urlencode({'key': self.api_key,
								 'q': text, 
								 'source': 'en', 
								 'target': language})
		url = url + "?" + data

		http = httplib2.Http()
		response, content = http.request(url, "GET")
		# response, content = http.request(url, "GET", body=data)

		print(response)
		print(content)

		return(content)

	# Parse the JSON
	def __parse_json(self, json_string):
		data_dict = json.loads(json_string)
		try:
			translated_text = data_dict['data']['translations'][0]['translatedText']
		except:
			translated_text = "The text could not be translated."

		return(translated_text)

	# Translate
	def translate(self, text, language):
		if type(text) == str:
			res = self.__request(text, language)
			translated_text = self.__parse_json(res)
			return(translated_text)
		elif type(text) == list:
			translated_list = []
			for string in text:
				self.__request(string, language)
				translated_text = self.__parse_json()
				translated_list.append(translated_text)
			return(translated_list)
		else:
			return("Please use str or list")


if __name__ == "__main__":
	main()
