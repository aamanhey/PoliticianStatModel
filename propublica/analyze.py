# counts the number of representatives that are Male and Female
import json

from urllib.request import urlopen

# calls the GenderAPI to approximate the gender based on a person's name for senators that did not have
# a gender available in propublica
def approx_gender(name):
    myKey = "cuBFBDdkJGrCWETndE"
    #split up the name split=tim%20johnson to first and last and replace space with %20
    url = "https://gender-api.com/get?key=" + myKey + "&country=US"
    # includes first and last names if available
    if (len(name) == 2):
        url = url + "&split=" + name[0] + "%20" + name[1]
    # includes first name if available
    elif (len(name) == 1):
        url = url + "&name=" + name[0]
    # does not make query if no name available
    else:
        return {"gender":None, "accuracy":100}
    response = urlopen(url)
    decoded = response.read().decode('utf-8')
    info = json.loads(decoded)
    return {"gender":info["gender"], "accuracy":info['accuracy']}

# open json file and turns it into a python dictionary
with open('propublica_formatted.json') as f:
  data = json.load(f)

# counters for all the years considered
tot_w = 0
tot_m = 0
tot_n = 0 # neither, propublica didn't have data on that person and the GenderAPI could not predict the gender
total_apprxs = 0

num_senators = 0
stats = {}
# iterate through each of the congresses in the propublica dataset and count the number of men and women
for year in range(1990, 2015+1, 2):
    congress_num = str(int((year-1788)/2)) # convert year into the congress number
    # counters for that year
    num_women = 0
    num_men = 0
    num_n = 0 # neither
    num_apprxs = 0

    senate = data[congress_num] # senate in the respective year
    # GenderAPI provides an accuracy with each prediction
    apprxs = {'overall accuracy':100, 'number':num_apprxs, 'senators':{}}
    accuracy = 100 # default accuracy for the respective year

    for member in senate:
        senator = senate[member]
        # get gender from propublica if available
        gender = senator['gender']
        if(gender == 'M'):
            num_men += 1
            tot_m += 1
        elif(gender == 'F'):
            num_women += 1
            tot_w += 1
        else:
            # get gender from GenderAPI if available with an accuracy
            result = approx_gender(member.split()) # function call for GenderAPI
            gender = result['gender'] # predicted gender

            apprxs['senators'][member] = {'i_acc':result['accuracy'], 'gender':result['gender']}
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
    # add the data from an individual year to the total dictionary
    apprxs['overall accuracy'] = accuracy
    apprxs['number'] = num_apprxs
    stats[congress_num] = {'women':num_women, 'men':num_men, 'neither':num_n, 'approximations':apprxs}
    print(congress_num, "calculated")
# add the total value of the counters to a seperate field in the overall dictionary
stats['total'] = {'women':tot_w, 'men':tot_m, 'other':tot_n, 'approximations':total_apprxs}

# exports the stats dictionary to a file as a JSON string
with open('stats.json', 'w') as outfile:
    json.dump(stats, outfile, indent=2)
