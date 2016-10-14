from flask import Flask
from flask import request
import json

app = Flask(__name__)

# General Welcome
@app.route("/")
def welcome():
	result_string = "Hey! You can check out /hello/<name>."
	return(result_string)

# Name
@app.route('/hello/<name>')
def hello(name):
	welcome = 'Hello, ' + str(name) + '!'
	br = '<br>'
	name = 'Your name has ' + str(len(name)) + ' characters in it.'
	result_string = welcome + br + name
	return(result_string)

# Fizzbuzz
@app.route('/fizzbuzz/<num>')
def fizzbuzz(num):

	dictionary = {}
	num_fizz = 0
	num_buzz = 0
	num_fizz_buzz = 0
	num_non = 0

	result_string = ""
	for i in range(1, int(num)+1):
		if i%3 == 0 and i%5 == 0:
			result_string += "fizzbuzz "
			num_fizz_buzz += 1
		elif i%3 == 0:
			result_string += "fizz "
			num_fizz += 1
		elif i%5 == 0:
			result_string += "buzz "
			num_buzz += 1
		else:
			result_string += str(str(i) + " ")
			num_non += 1

	dictionary["code"] = 200
	dictionary["number"] = num
	dictionary["string"] = result_string
	dictionary["num_of_fizz"] = num_fizz
	dictionary["num_of_buzz"] = num_buzz
	dictionary["num_of_fizzbuzz"] = num_fizz_buzz
	dictionary["num_of_non"] = num_non

	result = json.dumps(dictionary)
	return(result)


# =================================================
# Pets
# =================================================

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

# # Turn Multiple Pets Into JSON String
# def pets_to_str(pets):
# 	pets_dict = []
# 	for pet in pets:
# 		p_dict = pet.to_dict()
# 		p_str = str(p_dict)
# 		pets_dict.append(p_str)
# 	result_string = "["
# 	result_string += ','.join(pets_dict)
# 	result_string += "]"
# 	return(result_string)

# Pet List
pet_list = []

# PETS
@app.route('/pets/', methods=['GET'])
def pets():
	return_list = [pet.to_str() for pet in pet_list]
	print(return_list)
	print(type(return_list))
	return(','.join(return_list))

# ADD PET
@app.route('/pets/', methods=['POST'])
def addPet():

	

	args = request.args
	if all(arg in args for arg in ['name', 'age', 'species']):
		pet = Pet(args.get('name'), args.get('age'), args.get('species'))
		pet_list.append(pet)
		return("Succesfully added.")
	return("Unsuccessful. Please have parameters 'name', 'age', and 'species' set.")

# GET PET
@app.route('/pets/<name>', methods=['GET'])
def getPet(name):
	name = str(name)

	matching_pets = []
	for pet in pet_list:
		if pet.name == name:
			matching_pets.append(pet)

	if len(matching_pets) > 0:
		return_list = [pet.to_str() for pet in pet_list]
		print(return_list)
		print(type(return_list))
		return(','.join(return_list))

	else:
		return("No matching pets by the name '" + name + "'")

if __name__ == "__main__":
    app.run()
