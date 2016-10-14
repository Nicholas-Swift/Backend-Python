import httplib2
import json

http = httplib2.Http()
response, body = http.request(url, "GET")
content = json.loads(body)

# Body is a string, content is usually a dictionary, but sometimes a list, depending on what the url returns


response_string = '''{
    "firstName": "Grace",
    "lastName": "Hopper",
    "age": 107,
    "address": {
        "streetAddress": "21 2nd Street",
        "city": "New York",
        "state": "NY",
        "postalCode": 10021
    },
    "phoneNumbers": [
        {
            "type": "home",
            "number": "212-555-1234"
        },
        {
            "type": "mobile",
            "number": "646-555-4567"
        }
    ]
}'''

# print(returned_string)

content_dict = json.loads(response_string)
postal_code = content_dict["address"]["postalCode"]
mobile_phone = content_dict["phoneNumbers"][1]["number"]

print(postal_code)
print(mobile_phone)