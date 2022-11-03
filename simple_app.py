import plotly.express as px
import dash
from dash import dcc, html, Dash, dash_table
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output, State
import utils.dash_reusable_components as drc
from CLASS import IndexReplication

IndexReplication = IndexReplication()
data = IndexReplication.data
spy = IndexReplication.spy
spy_fig = px.line(spy, x="Date", y= "Close", title=  "S&P 500")


app = Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
app.title = "JPMC Index Replication"
server = app.server


app.layout = html.Div(
    children=[
        # .container class is fixed, .container.scalable is scalable
        html.Div(
            className="banner",
            children=[
                # Change App Name here
                html.Div(
                    className="container scalable",
                    children=[
                        # Change App Name here
                        html.H2(
                            id="banner-title",
                            children=[
                                html.A(
                                    "JPMC Index Replication",
                                    href="https://github.com/plotly/dash-svm",
                                    style={
                                        "text-decoration": "none",
                                        "color": "inherit",
                                    },
                                )
                            ],
                        ),
                        html.A(
                            id="banner-logo",
                            children=[
                                html.Img(src=app.get_asset_url("dash-logo-new.png"))
                            ],
                            href="https://plot.ly/products/dash/",
                        ),
                    ],
                )
            ],
        ),
        html.Div(
            id="body",
            className="container scalable",
            children=[
                html.Div(
                    id="app-container",
                    # className="row",
                    children=[
                        html.Div(
                            # className="three columns",
                            id="left-column",
                            children=[
                                drc.Card(
                                    id="button-card",
                                    children=[
                                        html.Label("User Input:"),
                                        dcc.Input(
                                                id='user-input', 
                                                type='text', 
                                                placeholder="I want..."
                                                ),
                                        html.Br(),
                                        html.Button(
                                            "Generate Solution",
                                            id="button-generate-solution",
                                        ),
                                    ],
                                ),
                                drc.Card(
                                    id="first-card",
                                    children=[]
                                )
                            ],
                        ),
                        html.Div(
                            id="div-graphs",
                            # children=dcc.Graph(
                            #     id="graph-sklearn-svm",
                            #     figure=spy_fig,
                            # ),
                        ),
                    ],
                )
            ],
        ),
    ]
)




@app.callback(
    Output("div-graphs", "children"),
    [Input("button-generate-solution", "n_clicks")],
    [State("user-input", "value")],
)
def update_graph(n_clicks, value):
    
    top_10 = ['AAPL', 'MSFT', 'AMZN', 'TSLA', 'GOOGL', 'V', 'XOM', 'JNJ', 'JPM', 'NVDIA']
    d = pd.DataFrame({'Company': top_10,
                      'Returns (%)': [round(data[data['Symbol'] == stock]['Percent_Change'].sum() * 100, 2) for stock in top_10]})
    sp500_top_holdings_table = dash_table.DataTable(style_data={
                                    'overflowY': 'auto',
                                    'width': '100px'}, 
                                    data = d.to_dict('records'),
                                    fill_width=True,
                                    fixed_rows={'headers': True})
    if not value:
        return [
                html.Div(
                    id="svm-graph-container",
                    children=[
                        dcc.Loading(
                        className="graph-wrapper",
                        children=dcc.Graph(id="SPY", figure=spy_fig, style = {'width': '700px', 'height': '380px'}),
                        style={"display": "none"},
                        ),
                    ],
                ),
                html.Div(
                    id="graphs-container",
                    children=[
                        html.Label("Top 10 S&P500 Holdings", style={'text-align': 'center'}),
                        sp500_top_holdings_table,
                    ],
                ),
            ]

    best_portfolio = IndexReplication.index_replicationV2(value)

    portfolio_holdings = pd.DataFrame({'Company': best_portfolio,
                      'Returns (%)': [round(data[data['Symbol'] == stock]['Percent_Change'].sum() * 100, 2) for stock in best_portfolio]})

    port_time_series = IndexReplication.compound_timeseries(best_portfolio)
    spy_time_series = spy['Percent_Change'].reset_index()['Percent_Change']

    portfolio_figure = px.scatter(x = port_time_series, y = spy_time_series)
    
    portfolio_holdings_table = dash_table.DataTable(style_data={
                                    'overflowY': 'auto',
                                    'width': '100px'}, 
                                    data = portfolio_holdings.to_dict('records'),
                                    fill_width=True,
                                    fixed_rows={'headers': True})

    return [
        html.Div(
            id="svm-graph-container",
            children=[
                dcc.Loading(
                className="graph-wrapper",
                children=dcc.Graph(id="SPY", figure=spy_fig, style = {'width': '700px', 'height': '380px'}),
                style={"display": "none"},
                ),
                html.Br(),
                html.Br(),
                dcc.Loading(
                className="graph-wrapper",
                children=dcc.Graph(id="graph-sklearn-svm", figure=portfolio_figure, style = {'width': '700px', 'height': '380px'}),
                style={"display": "none"},
            )
            ],
        ),
        html.Div(
            id="graphs-container",
            children=[
                html.Label("Top 10 S&P 500 Holdings", style={'text-align': 'center'}),
                sp500_top_holdings_table,
                html.Br(),
                html.Br(),
                html.Br(),
                html.Label("Portfolio Holdings", style={'text-align': 'center'}),
                portfolio_holdings_table,
            ],
        ),
    ]
    

@app.callback(
    Output("first-card", "children"),
    [Input("button-generate-solution", "n_clicks")],
    [State("user-input", "value")],
)
def update_allocation(n_clicks, value):
    if not value:
        return
    
    best_portfolio = IndexReplication.index_replicationV2(value)
    port_time_series = IndexReplication.compound_timeseries(best_portfolio)
    spy_time_series = spy['Percent_Change'].reset_index()['Percent_Change']
    corr = port_time_series.corr(spy_time_series)
    return [
            html.Label("Proposed Allocation", style={'text-align': 'center'}),
            html.Label(str(best_portfolio), style={'text-align': 'center'}),
            html.Label("Correlation to S&P500", style={'text-align': 'center'}),
            html.Label(str(corr), style={'text-align': 'center'})
            ]
    

# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)
