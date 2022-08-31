import dash
from dash import Dash, dcc, Output, Input, html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np

# import data
df = pd.read_excel("chat_analyze.xlsx")
df = df.dropna()

app = dash.Dash(__name__)
mytitle = dcc.Markdown(children = '# app that analyzes..')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(id='dropdown', options= [{'label': 'All', 'value': 'All'}] + [
        {'label': i, 'value': i} for i in df.Team.unique()
    ], value = "All")

app.layout = dbc.Container([mytitle, mygraph, dropdown])

@app.callback(
    Output(mygraph, component_property="figure"),
    Input(dropdown, component_property="value")
)

def update_graph(user_input):
    if user_input == "All":
        fig = px.bar(df, x = df['Category'].unique(), y = df['Category'].value_counts())
    else:
        filtered_df = df[df.Team == user_input]
        fig = px.bar(filtered_df, x = filtered_df['Category'].unique(), y = filtered_df['Category'].value_counts())

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)