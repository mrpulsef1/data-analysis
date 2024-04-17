import warnings

import pytest


with warnings.catch_warnings():
    warnings.simplefilter("ignore", FutureWarning)
    from fastf1.plotting import (
        DRIVER_COLORS,
        DRIVER_TRANSLATE,
        TEAM_COLORS,
        TEAM_TRANSLATE
    )


def test_team_colors_dict_warning():
    with pytest.raises(KeyError):
        with pytest.warns(UserWarning):
            TEAM_COLORS['Ferrari']

    with pytest.warns(UserWarning):
        TEAM_COLORS.get('Ferrari', None)

    TEAM_COLORS['ferrari']
    TEAM_COLORS.get('ferrari', None)


def test_team_color_name_abbreviation_integrity():
    for value in TEAM_TRANSLATE.values():
        assert value in TEAM_COLORS
    assert len(TEAM_COLORS) == len(TEAM_TRANSLATE)


def test_driver_color_name_abbreviation_integrity():
    for value in DRIVER_TRANSLATE.values():
        assert value in DRIVER_COLORS
    assert len(DRIVER_COLORS) == len(DRIVER_TRANSLATE)
