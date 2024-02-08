import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

scot_postcodes = ['AB', 'DD', 'DG', 'EH', 'FK', 'G', 'HS', 'IV', 'KA', 'KW', 'KY', 'ML', 'PA', 'PH', 'TD', 'ZE']
wales_postcodes = ['CF', 'LL', 'NP', 'SA', 'SY']
north_ireland_postcodes = ['BT']

# This function calculates total distance travelled by a given method of transport

def total_distance(data: dict):
    scot_dist = 0
    england_dist = 0
    wales_dist = 0
    north_ireland_dist = 0

    for key, value in data.items():
        if key[:2] in scot_postcodes or key[:1] == 'G':
            scot_dist += value[2]
        elif key[:2] in wales_postcodes:
            wales_dist += value[2]
        elif key[:2] in north_ireland_postcodes:
            north_ireland_dist += value[2]
        else:
            england_dist += value[2]

    scot_dist = round(scot_dist, 2)
    england_dist = round(england_dist, 2)
    wales_dist = round(wales_dist, 2)
    north_ireland_dist = round(north_ireland_dist, 2)

    return scot_dist, england_dist, wales_dist, north_ireland_dist

# Create a heatmap of the UK showing the total distance travelled by bus and plane by country
def create_heatmap(bus: tuple, plane: tuple):
    # Create a dataframe with the total distance travelled by bus and plane by country
    df = pd.DataFrame({'Scotland': [bus[0], plane[0]], 'England': [bus[1], plane[1]], 'Wales': [bus[2], plane[2]], 'North Ireland': [bus[3], plane[3]]}, index=['Bus', 'Plane'])
    # Create a heatmap
    sns.heatmap(df, annot=True, fmt=".2f", cmap='YlGnBu', cbar_kws={'label': 'Distance (km)'})
    plt.title('Total distance travelled by bus and plane by country')
    plt.show()

