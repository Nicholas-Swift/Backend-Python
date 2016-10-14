from flask import Flask
from flask import request
import json

app = Flask(__name__)

# =================================================
# Welcome
# =================================================
@app.route("/")
def welcome():
	response_dict = {}
	response_dict["response"] = "Welcome to the petstore!"
	return(json.dumps(response_dict))


# =================================================
# Pets
# =================================================

# Pet List
pet_list = []

# Class Pet
class Pet:
	def __init__(self, name, age, species):
		self.name = name
		self.age = age
		self.species = species

	def to_dict(self):
		pet_dict = {}
		pet_dict['name'] = str(self.name)
		pet_dict['age'] = str(self.age)
		pet_dict['species'] = str(self.species)
		return pet_dict

	def to_str(self):
		pet_dict = self.to_dict()
		pet_str = json.dumps(pet_dict)
		return(pet_str)

# PETS
@app.route('/pets/', methods=['GET'])
def pets():
	response_dict = {}
	pet_str_list = [pet.to_dict() for pet in pet_list]
	response_dict["response"] = pet_str_list
	return(json.dumps(response_dict))

# ADD PET
@app.route('/pets/', methods=['POST'])
def addPet():
	response_dict = {}
	args = request.args

	if all(arg in args for arg in ['name', 'age', 'species']):

		pet_name = args.get('name')
		pet_age = args.get('age')
		pet_species = args.get('species')

		for pet in pet_list:
			if pet_name == pet.name:
				response_dict["response"] = "Unsuccessful. There is already a pet with that name.."
				return(json.dumps(response_dict), 409)

		pet = Pet(pet_name, pet_age, pet_species)
		pet_list.append(pet)
		response_dict["response"] = "Succesful. Added pet."
		return(json.dumps(response_dict))

	response_dict["response"] = "Unsuccessful. Please have parameters 'name', 'age', and 'species' set."
	return(json.dumps(response_dict), 400)

# GET PET
@app.route('/pets/<name>', methods=['GET'])
def getPet(name):
	response_dict = {}
	name = str(name)

	for pet in pet_list:
		if pet.name == name:
			response_dict["response"] = pet.to_dict()
			return(json.dumps(response_dict))

	response_dict["response"] = "Unsuccessful. No matching pets by that name."
	return(json.dumps(response_dict), 400)

# UPDATE PET
@app.route('/pets/<name>', methods=['PUT'])
def updatePet(name):
	response_dict = {}
	args = request.args
	name = str(name)

	if all(arg in args for arg in ['name', 'age', 'species']):
		pet_name = args.get('name')
		pet_age = args.get('age')
		pet_species = args.get('species')

		for pet in pet_list:
			if pet.name == name:
				pet.name = pet_name
				pet.age = pet_age
				pet.species = pet_species

				response_dict["response"] = "Succesful. Updated pet."
				return(json.dumps(response_dict))

		response_dict["response"] = "Unsuccessful. There is no pet with that name."
		return(json.dumps(response_dict), 404)

	else:
		response_dict["response"] = "Unsuccessful. Please have parameters 'name', 'age', and 'species' set."
		return(json.dumps(response_dict), 400)

# DELETE PET
@app.route('/pets/<name>', methods=['DELETE'])
def deletePet(name):
	response_dict = {}
	name = str(name)

	for i in range(0, len(pet_list)):
		if pet_list[i].name == name:
			pet_list.remove(pet_list[i])

			response_dict["response"] = "Succesful. Removed pet."
			return(json.dumps(response_dict))

	response_dict["response"] = "Unsuccessful. There is no pet with that name."
	return(json.dumps(response_dict), 404)


if __name__ == "__main__":
    app.run()
