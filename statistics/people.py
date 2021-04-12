class Person:
    def __init__(self, gender, party, state):
        self.gender = gender
        self.party = party
        self.state = state
        self.name = None

    def add_name(self, name):
        if(type(name) == type([])):
            cleaned_name = []
            for each in name:
                if(each != None and each != "null" and each != "" and each != " "):
                    cleaned_name.append(each)
            self.name = ' '.join(cleaned_name)
        else:
            self.name = name

    def print(self):
        if (self.name == "Unopposed"):
            print("\t\t No additional candidates")
        else:
            print("\t\t", self.name, self.state, self.party, self.gender)

class Senator:
    def __init__(self, person, incumbency_status, seniority, elect1, elect2, perc_with_party, perc_against_party):
        self.person = person
        self.incumbent = incumbency_status
        self.seniority = seniority
        self.elections = [elect1, elect2]
        self.perc_with_party = perc_with_party
        self.perc_against_party = perc_against_party

    def print(self):
        print("\t\t I")
        self.person.print()

class Candidate:
    def __init__(self, person, perc_votes, funding):
        self.person = person
        self.perc_votes = perc_votes
        self.funding = funding

    def is_incumbent(self, status):
        self.incumbent = status

    def print(self):
        self.person.print()
