from typing import Dict

from fastf1.plotting._constants.base import (
    Compounds,
    Team,
    TeamColors
)


# TODO: sort all alphabetically


Teams: Dict[str, Team] = {  # TODO: update official colors
    'alpine': Team(
        ShortName='Alpine',
        TeamColor=TeamColors(
            Official='#ff87bc',
            Default=('#fe86bc', '#ff117c')
        )
    ),
    'aston martin': Team(
        ShortName='Aston',
        TeamColor=TeamColors(
            Official='#229971',
            Default=('#00665e', '#00413b')
        )
    ),
    'ferrari': Team(
        ShortName='Ferrari',
        TeamColor=TeamColors(
            Official='#e8002d',
            Default=('#da291c', '#8c1a11')
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
            Official='#ff8000',
            Default=('#ff8000', '#9d4d00')
        )
    ),
    'mercedes': Team(
        ShortName='Mercedes',
        TeamColor=TeamColors(
            Official='#27f4d2',
            Default=('#00f5d0', '#a8fff2')
        )
    ),
    'rb visa': Team(  # TODO: name?
        ShortName='RB',
        TeamColor=TeamColors(
            Official='#6692ff',
            Default=('#1634cb', '#0c207e')  # TODO: update
        )
    ),
    'red bull': Team(
        ShortName='Red Bull',
        TeamColor=TeamColors(
            Official='#3671c6',
            Default=('#fcd700', '#ffec7b')
        )
    ),
    'sauber': Team(
        ShortName='Sauber',
        TeamColor=TeamColors(
            Official='#52e252',
            Default=('#00e701', '#008d01')
        )
    ),
    'williams': Team(
        ShortName='Williams',
        TeamColor=TeamColors(
            Official='#64c4ff',
            Default=('#00a0dd', '#8cc8ff')
        )
    )
}

# TODO: future proofing?
CompoundColors: Dict[Compounds, str] = {
    Compounds.Soft: "#da291c",
    Compounds.Medium: "#ffd12e",
    Compounds.Hard: "#f0f0ec",
    Compounds.Intermediate: "#43b02a",
    Compounds.Wet: "#0067ad",
    Compounds.Unknown: "#00ffff",
    Compounds.TestUnknown: "#434649"
}
