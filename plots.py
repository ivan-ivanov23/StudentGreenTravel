import plotly.express as px
import pandas as pd

# Source: https://plotly.com/python/heatmaps/

def plot_by_country(df):
    # Round the values to 2 decimal places
    df = df.round(0)

    # take names from first row
    names = df.columns[1:]
    # Values are the second row
    values = df.iloc[0, 1:]

    fig = px.pie(df, values=values, names=names, title='Total Emissions by Country')

    # Edit the font size and color of the values
    fig.update_traces(textfont_size=16)

    fig.show()

df = pd.read_csv('total_emissions.csv')

plot_by_country(df)