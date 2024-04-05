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
            Official='#b12039',
            Default=('#900000', '#5f0000')
        )
    ),
    'alphatauri': Team(
        ShortName='AlphaTauri',
        TeamColor=TeamColors(
            Official='#4e7c9b',
            Default=('#2b4562', '#406991')
        )
    ),
    'alpine': Team(
        ShortName='Alpine',
        TeamColor=TeamColors(
            Official='#2293d1',
            Default=('#fe86bc', '#ff117c')
        )
    ),
    'aston martin': Team(
        ShortName='Aston',
        TeamColor=TeamColors(
            Official='#2d826d',
            Default=('#00665e', '#00413b')
        )
    ),
    'ferrari': Team(
        ShortName='Ferrari',
        TeamColor=TeamColors(
            Official='#ed1c24',
            Default=('#da291c', '#e84d40')
        )
    ),
    'haas': Team(
        ShortName='Haas',
        TeamColor=TeamColors(
            Official='#b6babd',
            Default=('#ffffff', '#a7a7a7')
        )
    ),
    'mclaren': Team(
        ShortName='McLaren',
        TeamColor=TeamColors(
            Official='#f58020',
            Default=('#ff8000', '#9d4d00')
        )
    ),
    'mercedes': Team(
        ShortName='Mercedes',
        TeamColor=TeamColors(
            Official='#6cd3bf',
            Default=('#00f5d0', '#a8fff2')
        )
    ),
    'red bull': Team(
        ShortName='Red Bull',
        TeamColor=TeamColors(
            Official='#1e5bc6',
            Default=('#fcd700', '#ffec7b')
        )
    ),
    'williams': Team(
        ShortName='Williams',
        TeamColor=TeamColors(
            Official='#37bedd',
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
