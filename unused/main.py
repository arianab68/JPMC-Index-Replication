import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
from CLASS import IndexReplication

IndexReplication = IndexReplication()
df = IndexReplication.spy
#Dashboard Code
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])



# fig = px.line(spy, x="Date", y= "Close", title=  "S&P 500")

app.layout = html.Div(children = [

    html.H1(children='Index Replication Optimization with Natural Language Constraints', style = {'textAlign': 'center'}),

    html.Div(dcc.Input(id='user-input', type='text')),

    html.Button('Submit', id='submit-val', n_clicks=0),

    # dcc.Graph(
    #     id='sp500',
    #     figure = fig
    # ),

    html.Div(id='container-button-basic',
             children= dash_table.DataTable(
              style_data={
            'whiteSpace': 'normal',
            'height': '10px',
            'lineHeight': '15px',
            'width': '50px'
              }, 
            data = df.to_dict('records'),
            fill_width=False,
            page_size=10))
])

# @app.callback(
#     Output('container-button-basic', 'children'),
#     Input('submit-val', 'n_clicks'),
#     State('user-input', 'value')
# )
# def update_output(n_clicks, value):
#   if value:
#     res = IndexReplication.index_replicationV2(value)
#     return str(res)
#   else:
#     return "No User Input"


if __name__ == "__main__":
    app.run_server(debug=True, port=3000)
    #print(IndexReplication.data.head())