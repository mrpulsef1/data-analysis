import unicodedata
from typing import (
    Dict,
    List,
    Sequence,
    Tuple
)

from thefuzz import fuzz


class _Driver:
    value: str
    normalized_value: str
    abbreviation: str
    team: "_Team"


class _Team:
    value: str
    normalized_value: str

    def __init__(self):
        super().__init__()
        self.drivers: List["_Driver"] = list()

    @property
    def abbreviations(self) -> Tuple[str, ...]:
        return tuple([drv.abbreviation for drv in self.drivers])


class _DriverTeamMapping:
    def __init__(
            self,
            year: str,
            teams: List[_Team],
    ):
        self.year = year
        self.teams = teams

        self.drivers_by_normalized: Dict[str, _Driver] = dict()
        self.drivers_by_abbreviation: Dict[str, _Driver] = dict()
        self.teams_by_normalized: Dict[str, _Team] = dict()

        for team in teams:
            for driver in team.drivers:
                self.drivers_by_normalized[driver.normalized_value] = driver
                self.drivers_by_abbreviation[driver.abbreviation] = driver
            self.teams_by_normalized[team.normalized_value] = team


def _fuzzy_matcher[S: str](identifier: str, reference: Sequence[S]) -> S:
    # do fuzzy string matching
    key_ratios = list()
    for existing_key in reference:
        ratio = fuzz.ratio(identifier, existing_key)
        key_ratios.append((ratio, existing_key))
    key_ratios.sort(reverse=True)
    if ((key_ratios[0][0] < 35)
            or (key_ratios[0][0] / key_ratios[1][0] < 1.2)):
        # ensure that the best match has a minimum accuracy (35 out of
        # 100) and that it has a minimum confidence (at least 20%
        # better than second best)
        raise KeyError
    best_matched_key = key_ratios[0][1]
    return best_matched_key


def _normalize_string(name: str) -> str:
    # removes accents from a string and returns the closest possible
    # ascii representation (https://stackoverflow.com/a/518232)
    stripped = ''.join(c for c in unicodedata.normalize('NFD', name)
                       if unicodedata.category(c) != 'Mn')
    return stripped
