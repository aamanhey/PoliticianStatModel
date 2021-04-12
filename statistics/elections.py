import people

class Election:
    def __init__(self, state, year):
        self.state = state
        self.year = year
        self.candidates = []
        self.incumbent = None

    def add_candidate(self, candidate):
        self.candidates.append(candidate)

    def add_incumbent(self, incumbent):
        self.incumbent = incumbent

    def print(self):
        print("\t", self.year, self.state)
        if self.incumbent != None:
            self.incumbent.print()
        for each in self.candidates:
            each.print()

def make_person(state, election_data):
    gender = election_data[5]
    if(gender == "F"):
        gender = 1
    else:
        gender = 0
    party = election_data[6]
    person = people.Person(gender, party, state)

    first_name = election_data[2]
    middle_name = election_data[3]
    last_name = election_data[4]
    person.add_name([first_name, middle_name, last_name])
    return person

def make_incumbent(person, election_data):
    election_history_1 = election_data[0]
    election_history_2 = election_data[1]
    seniority = election_data[2]
    perc_with_party = election_data[3]
    perc_against_party = election_data[4]
    incumbent = people.Senator(person, True, seniority, election_history_1, election_history_2, perc_with_party, perc_against_party)
    return incumbent

def check_incumbent(incumbent, candidate):
    incumbent_name = incumbent.person.name.split(" ")
    candidate_name = candidate.person.name.split(" ")
    if not(len(incumbent_name) == 3 and len(candidate_name) == 2):
        return False
    if(incumbent_name[0] == candidate_name[0] and incumbent_name[2] == candidate_name[1]):
        return True
    return False

def make_candidate(state, election_data):
    name = election_data[0]
    party = election_data[1]
    gender = election_data[3]
    person = people.Person(gender, party, state)
    person.add_name(name)
    perc_votes = election_data[2]
    funding = election_data[4]
    candidate = people.Candidate(person, perc_votes, funding)
    return candidate

class ElectionYear:
    def __init__(self, year):
        self.elections = []
        self.year = year

    def add_election(self, election_data):
        state = election_data[1].strip()
        # GET INCUMBENT
        person = make_person(state, election_data[0:7])
        incumbent = make_incumbent(person, election_data[7:12])
        # GET CANDIDATES
        candidate1 = make_candidate(state, election_data[14:19])
        candidate1.is_incumbent = check_incumbent(incumbent, candidate1)

        candidate2 = make_candidate(state, election_data[21:26])
        candidate2.is_incumbent = check_incumbent(incumbent, candidate2)


        # MAKE ELECTION
        election = Election(state, election_data[0])
        if(election_data[2] != ""):
            election.add_incumbent(incumbent)
        if(candidate1.person.name != None):
            election.add_candidate(candidate1)
        if(candidate2.person.name != None):
            election.add_candidate(candidate2)

        self.elections.append(election)

    def print(self):
        print(self.year)
        for each in self.elections:
            each.print()
