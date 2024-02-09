import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

scot_postcodes = ['AB', 'DD', 'DG', 'EH', 'FK', 'G', 'HS', 'IV', 'KA', 'KW', 'KY', 'ML', 'PA', 'PH', 'TD', 'ZE']
wales_postcodes = ['CF', 'LL', 'NP', 'SA', 'SY']
north_ireland_postcodes = ['BT']

# This function calculates total distance travelled by a given method of transport

def total_distance(data: dict):
    pass
# Create a heatmap of the UK showing the total distance travelled by bus and plane by country
def create_heatmap(bus: tuple, car: tuple, rail: tuple, plane: tuple):
    # Create a dataframe with the total distance travelled by each method of transport
    data = {'Scotland': [bus[0], car[0], rail[0], plane[0]], 'England': [bus[1], car[1], rail[1], plane[1]], 'Wales': [bus[2], car[2], rail[2], plane[2]], 'North Ireland': [bus[3], car[3], rail[3], plane[3] ]}
    df = pd.DataFrame(data, index=['Bus', 'Car', 'Rail', 'Plane'])
    # Create the heatmap
    sns.heatmap(df, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title('Total distance travelled by method of transport and country')
    plt.show()


