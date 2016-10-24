#from flask import json
import main as server
import json
import unittest

class FlaskServerTest(unittest.TestCase):

	def setUp(self):
		# Run app in testing mode to retrieve exceptions and stack traces
		server.app.testing = True
		self.app = server.app.test_client()
		self.initArray()

	def test_hello(self):
		response = self.app.get('/hello')
		assert response.status_code == 200, "Status code was not OK"
		assert response.data == "Hello World!", "Response data was not OK"

	def test_get_pets(self):
		response = self.app.get('/pets/')
		assert response.status_code == 200, "Status code was not OK"
		assert type(response.data) == str, "Response data was not string"
		response_dict = json.loads(response.data)
		assert type(response_dict["response"]) == list, "Response['response'] type was not list"
		assert response_dict["response"][0]["name"] == "Jimmy"

	def test_pet_search_by_name(self):
		response = self.app.get('/pets/Wowo')
		assert response.status_code == 200, "status code was not ok"
		assert type(response.data) == str, "Response data was not string"
		response_dict = json.loads(response.data)
		assert response_dict["response"]["name"] == "Wowo"
		assert response_dict["response"]["age"] == "16"
		assert response_dict["response"]["species"] == "cat"

	def test_pet_search_name_not_in_pet_list(self):
		response = self.app.get('/pets/wjeifojwiejf')
		assert response.status_code != 200
		assert type(response.data) == str
		response_dict = json.loads(response.data)
		assert response_dict["response"] == "Unsuccessful. No matching pets by that name."

	def test_create_pet(self):
		response = self.app.post('/pets/?name=Woah&age=16&species=cat')
		assert response.status_code == 200
		assert type(response.data) == str
		response_dict = json.loads(response.data)
		assert response_dict["response"]["name"] == "Woah"
		assert response_dict["response"]["age"] == "16"
		assert response_dict["response"]["species"] == "cat"
		assert len(json.loads(self.app.get('/pets/').data)["response"]) == 4

	def test_create_pet_with_same_name(self):
		response = self.app.post('/pets/?name=Jimmy&age=16&species=cat')
		assert response.status_code != 200
		assert type(response.data) == str
		response_dict = json.loads(response.data)
		assert response_dict["response"] == "Unsuccessful. There is already a pet with that name."

	def test_create_pet_without_all_args(self):
		response = self.app.post('/pets/?name=fake&age=8')
		assert response.status_code != 200
		assert type(response.data) == str
		response_dict = json.loads(response.data)
		assert response_dict["response"] == "Unsuccessful. Please have parameters 'name', 'age', and 'species' set."

	def test_update_pet(self):
		response = self.app.put('pets/Jimmy?name=Woah&age=16&species=cat')
		assert response.status_code == 200
		assert type(response.data) == str
		response_dict = json.loads(response.data)
		assert response_dict["response"]["name"] == "Woah"
		assert response_dict["response"]["age"] == "16"
		assert response_dict["response"]["species"] == "cat"
		assert len(json.loads(self.app.get('/pets/').data)["response"]) == 3

	def test_update_pet_name_not_in_pet_list(self):
		response = self.app.put('/pets/wjeifojwiejf/?name=fake&age=7&species=doggo')
		assert response.status_code != 200
		assert type(response.data) == str
		response_dict = json.loads(response.data)
		assert response_dict["response"] == "Unsuccessful. No matching pets by that name."

	def test_update_pet_without_all_args(self):
		response = self.app.put('/pets/?name=fake&age=8')
		assert response.status_code != 200
		assert type(response.data) == str
		response_dict = json.loads(response.data)
		assert response_dict["response"] == "Unsuccessful. Please have parameters 'name', 'age', and 'species' set."

	def test_delete_pet(self):
		response = self.app.delete('pets/Jimmy')
		assert response.status_code == 200
		assert type(response.data) == str
		response_dict = json.loads(response.data)
		assert response_dict["response"] == "Succesful. Removed pet."
		assert len(json.loads(self.app.get('/pets/').data)["response"]) == 2

	def test_delete_pet_name_not_in_pet_list(self):
		response = self.app.delete('/pets/wjeifojwiejf')
		assert response.status_code != 200
		assert type(response.data) == str
		assert response_dict["response"] == "Unsuccessful. No matching pets by that name."

	def initArray(self):
		pet1 = server.Pet("Jimmy", "16", "cat")
		pet2 = server.Pet("Jumy", "16", "cat")
		pet3 = server.Pet("Wowo", "16", "cat")
		server.pet_list = [pet1, pet2, pet3]

if __name__ == '__main__':
	unittest.main()