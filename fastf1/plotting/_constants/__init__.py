from typing import Dict

from fastf1.plotting._constants import (
    season2023,
    season2024
)
from fastf1.plotting._constants.base import BaseSeason


Constants: Dict[str, BaseSeason] = {
    '2023': BaseSeason(CompoundColors=season2023.CompoundColors,
                       Teams=season2023.Teams),
    '2024': BaseSeason(CompoundColors=season2024.CompoundColors,
                       Teams=season2024.Teams),
}


# Deprecated, will be removed for 2025
LEGACY_TEAM_TRANSLATE: Dict[str, str] = {
    'MER': 'mercedes',
    'FER': 'ferrari',
    'RBR': 'red bull',
    'MCL': 'mclaren',
    'APN': 'alpine',
    'AMR': 'aston martin',
    'SAU': 'sauber',
    'RB': 'rb',
    'HAA': 'haas',
    'WIL': 'williams'
}
