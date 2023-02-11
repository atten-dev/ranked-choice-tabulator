# ranked-choice-tabulator

# Usage
```commandline
usage: tabulate.py [-h] spreadsheet

Tabulates rank choice votes

positional arguments:
  spreadsheet

options:
  -h, --help   show this help message and exit
```
# Example
```commandline
tabulate.py RankedChoiceSample.xlsx
Raw votes, for reference (left side is more preferred):
 [['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A'], ['A', 'C', 'B', 'D']]



Round #1 results:
Tally for this round:
{'A': 2, 'B': 0, 'C': 0, 'D': 1}
Eliminated candidate(s) ['B', 'C'] with the least votes.
Remaining candidate(s): ['A', 'D']

Round #2 results:
Tally for this round:
{'A': 2, 'D': 1}
Eliminated candidate(s) ['D'] with the least votes.
Remaining candidate(s): ['A']

Round #2 is the final round.
Winner is: ['A']
```
