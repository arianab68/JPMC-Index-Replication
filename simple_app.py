import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html, Dash, dash_table
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import utils.dash_reusable_components as drc
from CLASS import IndexReplication


#instantiating class and loading data
IndexReplication = IndexReplication()
data = IndexReplication.data
spy = IndexReplication.spy

#getting the overall portfolio performance of sp500 AKA the cumulative return over time using percent change
daily_pct_change_spy = spy['Percent_Change'].reset_index()['Percent_Change'] 
cumprod_daily_pct_change_spy = ((1 + daily_pct_change_spy).cumprod() - 1) * 100

fig = go.Figure()
fig.add_trace(go.Scatter(x = spy.Date, y=cumprod_daily_pct_change_spy, name = 'S&P500', mode ='lines'))
fig.update_layout(title = "Cumulative Returns", title_x = 0.5, xaxis_title = 'Date', yaxis_title = 'Cumulative Return (%)')
    

app = Dash( __name__)
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
                                # html.Img(src=app.get_asset_url("unnamed.png"))
                            ],
                        ),
                    ],
                    style = {"text-align": "center"}
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
                                                placeholder="I want...",
                                                style={'color': 'white'}
                                                ),
                                        html.Br(),
                                        html.Button(
                                            "Generate Solution",
                                            id="button-generate-solution",
                                            style= {'color': 'white'}
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
                            children=dcc.Graph(
                                id="graph-sklearn-svm",
                                figure=fig,
                            ),
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

    #if no input is given we give the default graph of the sp500
    if not value:
        return [
                # html.Div(
                #     id="svm-graph-container",
                #     children=[
                #         dcc.Loading(
                #         className="graph-wrapper",
                #         children=dcc.Graph(id="SPY", figure = fig),
                #         style={"display": "none"},
                #         ),
                #     ],
                # ),
            ]
    
    #getting the best portfolio
    best_portfolio = IndexReplication.index_replicationV2(value)
    port_time_series = IndexReplication.compound_timeseries(best_portfolio) 
    cumprod_daily_pct_change = ((1 + port_time_series).cumprod() - 1) * 100

    #getting portfolio correlation to sp500
    spy_time_series = spy['Percent_Change'].reset_index()['Percent_Change']
    corr = port_time_series.corr(spy_time_series)

    #getting total returns of portfolio and sp500 over the timeframe
    portfolio_returns_total = str(round(cumprod_daily_pct_change[len(cumprod_daily_pct_change) - 1], 2)) + "%"
    sp_returns_total = str(round(cumprod_daily_pct_change_spy[len(cumprod_daily_pct_change_spy) -  1], 2)) + "%"


    #updating main graph to have portfolio chart
    fig.add_trace(go.Scatter(x = data.Date, y=cumprod_daily_pct_change, name = str(best_portfolio), mode ='lines'))
    
    

    return [
                html.Div(
                    id="svm-graph-container",
                    children=[
                        dcc.Loading(
                        className="graph-wrapper",
                        children=dcc.Graph(id="SPY", figure = fig),
                        style={"display": "none"},
                        ),
                        html.Label(f"Correlation to S&P500: {corr}", style={'text-align': 'center'}),
                        html.Label(f"Total Portfolio Return: {portfolio_returns_total}", style={'text-align': 'center'}),
                        html.Label(f"Total S&P500 Return: {sp_returns_total}", style={'text-align': 'center'})
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
        return []
    
    best_portfolio = IndexReplication.index_replicationV2(value)
    portfolio_holdings = pd.DataFrame({'Company': best_portfolio,
                                        'Weight(%)': [round(100/len(best_portfolio), 2) for stock in best_portfolio]})
    portfolio_holdings_table = dash_table.DataTable(style_data={
                                    'overflowY': 'auto',
                                    'width': '100px'}, 
                                    data = portfolio_holdings.to_dict('records'),
                                    fill_width=True,
                                    fixed_rows={'headers': True})
    return [
                html.Label("Proposed Allocation", style={'text-align': 'center'}),
                html.Br(),
                portfolio_holdings_table,
                html.Br()
            ]
    

# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)










#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#EXTRAS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------

    # return [
    #     html.Div(
    #         id="svm-graph-container",
    #         children=[
    #             dcc.Loading(
    #             className="graph-wrapper",
    #             children=dcc.Graph(id="SPY", figure=spy_fig, style = {'width': '700px', 'height': '380px'}),
    #             style={"display": "none"},
    #             ),
    #             html.Br(),
    #             html.Br(),
    #             dcc.Loading(
    #             className="graph-wrapper",
    #             children=dcc.Graph(id="graph-sklearn-svm", figure=portfolio_figure, style = {'width': '700px', 'height': '380px'}),
    #             style={"display": "none"},
    #         )
    #         ],
    #     ),
    #     html.Div(
    #         id="graphs-container",
    #         children=[
    #             html.Label("Top 10 S&P 500 Holdings", style={'text-align': 'center'}),
    #             sp500_top_holdings_table,
    #             html.Br(),
    #             html.Br(),
    #             html.Br(),
    #             html.Label("Portfolio Holdings", style={'text-align': 'center'}),
    #             portfolio_holdings_table,
    #         ],
    #     ),
    # ]