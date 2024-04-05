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
            Official='#C92D4B',
            Default=('#900000', '#5f0000')
        )
    ),
    'alphatauri': Team(
        ShortName='AlphaTauri',
        TeamColor=TeamColors(
            Official='#5E8FAA',
            Default=('#2b4562', '#406991')
        )
    ),
    'alpine': Team(
        ShortName='Alpine',
        TeamColor=TeamColors(
            Official='#2293D1',
            Default=('#fe86bc', '#ff117c')
        )
    ),
    'aston martin': Team(
        ShortName='Aston',
        TeamColor=TeamColors(
            Official='#358C75',
            Default=('#00665e', '#00413b')
        )
    ),
    'ferrari': Team(
        ShortName='Ferrari',
        TeamColor=TeamColors(
            Official='#F91536',
            Default=('#da291c', '#e84d40')
        )
    ),
    'haas': Team(
        ShortName='Haas',
        TeamColor=TeamColors(
            Official='#B6BABD',
            Default=('#ffffff', '#a7a7a7')
        )
    ),
    'mclaren': Team(
        ShortName='McLaren',
        TeamColor=TeamColors(
            Official='#F58020',
            Default=('#ff8000', '#9d4d00')
        )
    ),
    'mercedes': Team(
        ShortName='Mercedes',
        TeamColor=TeamColors(
            Official='#6CD3BF',
            Default=('#00f5d0', '#a8fff2')
        )
    ),
    'red bull': Team(
        ShortName='Red Bull',
        TeamColor=TeamColors(
            Official='#3671C6',
            Default=('#fcd700', '#ffec7b')
        )
    ),
    'williams': Team(
        ShortName='Williams',
        TeamColor=TeamColors(
            Official='#37BEDD',
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
