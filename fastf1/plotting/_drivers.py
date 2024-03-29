import json
import unicodedata
from typing import (
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Union
)

import matplotlib.axes
from thefuzz import fuzz

import fastf1._api
from fastf1.core import Session
from fastf1.plotting._constants import Constants
from fastf1.plotting._constants.base import Colormaps
from fastf1.req import Cache


class _Driver:
    value: str
    normalized_value: str
    abbreviation: str
    team: "_Team"


class _Team:
    value: str
    normalized_value: str

    def __init__(self):
        super().__init__()
        self.drivers: List["_Driver"] = list()

    @property
    def abbreviations(self) -> Tuple[str, ...]:
        return tuple([drv.abbreviation for drv in self.drivers])


class _DriverTeamMapping:
    def __init__(
            self,
            year: str,
            teams: List[_Team],
    ):
        self.year = year
        self.teams = teams

        self.drivers_by_normalized: Dict[str, _Driver] = dict()
        self.drivers_by_abbreviation: Dict[str, _Driver] = dict()
        self.teams_by_normalized: Dict[str, _Team] = dict()

        for team in teams:
            for driver in team.drivers:
                self.drivers_by_normalized[driver.normalized_value] = driver
                self.drivers_by_abbreviation[driver.abbreviation] = driver
            self.teams_by_normalized[team.normalized_value] = team


_DRIVER_TEAM_MAPPINGS = dict()


def _get_latest_api_path() -> (str, str):
    # find out what the "current" season is; this is the latest season
    # for which data is available, therefore before the first session
    # of any year, the "current" season is still last year
    res_seasons = Cache.requests_get(
        'https://livetiming.formula1.com/static/Index.json'
    )
    if res_seasons.status_code != 200:
        raise ValueError("Unable to fetch driver list")
    year = str(json.loads(
        res_seasons.content.decode('utf-8-sig')
    )['Years'][-1].get('Year'))
    # find the latest session of the current season
    res_meetings = Cache.requests_get(
        f'https://livetiming.formula1.com/static/{year}/Index.json'
    )
    if res_meetings.status_code != 200:
        raise ValueError("Unable to fetch driver list")
    meeting_info = json.loads(res_meetings.content.decode('utf-8-sig'))
    n_meetings = len(meeting_info.get('Meetings', []))
    # iterate over all session of the season in reverse and find the
    # latest session that has an api path (not necessarily every
    # session has that in case of error or if teh session is testing)
    path = None
    for i in range(n_meetings):
        sessions = meeting_info['Meetings'][-(i + 1)]['Sessions']
        for j in range(len(sessions)):
            path = sessions[-(j + 1)].get('Path', None)
            if path is not None:
                break
        if path is not None:
            break

    api_path = "/static/" + path

    return api_path, year


def _load_drivers_from_f1_livetiming(
        *, api_path: str, year: str
) -> List[_Team]:
    # load the driver information for the determined session
    driver_info = fastf1._api.driver_info(api_path)

    # parse the data into the required format
    teams: Dict[str, _Team] = dict()

    for num, driver_entry in driver_info.items():
        team_name = driver_entry.get('TeamName')

        if team_name in teams:
            team = teams[team_name]
        else:
            team = _Team()
            team.value = team_name

        abbreviation = driver_entry.get('Tla')

        name = ' '.join((driver_entry.get('FirstName'),
                         driver_entry.get('LastName')))
        driver = _Driver()
        driver.value = name
        driver.normalized_value = _normalize_string(name)
        driver.abbreviation = abbreviation
        driver.team = team

        team.drivers.append(driver)

        if team not in teams:
            normalized_full_team_name = _normalize_string(team_name).lower()
            for ref in Constants[year].Teams:
                # TODO: handle unknown teams
                if ref.value in normalized_full_team_name:
                    team.normalized_value = ref.value
            teams[team_name] = team

    return list(teams.values())


def _get_driver_team_mapping(
        session: Optional[Session] = None
) -> "_DriverTeamMapping":

    if session is None:
        api_path, year = _get_latest_api_path()
    else:
        api_path = session.api_path
        year = str(session.event['EventDate'].year)

    if api_path not in _DRIVER_TEAM_MAPPINGS:
        teams = _load_drivers_from_f1_livetiming(
            api_path=api_path, year=year
        )
        mapping = _DriverTeamMapping(year, teams)
        _DRIVER_TEAM_MAPPINGS[api_path] = mapping

    return _DRIVER_TEAM_MAPPINGS[api_path]


def _fuzzy_matcher[S: str](identifier: str, reference: Sequence[S]) -> S:
    # do fuzzy string matching
    key_ratios = list()
    for existing_key in reference:
        ratio = fuzz.ratio(identifier, existing_key)
        key_ratios.append((ratio, existing_key))
    key_ratios.sort(reverse=True)
    if ((key_ratios[0][0] < 35)
            or (key_ratios[0][0] / key_ratios[1][0] < 1.2)):
        # ensure that the best match has a minimum accuracy (35 out of
        # 100) and that it has a minimum confidence (at least 20%
        # better than second best)
        raise KeyError
    best_matched_key = key_ratios[0][1]
    return best_matched_key


def _normalize_string(name: str) -> str:
    # removes accents from a string and returns the closest possible
    # ascii representation (https://stackoverflow.com/a/518232)
    stripped = ''.join(c for c in unicodedata.normalize('NFD', name)
                       if unicodedata.category(c) != 'Mn')
    return stripped


def _get_driver(identifier, *, session: Session) -> _Driver:
    dtm = _get_driver_team_mapping(session)
    identifier = _normalize_string(identifier).lower()

    # try driver abbreviation first
    if (abb := identifier.upper()) in dtm.drivers_by_abbreviation:
        return dtm.drivers_by_abbreviation[abb]

    # check for an exact driver name match
    if identifier in dtm.drivers_by_normalized:
        return dtm.drivers_by_normalized[identifier]

    # check for exact partial string match
    for normalized_driver in dtm.drivers_by_normalized.keys():
        if identifier in normalized_driver:
            return dtm.drivers_by_normalized[normalized_driver]

    # do fuzzy string matching
    normalized_driver = _fuzzy_matcher(identifier,
                                       list(dtm.drivers_by_normalized.keys()))
    return dtm.drivers_by_normalized[normalized_driver]


def _get_team(
        identifier: str,
        *,
        session: Session
) -> _Team:
    dtm = _get_driver_team_mapping(session)
    identifier = _normalize_string(identifier).lower()

    team_name: Optional[str] = None

    # check for an exact team name match
    if identifier in dtm.teams_by_normalized.keys():
        return dtm.teams_by_normalized[identifier]

    # check for exact partial string match
    for normalized_team in dtm.teams_by_normalized.keys():
        if identifier in normalized_team:
            return dtm.teams_by_normalized[normalized_team]

    # do fuzzy string match
    team_name = _fuzzy_matcher(identifier,
                               list(dtm.teams_by_normalized.keys()))
    return dtm.teams_by_normalized[team_name]


def _get_team_color(
            identifier: str,
            *,
            session: Session,
            colormap: str = 'default',
            _variant: int = 0  # internal use only
    ):
    if (_variant != 0) and (colormap != 'default'):
        raise ValueError("Color variants are only supported on the "
                         "'default' colormap.")

    dtm = _get_driver_team_mapping(session)

    if dtm.year not in Constants.keys():
        raise ValueError(f"No team colors for year '{dtm.year}'")

    named_colormap = Colormaps(colormap)

    colormaps = Constants[dtm.year].Colormaps
    if named_colormap not in colormaps.keys():
        raise ValueError(f"Invalid colormap '{colormap}'")

    team_name = _get_team(identifier, session=session).normalized_value
    named_team = Constants[dtm.year].Teams(team_name)

    if named_team not in colormaps[named_colormap].keys():
        raise ValueError(f"Invalid team name '{team_name}'")

    return colormaps[named_colormap][named_team][_variant]


def get_team_name(
        identifier: str,
        *,
        session: Session,
        short: bool = False
) -> str:
    """
    Get a full team name based on a recognizable and identifiable part of
    the team name.

    Alternatively, a shortened version of the team name can be returned. The
    short version is intended for saving as much space as possible when
    annotating plots and may skip parts of the official team name.

    Args:
        identifier: a recognizable part of the team name
        session: the session for which the data should be obtained
        short: if True, a shortened version of the team name will be returned
    """
    team = _get_team(identifier, session=session)

    if short:
        dtm = _get_driver_team_mapping(session)
        named_team = Constants[dtm.year].Teams(team.normalized_value)
        return Constants[dtm.year].ShortTeamNames[named_team]

    return team.value


def get_team_name_by_driver(
        identifier: str,
        *,
        session: Session,
        short: bool = False,
) -> str:
    """
    Get a full team name based on a driver's abbreviation or based on a
    recognizable and identifiable part of a driver's name.

    Alternatively, a shortened version of the team name can be returned. The
    short version is intended for saving as much space as possible when
    annotating plots and may skip parts of the official team name.

    Args:
        identifier: driver abbreviation or recognizable part of the driver name
        session: the session for which the data should be obtained
        short: if True, a shortened version of the team name will be returned
    """
    driver = _get_driver(identifier, session=session)
    team = driver.team

    if short:
        dtm = _get_driver_team_mapping(session)
        named_team = Constants[dtm.year].Teams(team.normalized_value)
        return Constants[dtm.year].ShortTeamNames[named_team]

    return team.value


def get_team_color(
        identifier: str,
        *,
        session: Session,
        colormap: str = 'default',
):
    """
    Get a team color based on a recognizable and identifiable part of
    the team name.

    The team color is returned as a hexadecimal RGB color code.

    Args:
        identifier: a recognizable part of the team name
        session: the session for which the data should be obtained
        colormap: one of ``'default'`` or ``'official'``
    """
    return _get_team_color(identifier, session=session, colormap=colormap)


def get_driver_name(identifier: str, *, session: Session) -> str:
    """
    Get a full driver name based on the driver's abbreviation or based on
    a recognizable and identifiable part of the driver's name.

    Args:
        identifier: driver abbreviation or recognizable part of the driver name
        session: the session for which the data should be obtained
    """
    driver = _get_driver(identifier, session=session)
    return driver.value


def get_driver_abbreviation(identifier, *, session: Session) -> str:
    """
    Get a driver's abbreviation based on a recognizable and identifiable
    part of the driver's name.

    Note that the driver's abbreviation, if given exactly, is also a valid
    identifier. In this case the same value is returned as was given as the
    identifier.

    Args:
        identifier: recognizable part of the driver's name (or the
            driver's abbreviation)
        session: the session for which the data should be obtained
    """
    driver = _get_driver(identifier, session=session)
    return driver.abbreviation


def get_driver_names_by_team(
        identifier: str, *, session: Session
) -> List[str]:
    """
    Get a list of full names of all drivers that drove for a team in a given
    session based on a recognizable and identifiable part of the team name.

    Args:
        identifier: a recognizable part of the team name
        session: the session for which the data should be obtained
    """
    team = _get_team(identifier, session=session)
    return [driver.value for driver in team.drivers]


def get_driver_abbreviations_by_team(
        identifier: str, *, session: Session
) -> List[str]:
    """
    Get a list of abbreviations of all drivers that drove for a team in a given
    session based on a recognizable and identifiable part of the team name.

    Args:
        identifier: a recognizable part of the team name
        session: the session for which the data should be obtained
    """
    team = _get_team(identifier, session=session)
    return [driver.abbreviation for driver in team.drivers]


def _get_driver_color(
        identifier: str,
        *,
        session: Session,
        colormap: str = 'default',
        _variants: bool = False
):
    driver = _get_driver(identifier, session=session)
    team_name = driver.team.normalized_value

    if _variants:
        dtm = _get_driver_team_mapping(session)
        driver_ref = dtm.teams_by_normalized[team_name].drivers
        idx = driver_ref.index(driver)
        if idx > 1:
            idx = 1  # we only have two colors, limit to 0 or 1
        return _get_team_color(team_name, session=session, colormap='default',
                               _variant=idx)
    else:
        return _get_team_color(team_name, session=session, colormap=colormap)


def get_driver_color(
        identifier: str,
        *,
        session: Session,
        colormap: str = 'default',
):
    """
    Get the color that is associated with a driver based on the driver's
    abbreviation or based on a recognizable and identifiable part of the
    driver's name.

    .. note:: This will simply return the team color of the team that the
        driver participated for in this session. Contrary to older versions
        of FastF1, there are no separate colors for each driver!

    Args:
        identifier: driver abbreviation or recognizable part of the driver name
        session: the session for which the data should be obtained
        colormap: one of ``'default'`` or ``'official'``
    """
    return _get_driver_color(identifier, session=session, colormap=colormap)


def get_driver_style(
        identifier: str,
        style: Union[str, List[str], List[dict]],
        *,
        session: Session,
        colormap: str = 'default',
        additional_color_kws: Union[list, tuple] = ()
):
    """
    Get a plotting style that is unique for a driver based on the driver's
    abbreviation or based on a recognizable and identifiable part of the
    driver's name.

    This function simplifies the task of generating unique and easily
    distinguishable visual styles for multiple drivers in a plot.
    Primarily, the focus is on plotting with Matplotlib, but it is possible
    to customize the behaviour for compatibility with other plotting libraries.

    The general idea for creating visual styles is as follows:

    1. Set the primary color of the style to the color of the team for
       which a driver is driving. This may be the line color in a line plot,
       the marker color in a scatter plot, and so on.

    2. Use one or multiple other styling options (line style, markers, ...)
       to differentiate drivers in the same team.

    .. note:: It cannot be guaranteed that the styles are consistent throughout
        a full season, especially in case of driver changes within a team.


    **Option 1**: Rely on built-in styling options

    By default, this function supports the following Matplotlib plot arguments:
    ``linestyle``, ``marker``, ``color``, ``facecolor``, ``edgecolor`` as well
    as almost all other color-related arguments.

    The styling options include one color for each team, up to four different
    line styles and marker styles within a team. That means that no more than
    four different drivers are supported for a team in a single session. This
    should be sufficent in almost all scenarios.

    The following example obtains the driver style for Alonso and Stroll in a
    race in the 2023 season. The drivers should be represented using the
    ``color`` and ``marker`` arguments, as may be useful in a scatter plot.
    Both drivers were driving for the Aston Martin team, therefore, both
    automatically get assigned the same color, which is the Aston Martin team
    color. But both drivers get assigned a different marker style, so they can
    be uniquely identified in the plot.

    Example::
        >>> from fastf1 import get_session
        >>> from fastf1.plotting import get_driver_style
        >>> session = get_session(2023, 10, 'R')
        >>> get_driver_style('ALO', style=['color', 'marker'], session=session)
        {'color': '#00665e', 'marker': 'x'}
        >>> get_driver_style('STR', style=['color', 'marker'], session=session)
        {'color': '#00665e', 'marker': 'o'}

    **Option 2**: Provide a custom list of styling variants

    To allow for almost unlimited styling options, it is possible to specify
    custom styling variants. These are not tied to any specific plotting
    library.

    In the following example, a list with two custom stlyes is defined that are
    then used to generate driver specific styles. Each style is represented by
    a dictionary of keywords and values.

    The first driver in a team gets assigned the first style, the second driver
    the second style and so on (if there are more than two drivers). It is
    necessary to define at least as many styles as there are drivers in a team.

    The following things need to be noted:

    1. The notion of first or second driver does not refer to any particular
    reference and no specific order for drivers within a team is intended or
    guranteed.

    2. Any color-related key can make use of the "magic" ``'auto'`` value as
    shown with Alonso in this example. When the color value is set to
    ``'auto'`` it will automatically be replaced with the team color for this
    driver. All color keywords that are used in Matplotlib should be recognized
    automatically. You can define custom arguments as color arguments through
    the ``additional_color_kws`` argument.

    3. Each style dictionary can contain arbitrary keys and value. Therefore,
    you are not limited to any particular plotting library.

    Example::
        >>> from fastf1 import get_session
        >>> from fastf1.plotting import get_driver_style
        >>> session = get_session(2023, 10, 'R')
        >>> my_styles = [ \
                {'linestyle': 'solid', 'color': 'auto', 'custom_arg': True}, \
                {'linestyle': 'dotted', 'color': '#FF0060', 'other_arg': 10} \
            ]
        >>> get_driver_style('ALO', style=my_styles, session=session)
        {'linestyle': 'solid', 'color': '#00665e', 'custom_arg': True}
        >>> get_driver_style('STR', style=my_styles, session=session)
        {'linestyle': 'dotted', 'color': '#FF0060', 'other_arg': 10}

    .. seealso::
        :ref:`sphx_glr_examples_gallery_plot_driver_styling.py`

    Args:
        identifier: driver abbreviation or recognizable part of the driver name
        style: list of matplotlib plot arguments that should be used for
            styling or a list of custom style dictionaries
        session: the session for which the data should be obtained
        colormap: one of ``'default'`` or ``'official'``
        additional_color_kws: A list of keys that should additionally be
            treated as colors. This is most usefull for making the magic
            ``'auto'`` color work with custom styling options.

    Returns: a dictionary of plot style arguments that can be directly passed
        to a matplotlib plot function using the ``**`` expansion operator
    """
    stylers = {
        'linestyle': ['solid', 'dashed', 'dashdot', 'dotted'],
        'marker': ['x', 'o', '^', 'D']
    }

    # color keyword arguments that are supported by various matplotlib
    # functions
    color_kwargs = (
        # generic
        'color', 'colors', 'c',
        # .plot
        'gapcolor',
        'markeredgecolor', 'mec',
        'markerfacecolor', 'mfc',
        'markerfacecoloralt', 'mfcalt',
        # .scatter
        'facecolor', 'facecolors', 'fc',
        'edgecolor', 'edgecolors', 'ec',
        # .errorbar
        'ecolor',
        # add user defined color keyword arguments
        *additional_color_kws
    )

    driver = _get_driver(identifier, session=session)
    team = driver.team
    idx = team.drivers.index(driver)

    if not style:
        # catches empty list, tuple, str
        raise ValueError("The provided style info is empty!")

    if isinstance(style, str):
        style = [style]

    plot_style = dict()

    if isinstance(style[0], str):
        # generate the plot style based on the provided keyword
        # arguments
        for opt in style:
            if opt in color_kwargs:
                value = get_team_color(team.normalized_value,
                                       colormap=colormap,
                                       session=session)
            elif opt in stylers:
                value = stylers[opt][idx]
            else:
                raise ValueError(f"'{opt}' is not a supported styling "
                                 f"option")
            plot_style[opt] = value

    else:
        try:
            custom_style = style[idx]
        except IndexError:
            raise ValueError(f"The provided custom style info does not "
                             f"contain enough variants! (Has: {len(style)}, "
                             f"Required: {idx})")

        if not isinstance(custom_style, dict):
            raise ValueError("The provided style info has an invalid format!")

        # copy the correct user provided style and replace any 'auto'
        # colors with the correct color value
        plot_style = custom_style.copy()
        for kwarg in color_kwargs:
            if plot_style.get(kwarg, None) == 'auto':
                color = get_team_color(team.normalized_value,
                                       colormap=colormap,
                                       session=session)
                plot_style[kwarg] = color

    return plot_style


def add_sorted_driver_legend(ax: matplotlib.axes.Axes, *, session: Session):
    """
    Adds a legend to the axis where drivers are ordered by team and within a
    team in the same order that is used for selecting plot styles.

    This function is a drop in replacement for calling Matplotlib's
    ``ax.legend()`` method. It can only be used when driver names or driver
    abbreviations are used as labels for the legend.

    There is no particular need to use this function except to make the
    legend more visually pleasing.

    .. seealso::
        :ref:`sphx_glr_examples_gallery_plot_driver_styling.py`

    Args:
        ax: An instance of a Matplotlib ``Axes`` object
        session: the session for which the data should be obtained
    """
    dtm = _get_driver_team_mapping(session)
    handles, labels = ax.get_legend_handles_labels()

    teams_list = list(dtm.teams_by_normalized.values())
    driver_list = list(dtm.drivers_by_normalized.values())

    # create an intermediary list where each element is a tuple that
    # contains (team_idx, driver_idx, handle, label). Then sort this list
    # based on the team_idx and driver_idx. As a result, drivers from the
    # same team will be next to each other and in the same order as their
    # styles are cycled.
    ref = list()
    for hdl, lbl in zip(handles, labels):
        driver = _get_driver(lbl, session=session)
        team = driver.team

        team_idx = teams_list.index(team)
        driver_idx = driver_list.index(driver)

        ref.append((team_idx, driver_idx, hdl, lbl))

    # sort based only on team_idx and driver_idx (i.e. first two entries)
    ref.sort(key=lambda e: e[:2])

    handles_new = list()
    labels_new = list()
    for elem in ref:
        handles_new.append(elem[2])
        labels_new.append(elem[3])

    ax.legend(handles_new, labels_new)
