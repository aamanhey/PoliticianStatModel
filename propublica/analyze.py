import json

from urllib.request import urlopen

def approx_gender(name):
    # calls the GenderAPI
    # approximates the gender of a person based on the name
    myKey = "cuBFBDdkJGrCWETndE"
    #split up the name split=tim%20johnson to first and last and replace space with %20
    url = "https://gender-api.com/get?key=" + myKey + "&country=US"
    if (len(name) == 2):
        url = url + "&split=" + name[0] + "%20" + name[1]
    elif (len(name) == 1):
        url = url + "&name=" + name[0]
    else:
        return {"gender":None, "accuracy":100}
    response = urlopen(url)
    decoded = response.read().decode('utf-8')
    info = json.loads(decoded)
    # print( "Gender: " + data["gender"]); #Gender: male
    return {"gender":info["gender"], "accuracy":info['accuracy']}

# open json file
with open('propublica_formatted.json') as f:
  data = json.load(f)



tot_w = 0
tot_m = 0
tot_n = 0 # neither
# a neither signifies the propublica didn't have data on that person
total_apprxs = 0

num_senators = 0
stats = {}
# for year in range(1948, 2015+1):
for year in range(1990, 2015+1, 2):
    congress_num = str(int((year-1788)/2))
    num_women = 0
    num_men = 0
    num_n = 0 # neither
    num_apprxs = 0
    senate = data[congress_num]
    apprxs = {'overall accuracy':100, 'number':num_apprxs, 'senators':{}}
    accuracy = 100
    for member in senate:
        senator = senate[member]
        gender = senator['gender']
        if(gender == 'M'):
            num_men += 1
            tot_m += 1
        elif(gender == 'F'):
            num_women += 1
            tot_w += 1
        else:
            result = approx_gender(member.split())
            apprxs['senators'][member] = {'i_acc':result['accuracy'], 'gender':result['gender']}
            gender = result['gender']
            accuracy = accuracy * (result['accuracy']/100)
            total_apprxs += 1
            num_apprxs += 1
            if(gender == 'male'):
                num_men += 1
                tot_m += 1
            elif(gender == 'female'):
                num_women += 1
                tot_w += 1
            else:
                num_n += 1
                tot_n += 1
        num_senators += 1
    apprxs['overall accuracy'] = accuracy
    apprxs['number'] = num_apprxs
    stats[congress_num] = {'women':num_women, 'men':num_men, 'non-binary':num_n, 'approximations':apprxs}
    print(congress_num, "calculated")
stats['total'] = {'women':tot_w, 'men':tot_m, 'other':tot_n, 'approximations':total_apprxs}
with open('stats.json', 'w') as outfile:
    json.dump(stats, outfile, indent=2)
