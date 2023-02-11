import argparse
import pathlib
import sys

import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Tabulates rank choice votes")
    parser.add_argument('spreadsheet', type=pathlib.Path)
    args = parser.parse_args()

    voters = load_voters(args.spreadsheet)
    t = Tabulator()
    t.run(voters)


class Voter:
    def __init__(self, votes=None):
        if votes is None:
            self.original_votes = []
            self.remaining_votes = []
        else:
            self.original_votes = votes
            self.remaining_votes = votes
            if len(self.remaining_votes) != len(set(self.remaining_votes)):
                raise Exception("Error: candidate found multiple times in one voter")

    def add_vote(self, vote: str):
        self.original_votes.append(vote)  # Original votes not currently used
        self.remaining_votes.append(vote)
        if len(self.remaining_votes) != len(set(self.remaining_votes)):
            raise Exception("Error: candidate found multiple times in one voter")

    def __repr__(self):
        return str(self.remaining_votes)


class Round:
    def __init__(self, voters: list[Voter]):
        """NOTE: Callers voters list passed in here will be modified by run_round! """
        self.eliminated = []
        self.voters = voters
        self.this_round_tally = dict()

    def run_round(self) -> bool:
        """ Returns true if winner(s) found. Modifies voters that was passed to the ctor! """
        for c in self.get_active_candidates():
            self.this_round_tally[c] = 0

        for v in self.voters:
            if len(v.remaining_votes) > 0:
                self.this_round_tally[v.remaining_votes[0]] += 1

        self.eliminated = self.get_least_voted_candidates()

        if len(self.eliminated) == len(self.get_active_candidates()):
            # All remaining candidates tie for least number of votes, return true
            return True

        # Else we continue to remove the least voted candidates and check if only 1 is left
        for e in self.eliminated:
            for v in self.voters:
                if v.remaining_votes.count(e) > 0:
                    v.remaining_votes.remove(e)

        if len(self.get_active_candidates()) == 1:
            return True

        return False

    def get_least_voted_candidates(self):
        min_candidates = []
        min_votes = sys.maxsize
        for c, votes in self.this_round_tally.items():
            if votes == min_votes:
                min_candidates.append(c)
            if votes < min_votes:
                # Reset
                min_candidates = [c]
                min_votes = votes

        return min_candidates

    def get_active_candidates(self):
        active_candidates = []
        for v in self.voters:
            for c in v.remaining_votes:
                if c not in active_candidates:
                    active_candidates.append(c)

        return active_candidates

    def results(self):
        result_str = ""
        result_str += "Tally for this round:\n" + str(self.this_round_tally) + "\n"
        result_str += f"Eliminated candidate(s) {self.eliminated} with the least votes.\n"
        result_str += f"Remaining candidate(s): {self.get_active_candidates()}\n"

        return result_str


class Tabulator:
    def run(self, voters: list[Voter]):
        print(f"Raw votes, for reference (left side is more preferred):\n {voters}\n\n\n")

        done = False
        i = 1
        while not done:
            r = Round(voters)
            done = r.run_round()
            print(f"Round #{i} results:\n{r.results()}")
            if done:
                print(f"Round #{i} is the final round.")
            i += 1
        winners = r.get_active_candidates()
        print(f"Winner{len(winners) == 1 and ' is' or 's are'}: {winners}")
        return winners


def load_voters(path: pathlib.Path) -> list[Voter]:
    dataframe = pd.read_excel(path, skiprows=3)
    voters = []
    curr_voter = None
    dataframe.reset_index()
    for index, row in dataframe.iterrows():
        if index == 0:
            continue  # Skip first row which just has the question
        user = row['USER ID']
        if not pd.isna(user):
            if curr_voter:
                voters.append(curr_voter)
            curr_voter = Voter()
        curr_voter.add_vote(row['ANSWER'])
    if curr_voter:
        voters.append(curr_voter)
    return voters


if __name__ == "__main__":
    main()