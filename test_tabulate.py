import tabulate
import pytest


def test_load_voters():
    voters = tabulate.load_voters("RankedChoiceSample.xlsx")
    assert len(voters) == 3
    assert voters[0].remaining_votes == ['A', 'B', 'C', 'D']
    assert voters[1].remaining_votes == ['D', 'C', 'B', 'A']
    assert voters[2].remaining_votes == ['A', 'C', 'B', 'D']


def test_run_round_winner():
    voters = [tabulate.Voter(['A', 'B', 'C', 'D']),
              tabulate.Voter(['D', 'C', 'B', 'A']),
              tabulate.Voter(['A', 'C', 'B', 'D'])]
    r1 = tabulate.Round(voters)
    assert not r1.run_round()
    assert r1.get_active_candidates() == ['A', 'D']
    r2 = tabulate.Round(voters)
    assert r2.run_round()
    assert r2.get_active_candidates() == ['A']


def test_run_round_tie():
    voters = [tabulate.Voter(['A', 'B', 'C', 'D']),
              tabulate.Voter(['D', 'C', 'B', 'A']),
              tabulate.Voter(['B', 'A', 'C', 'D'])]
    r1 = tabulate.Round(voters)
    assert not r1.run_round()
    r2 = tabulate.Round(voters)
    assert r2.run_round()
    assert r2.get_active_candidates() == ['A', 'B', 'D']


def test_run_multi_round():
    voters = [tabulate.Voter(['A', 'B', 'C', 'D']),
              tabulate.Voter(['A', 'C', 'D', 'B']),
              tabulate.Voter(['D', 'A', 'B', 'C']),
              tabulate.Voter(['B', 'C', 'D', 'A']),
              tabulate.Voter(['B', 'A', 'C', 'D'])]
    r1 = tabulate.Round(voters)
    assert not r1.run_round()
    assert r1.get_active_candidates() == ['A', 'B', 'D']
    r2 = tabulate.Round(voters)
    assert not r2.run_round()
    assert r2.get_active_candidates() == ['A', 'B']
    r3 = tabulate.Round(voters)
    assert r3.run_round()
    assert r3.get_active_candidates() == ['A']


def test_run_multi_round_diff_num_votes():
    voters = [tabulate.Voter(['A', 'B', 'C', 'D']),
              tabulate.Voter(['A', 'C', 'D', 'B']),
              tabulate.Voter(['D', 'C', 'B']),
              tabulate.Voter(['B']),
              tabulate.Voter(['B', 'A', 'C'])]
    r1 = tabulate.Round(voters)
    assert not r1.run_round()
    assert r1.get_active_candidates() == ['A', 'B', 'D']
    r2 = tabulate.Round(voters)
    assert not r2.run_round()
    assert r2.get_active_candidates() == ['A', 'B']
    r3 = tabulate.Round(voters)
    assert r3.run_round()
    assert r3.get_active_candidates() == ['B']


def test_run_multi_round_diff_num_votes_tie():
    voters = [tabulate.Voter(['A', 'B', 'C', 'D']),
              tabulate.Voter(['A', 'C', 'D', 'B']),
              tabulate.Voter(['D']),
              tabulate.Voter(['B', 'C',]),
              tabulate.Voter(['B', 'A', 'C'])]
    r1 = tabulate.Round(voters)
    assert not r1.run_round()
    assert r1.get_active_candidates() == ['A', 'B', 'D']
    r2 = tabulate.Round(voters)
    assert not r2.run_round()
    assert r2.get_active_candidates() == ['A', 'B']
    r3 = tabulate.Round(voters)
    assert r3.run_round()
    assert r3.get_active_candidates() == ['A', 'B']


def test_run_one_round_diff_num_votes_tie():
    voters = [tabulate.Voter(['A', 'B', 'C', 'D']),
              tabulate.Voter(['A', 'C', 'D', 'B']),
              tabulate.Voter(['A']),
              tabulate.Voter(['A', 'C', ]),
              tabulate.Voter(['A', 'B', 'C'])]
    r1 = tabulate.Round(voters)
    assert r1.run_round()
    assert r1.get_active_candidates() == ['A']


def test_duplicate_votes():
    with pytest.raises(Exception):
         tabulate.Voter(['C', 'C', 'B', 'A'])

    v = tabulate.Voter()
    v.add_vote("A")
    v.add_vote("B")
    with pytest.raises(Exception):
        v.add_vote("A")


def test_tabulator():
    t = tabulate.Tabulator()
    voters = [tabulate.Voter(['A', 'B', 'D']),
              tabulate.Voter(['A', 'C', 'D', 'B']),
              tabulate.Voter(['D', 'A', 'B', 'C']),
              tabulate.Voter(['B']),
              tabulate.Voter(['B', 'A', 'C', 'D'])]
    result = t.run(voters)
    assert result == ['A']
