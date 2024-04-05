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
            Official='#900000',
            Default=('#900000', '#5f0000')
        )
    ),
    'alphatauri': Team(
        ShortName='AlphaTauri',
        TeamColor=TeamColors(
            Official='#2B4562',
            Default=('#2b4562', '#406991')
        )
    ),
    'alpine': Team(
        ShortName='Alpine',
        TeamColor=TeamColors(
            Official='#0090FF',
            Default=('#fe86bc', '#ff117c')
        )
    ),
    'aston martin': Team(
        ShortName='Aston',
        TeamColor=TeamColors(
            Official='#006F62',
            Default=('#00665e', '#00413b')
        )
    ),
    'ferrari': Team(
        ShortName='Ferrari',
        TeamColor=TeamColors(
            Official='#DC0004',
            Default=('#da291c', '#e84d40')
        )
    ),
    'haas': Team(
        ShortName='Haas',
        TeamColor=TeamColors(
            Official='#FFFFFF',
            Default=('#ffffff', '#a7a7a7')
        )
    ),
    'mclaren': Team(
        ShortName='McLaren',
        TeamColor=TeamColors(
            Official='#FF9800',
            Default=('#ff8000', '#9d4d00')
        )
    ),
    'mercedes': Team(
        ShortName='Mercedes',
        TeamColor=TeamColors(
            Official='#00D2BE',
            Default=('#00f5d0', '#a8fff2')
        )
    ),
    'red bull': Team(
        ShortName='Red Bull',
        TeamColor=TeamColors(
            Official='#0600EF',
            Default=('#fcd700', '#ffec7b')
        )
    ),
    'williams': Team(
        ShortName='Williams',
        TeamColor=TeamColors(
            Official='#005AFF',
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
