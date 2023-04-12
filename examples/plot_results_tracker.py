"""Plot GP results in a heatmap
======================================

Plot the points for each driven in each race of a given season in a heatmap, as
https://public.tableau.com/app/profile/mateusz.karmalski/viz/F1ResultsTracker2022
"""

import time

import pandas as pd
import plotly.express as px
import plotly.io as pio

from fastf1.ergast import Ergast


##############################################################################
# First, we load the results for season 2022
ergast = Ergast()
races = ergast.get_race_schedule(2022)  # Races in year 2022
results = []
for rnd, race in races['raceName'].items():
    temp = ergast.get_race_results(season=2022, round=rnd)  # Race results
    temp = temp.content[0]                                  # Points scored
    sprint = ergast.get_sprint_results(season=2022, round=rnd)
    if sprint.content and sprint.description['round'][0] == rnd:  # If sprint
        temp = pd.merge(temp, sprint.content[0], on='driverCode', how='left')
        temp['points'] = temp['points_x'] + temp['points_y']
        temp.drop(columns=['points_x', 'points_y'], inplace=True)
    temp['round'] = rnd + 1                                 # Add race name
    temp['race'] = race.removesuffix(' Grand Prix')
    temp = temp[['round', 'race', 'driverCode', 'points']]  # Only useful cols.
    results.append(temp)
results = pd.concat(results)
races = results['race'].drop_duplicates()

##############################################################################
# Then we ``reshape'' the results to a wide table, where each row represents a
# driver and each column refers to a race, and the cell value is the points
results = results.pivot(index='driverCode', columns='round', values='points')
# Here we have a 22-by-22 matrix (22 races and 22 drivers, incl. DEV and HUL)

# Order the drivers by their total points
results['total_points'] = results.sum(axis=1)
results = results.sort_values(by='total_points', ascending=False)
results.drop(columns='total_points', inplace=True)

# Use race name, instead of round no., as column names
results.columns = races


##############################################################################
# The final step is to plot a heatmap using plotly
fig = px.imshow(
    results,
    text_auto=True,
    aspect='auto',  # Automatically adjust the aspect ratio
    color_continuous_scale=[[0,    'rgb(198, 219, 239)'],  # Blue scale
                            [0.25, 'rgb(107, 174, 214)'],
                            [0.5,  'rgb(33,  113, 181)'],
                            [0.75, 'rgb(8,   81,  156)'],
                            [1,    'rgb(8,   48,  107)']],
    labels={'x': 'Race',
            'y': 'Driver',
            'color': 'Points'}   # Change hover texts
)
fig.update_xaxes(title_text='')  # Remove axis titles
fig.update_yaxes(title_text='')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey',
                 showline=True, linewidth=1, linecolor='LightGrey',
                 tickson='boundaries')
fig.update_xaxes(showgrid=False, showline=False)  # Show horizontal grid only
fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')   # White background
fig.update_layout(coloraxis_showscale=False)      # Remove legend
fig.update_layout(xaxis=dict(side='top'))         # x-axis on top
fig.show()
with open('examples/results_tracker.html', 'w') as f:
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
f.close()
