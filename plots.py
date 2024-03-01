import plotly.express as px

# Source: https://plotly.com/python/heatmaps/

def plot_by_country(df):

    # Set the the first column as the index it is unnamed
    df.set_index(df.columns[0], inplace=True)
    # remove the name of the index
    df.index.name = None

    # Exclude the Walk values
    df = df.drop('Walk', axis=0)

    # Round the values to 2 decimal places
    df = df.round(2)

    fig = px.imshow(df, text_auto=True, aspect='auto', title='Total Emissions (kgCO2e) by Country and Mode of Transport',
                    labels=dict(x="Country", y="Transport", color="Emissions (kgCO2e)"),
                    color_continuous_scale='bupu')

    # Edit the font size and color of the values
    fig.update_traces(textfont_size=16)

    return fig

