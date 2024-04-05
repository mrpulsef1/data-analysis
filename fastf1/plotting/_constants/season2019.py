from typing import Dict

from fastf1.plotting._constants.base import (
    Compounds,
    Team,
    TeamColors
)


Teams: Dict[str, Team] = {
    'alfa romeo': Team(
        ShortName='Alfa Romeo',
        TeamColor=TeamColors(
            Official='#9b0000',
            Default=('#900000', '#5f0000')
        )
    ),
    'haas': Team(
        ShortName='Haas',
        TeamColor=TeamColors(
            Official='#bd9e57',
            Default=('#ffffff', '#a7a7a7')
        )
    ),
    'ferrari': Team(
        ShortName='Ferrari',
        TeamColor=TeamColors(
            Official='#dc0000',
            Default=('#da291c', '#e84d40')
        )
    ),
    'mclaren': Team(
        ShortName='McLaren',
        TeamColor=TeamColors(
            Official='#ff8700',
            Default=('#ff8000', '#9d4d00')
        )
    ),
    'mercedes': Team(
        ShortName='Mercedes',
        TeamColor=TeamColors(
            Official='#00d2be',
            Default=('#00f5d0', '#a8fff2')
        )
    ),
    'racing point': Team(
        ShortName='Racing Point',
        TeamColor=TeamColors(
            Official='#f596c8',
            Default=('#00665e', '#00413b')
        )
    ),
    'red bull': Team(
        ShortName='Red Bull',
        TeamColor=TeamColors(
            Official='#1e41ff',
            Default=('#fcd700', '#ffec7b')
        )
    ),
    'renault': Team(
        ShortName='Renault',
        TeamColor=TeamColors(
            Official='#fff500',
            Default=('#fe86bc', '#ff117c')
        )
    ),
    'toro rosso': Team(
        ShortName='Toro Rosso',
        TeamColor=TeamColors(
            Official='#469bff',
            Default=('#2b4562', '#406991')
        )
    ),
    'williams': Team(
        ShortName='Williams',
        TeamColor=TeamColors(
            Official='#ffffff',
            Default=('#00a0dd', '#8cc8ff')
        )
    )
}

CompoundColors: Dict[Compounds, str] = {
    Compounds.Soft: "#da291c",
    Compounds.Medium: "#ffd12e",
    Compounds.Hard: "#f0f0ec",
    Compounds.Intermediate: "#43b02a",
    Compounds.Wet: "#0067ad",
    Compounds.Unknown: "#00ffff",
    Compounds.TestUnknown: "#434649"
}
