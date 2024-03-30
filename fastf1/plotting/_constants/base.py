from dataclasses import dataclass
from enum import Enum
from typing import (
    Dict,
    Tuple
)


class Compounds(Enum):
    HyperSoft = "HYPERSOFT"
    UltraSoft = "ULTRASOFT"
    SuperSoft = "SUPERSOFT"
    Soft = "SOFT"
    Medium = "MEDIUM"
    Hard = "HARD"
    SuperHard = "SUPERHARD"
    Intermediate = "INTERMEDIATE"
    Wet = "WET"
    Unknown = "UNKNOWN"
    TestUnknown = "TEST-UNKNOWN"


@dataclass(frozen=True)
class TeamColors:
    Classic: str
    Official: str
    Default: Tuple[str, str]


@dataclass(frozen=True)
class Team:
    ShortName: str
    TeamColor: TeamColors


@dataclass(frozen=True)
class BaseSeason:
    CompoundColors: Dict[Compounds, str]
    Teams: dict[str, Team]
