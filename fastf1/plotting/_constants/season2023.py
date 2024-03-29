from typing import Dict

from fastf1.plotting._constants.base import (
    Compounds,
    Team,
    TeamColors
)


Teams: Dict[str, Team] = {
    'mercedes': Team(
        ShortName='Mercedes',
        TeamColor=TeamColors(
            Classic='#00d2be',
            Official='#6CD3BF',
            Default=('#00f5d0', '#a8fff2')
        )
    ),
    'ferrari': Team(
        ShortName='Ferrari',
        TeamColor=TeamColors(
            Classic='#dc0000',
            Official='#F91536',
            Default=('#da291c', '#e84d40')
        )
    ),
    'red bull': Team(
        ShortName='Red Bull',
        TeamColor=TeamColors(
            Classic='#0600ef',
            Official='#3671C6',
            Default=('#fcd700', '#ffec7b')
        )
    ),
    'mclaren': Team(
        ShortName='McLaren',
        TeamColor=TeamColors(
            Classic='#ff8700',
            Official='#F58020',
            Default=('#ff8000', '#9d4d00')
        )
    ),
    'alpine': Team(
        ShortName='Alpine',
        TeamColor=TeamColors(
            Classic='#0090ff',
            Official='#2293D1',
            Default=('#fe86bc', '#ff117c')
        )
    ),
    'aston martin': Team(
        ShortName='Aston',
        TeamColor=TeamColors(
            Classic='#006f62',
            Official='#358C75',
            Default=('#00665e', '#00413b')
        )
    ),
    'alfa romeo': Team(
        ShortName='Alfa Romeo',
        TeamColor=TeamColors(
            Classic='#900000',
            Official='#900000',
            Default=('#900000', '#5f0000')
        )
    ),
    'alphatauri': Team(
        ShortName='AlphaTauri',
        TeamColor=TeamColors(
            Classic='#2b4562',
            Official='#5E8FAA',
            Default=('#2b4562', '#406991')
        )
    ),
    'haas': Team(
        ShortName='Haas',
        TeamColor=TeamColors(
            Classic='#ffffff',
            Official='#B6BABD',
            Default=('#ffffff', '#a7a7a7')
        )
    ),
    'williams': Team(
        ShortName='Williams',
        TeamColor=TeamColors(
            Classic='#005aff',
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

