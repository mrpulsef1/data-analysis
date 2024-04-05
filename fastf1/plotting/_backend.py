import json
from typing import (
    Dict,
    List
)

import fastf1._api
from fastf1 import Cache
from fastf1.plotting._base import (
    _Driver,
    _normalize_string,
    _Team
)
from fastf1.plotting._constants import Constants


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
            for ref_team_name in Constants[year].Teams.keys():
                # TODO: handle unknown teams
                if ref_team_name in normalized_full_team_name:
                    team.normalized_value = ref_team_name
                    break
            else:
                raise ValueError  # TODO: log

            teams[team_name] = team

    return list(teams.values())
