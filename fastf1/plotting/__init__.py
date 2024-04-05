import warnings
from typing import (
    Dict,
    List
)

from fastf1.core import Session
from fastf1.plotting._constants import LEGACY_TEAM_TRANSLATE as _LTT
from fastf1.plotting._constants import Constants as _Constants
from fastf1.plotting._constants.base import Compounds as _Compounds
from fastf1.plotting._interface import (  # noqa: F401
    _get_driver_team_mapping,
    add_sorted_driver_legend,
    get_driver_abbreviation,
    get_driver_abbreviations_by_team,
    get_driver_color,
    get_driver_name,
    get_driver_names_by_team,
    get_driver_style,
    get_team_color,
    get_team_name,
    get_team_name_by_driver
)
from fastf1.plotting._plotting import (  # noqa: F401
    _COLOR_PALETTE,
    driver_color,
    lapnumber_axis,
    setup_mpl,
    team_color
)


def __getattr__(name):
    if name in ('COMPOUND_COLORS', 'DRIVER_TRANSLATE', 'DRIVER_COLORS',
                'TEAM_COLORS', 'TEAM_TRANSLATE', 'COLOR_PALETTE'):
        warnings.warn(f"{name} is deprecated and will be removed in a future"
                      f"version.", FutureWarning)

        if ((name == 'DRIVER_TRANSLATE')
                and ('_DEPR_DRIVER_TRANSLATE' not in globals())):
            _load_depr_driver_translate()

        if ((name == 'DRIVER_COLORS')
                and ('_DEPR_DRIVER_COLORS' not in globals())):
            _load_depr_driver_colors()

        return globals()[f"_DEPR_{name}"]

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


_DEPR_COMPOUND_COLORS: Dict[str, str] = {
    str(key.value): val for key, val
    in _Constants['2024'].CompoundColors.items()
}
COMPOUND_COLORS: Dict[str, str]
"""
Mapping of tyre compound names to compound colors (hex color codes).
(current season only)

.. deprecated:: 3.3.0
    The ``COMPOUND_COLORS`` dictionary is deprecated and will be removed in a
    future version. Use :func:`~fastf1.plotting.get_compound_color` instead.
"""


def _load_depr_driver_colors():
    global _DEPR_DRIVER_COLORS

    dtm = _get_driver_team_mapping(session=None)
    name_to_color = dict()
    for driver in dtm.drivers_by_abbreviation.values():
        name_to_color[driver.normalized_value.lower()] \
            = get_driver_color(driver.abbreviation, session=None)
    _DEPR_DRIVER_COLORS = name_to_color


_DEPR_DRIVER_COLORS: Dict[str, str]
DRIVER_COLORS: Dict[str, str]
"""
Mapping of driver names to driver colors (hex color codes).

.. warning::
    This dictionary is created based on the drivers that participated in the
    latest session. Therefore, it is not static and not fully backwards
    compatible with FastF1 before v3.4.0.

.. deprecated:: 3.3.0
    The ``DRIVER_COLORS`` dictionary is deprecated and will ber removed in a
    future version. Use :func:`~fastf1.plotting.get_driver_color` instead.
"""


def _load_depr_driver_translate():
    global _DEPR_DRIVER_TRANSLATE

    dtm = _get_driver_team_mapping(session=None)
    abb_to_name = dict()
    for abbreviation, driver in dtm.drivers_by_abbreviation.items():
        abb_to_name[abbreviation] = driver.normalized_value.lower()
    _DEPR_DRIVER_TRANSLATE = abb_to_name


_DEPR_DRIVER_TRANSLATE: Dict[str, str]
DRIVER_TRANSLATE: Dict[str, str]
"""
Mapping of driver names to theirs respective abbreviations.

.. deprecated:: 3.3.0
    The ``DRIVER_TRANSLATE`` dictionary is deprecated and will be removed in a
    future version. Use :func:`~fastf1.plotting.get_driver_name` instead.
"""

_DEPR_TEAM_COLORS: Dict[str, str] = {
    # str(key.value): val for key, val
    # in _Constants['2024'].Colormaps[_Colormaps.Default].items()
    name: team.TeamColor.Default[0] for name, team
    in _Constants['2024'].Teams.items()
}
TEAM_COLORS: Dict[str, str]
"""
Mapping of team names to team colors (hex color codes).
(current season only)

.. deprecated:: 3.3.0
    The ``TEAM_COLORS`` dictionary is deprecated and will be removed in a
    future version. Use :func:`~fastf1.plotting.get_team_color` instead.
"""

_DEPR_TEAM_TRANSLATE: Dict[str, str] = {
    str(key): val for key, val in _LTT.items()
}
TEAM_TRANSLATE: Dict[str, str]
"""
Mapping of team names to theirs respective abbreviations.

.. deprecated:: 3.3.0
    The ``TEAM_TRANSLATE`` dictionary is deprecated and will be removed in a
    future version. Use :func:`~fastf1.plotting.get_team_name` instead.
"""

_DEPR_COLOR_PALETTE: List[str] = _COLOR_PALETTE.copy()
COLOR_PALETTE: List[str]
"""
The default color palette for matplotlib plot lines in fastf1's color scheme.

.. deprecated:: 3.3.0
    The ``COLOR_PALETTE`` list is deprecated and will be removed in a
    future version with no replacement.
"""


def get_compound_color(compound: str, *, session: Session) -> str:
    """
    Get the compound color as hexadecimal RGB color code for a given compound.

    Args:
        compound: The name of the compound
        session: the session for which the data should be obtained

    Returns: A hexadecimal RGB color code
    """
    year = str(session.event['EventDate'].year)
    return _Constants[year].CompoundColors[_Compounds(compound.upper())]
