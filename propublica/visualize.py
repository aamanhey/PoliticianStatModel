# visualizes the propublica data
import json
import matplotlib.pyplot as plt

with open('stats.json') as f:
  data = json.load(f)

def scatter():
    x_vals = []
    y_vals = []
    for each in data:
        print(each)
        if(each != 'total'):
            year = 1788 + 2*(int(each))
            congress = data[each]
            women = congress['women']
            men = congress['men']
            p = women / men
            x_vals.append(year)
            y_vals.append(p)
    fig = plt.figure()
    s = plt.scatter(x_vals, y_vals)
    print(x_vals, y_vals)
    fig.suptitle('Proportion of Women to Men in the Senate\nfrom the 101st to the 113th Congresses')
    plt.show()

def histogram():
    overall = data['total']
    new_data = {'women':overall['women'],'men':overall['men'],'other':overall['other']}
    names = list(new_data.keys())
    values = list(new_data.values())

    fig, axs = plt.subplots()
    axs.bar(names, values)
    fig.suptitle('101-113th Congresses')
    plt.show()

scatter()

'''
Confidence Level : 90%
Population Size: 1338
Margin of Error: 7%
Ideal Sample Size: 126

11% of all members of the senate are women
[1990, 1992, 1994, 1996, 1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014]
[0.020202020202020204, 0.04, 0.07216494845360824, 0.09574468085106383, 0.0989010989010989, 0.0967741935483871, 0.15555555555555556, 0.16279069767441862, 0.16091954022988506, 0.18604651162790697, 0.1956521739130435, 0.2, 0.23529411764705882]

'''
