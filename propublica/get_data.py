# gets the senate data from propublica
import requests
import json

X_API_Key = "eCnek3741Wxhg4vWGwNoMvv150cmsozKhFLH413p"

#80 - 117
full_response = {}
# get the api data from the 80th to 117th Congress
for i in range(80, 117+1):
    url = 'https://api.propublica.org/congress/v1/'+str(i)+'/senate/members.json'
    headers = {'X-API-Key': X_API_Key} # signed up for a key on their website
    r = requests.get(url, headers=headers) # returns a JSON string
    full_response[i] = r.json()
    print(i, "retrieved")

print(r.status_code) # tells whether the last request was successful

# exports the full_response dictionary to a file as a JSON string
with open('propublica.json', 'w') as outfile:
    json.dump(full_response, outfile, indent=2)
