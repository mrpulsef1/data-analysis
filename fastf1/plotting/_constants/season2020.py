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
            Official='#9B0000',
            Default=('#900000', '#5f0000')
        )
    ),
    'alphatauri': Team(
        ShortName='AlphaTauri',
        TeamColor=TeamColors(
            Official='#ffffff',
            Default=('#2b4562', '#406991')
        )
    ),
    'ferrari': Team(
        ShortName='Ferrari',
        TeamColor=TeamColors(
            Official='#DC0000',
            Default=('#da291c', '#e84d40')
        )
    ),
    'haas': Team(
        ShortName='Haas',
        TeamColor=TeamColors(
            Official='#787878',
            Default=('#ffffff', '#a7a7a7')
        )
    ),
    'mclaren': Team(
        ShortName='McLaren',
        TeamColor=TeamColors(
            Official='#FF8700',
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
    'racing point': Team(
        ShortName='Racing Point',
        TeamColor=TeamColors(
            Official='#F596C8',
            Default=('#00665e', '#00413b')
        )
    ),
    'red bull': Team(
        ShortName='Red Bull',
        TeamColor=TeamColors(
            Official='#1E41FF',
            Default=('#fcd700', '#ffec7b')
        )
    ),
    'renault': Team(
        ShortName='Renault',
        TeamColor=TeamColors(
            Official='#FFF500',
            Default=('#fe86bc', '#ff117c')
        )
    ),
    'williams': Team(
        ShortName='Williams',
        TeamColor=TeamColors(
            Official='#0082fa',
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
