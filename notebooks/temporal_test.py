import requests
import json

# Define the URL of the context broker's NGSI-LD API
url = "http://10.0.01:1026/ngsi-ld/v1/entities"

# Define the headers for the HTTP request
headers = {
    "Content-Type": "application/ld+json",

}

# Define the entity to be posted as a Python dictionary
entity = {
    "@context": ["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"],
    "id": "urn:ngsi-ld:Room:001",
    "type": "Room",
    "temperature": {
        "type": "Property",
        "value": 25,
        "observedAt": "2022-03-28T14:22:00Z"
    }
}

# Convert the entity to a JSON string
payload = json.dumps(entity)

# Send the POST request to the context broker's NGSI-LD API
response = requests.post(url, headers=headers, data=payload)

# Print the response from the context broker's NGSI-LD API
print(response.text)
