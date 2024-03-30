from typing import Dict

from fastf1.plotting._constants.base import (
    Compounds,
    Team,
    TeamColors
)


# TODO: sort all alphabetically


Teams: Dict[str, Team] = {  # TODO: update official colors
    'mercedes': Team(
        ShortName='Mercedes',
        TeamColor=TeamColors(
            # Classic='#00d2be',
            Official='#27f4d2',
            # Default=('#00f5d0', '#a8fff2')
        )
    ),
    'ferrari': Team(
        ShortName='Ferrari',
        TeamColor=TeamColors(
            # Classic='#dc0000',
            Official='#e8002d',
            # Default=('#da291c', '#8c1a11')
        )
    ),
    'red bull': Team(
        ShortName='Red Bull',
        TeamColor=TeamColors(
            # Classic='#0600ef',
            Official='#3671c6',
            # Default=('#fcd700', '#ffec7b')
        )
    ),
    'mclaren': Team(
        ShortName='McLaren',
        TeamColor=TeamColors(
            # Classic='#ff8700',
            Official='#ff8000',
            # Default=('#ff8000', '#9d4d00')
        )
    ),
    'alpine': Team(
        ShortName='Alpine',
        TeamColor=TeamColors(
            # Classic='#0090ff',
            Official='#ff87bc',
            # Default=('#fe86bc', '#ff117c')
        )
    ),
    'aston martin': Team(
        ShortName='Aston',
        TeamColor=TeamColors(
            # Classic='#006f62',
            Official='#229971',
            # Default=('#00665e', '#00413b')
        )
    ),
    'sauber': Team(
        ShortName='Sauber',
        TeamColor=TeamColors(
            # Classic='#00e701',
            Official='#52e252',
            # Default=('#00e701', '#008d01')
        )
    ),
    'rb visa': Team(  # TODO: name?
        ShortName='RB',
        TeamColor=TeamColors(
            # Classic='#1434CB',  # TODO: update
            Official='#6692ff',
            # Default=('#1634cb', '#0c207e')  # TODO: update
        )
    ),
    'haas': Team(
        ShortName='Haas',
        TeamColor=TeamColors(
            # Classic='#ffffff',
            Official='#b6babd',
            # Default=('#ffffff', '#a7a7a7')
        )
    ),
    'williams': Team(
        ShortName='Williams',
        TeamColor=TeamColors(
            # Classic='#005aff',
            Official='#64c4ff',
            # Default=('#00a0dd', '#8cc8ff')
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
