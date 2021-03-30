import requests
import json

X_API_Key = "eCnek3741Wxhg4vWGwNoMvv150cmsozKhFLH413p"

# end year of that congress = 1788 + 2(congress #)
# 117th congress: 1788 + 2(117) = 2022
# congress numbers can range from 80 to 117

#80 - 117
full_response = {}
for i in range(80, 117+1):
    url = 'https://api.propublica.org/congress/v1/'+str(i)+'/senate/members.json'
    headers = {'X-API-Key': X_API_Key}
    r = requests.get(url, headers=headers)
    full_response[i] = r.json()
    print(i, "retrieved")

print(r.status_code)

with open('propublica.json', 'w') as outfile:
    json.dump(full_response, outfile, indent=2)
