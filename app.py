import dash
from dash import Dash, dcc, Output, Input, html
from datetime import datetime as dt
from datetime import date
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np  

# import data
df = pd.read_excel("chat_analyze.xlsx")
df = df.dropna()
df['Date'] = pd.to_datetime(df['Date'])

app = dash.Dash(__name__)
mytitle = dcc.Markdown(children = '# Chat Analysis')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(id='dropdown', options= [{'label': 'All', 'value': 'All'}] + [
        {'label': i, 'value': i} for i in df.Team.unique()
    ], value = "All")
date_picker = dcc.DatePickerRange(id='my_date_picker', start_date=df['Date'].min(), end_date=df['Date'].max() ,start_date_placeholder_text="Start Period", end_date_placeholder_text="End Perdiod", calendar_orientation='horizontal', clearable=False, min_date_allowed=dt(2022, 1, 1), initial_visible_month=df['Date'].min(), minimum_nights=0, persistence=True, persisted_props=['start_date', 'end_date'], persistence_type='local', updatemode='bothdates')
app.layout = dbc.Container([mytitle, date_picker, mygraph, dropdown])


@app.callback(
    Output(mygraph, component_property="figure"),
    Input(dropdown, component_property="value"),
    Input(date_picker, component_property="start_date"),
    Input(date_picker, component_property="end_date")
)

def update_graph(user_input, start_date, end_date):
    dff = df[df['Date'].between(start_date, end_date)]
    if user_input == "All":
        fig = px.bar(dff, x = dff['Category'].unique(), y = dff['Category'].value_counts())
    else:
        filtered_df = dff[dff.Team == user_input]
        fig = px.bar(filtered_df, x = filtered_df['Category'].unique(), y = filtered_df['Category'].value_counts())

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)