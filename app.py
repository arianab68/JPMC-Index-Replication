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
                                    id="first-card",
                                    children=[
                                        drc.NamedDropdown(
                                            name="Select Sector",
                                            id="dropdown-select-sector",
                                            options=[
                                                {
                                                    "label": "Tech", 
                                                    "value": "Information Technology"},
                                                {
                                                    "label": "Finance",
                                                    "value": "Financials",
                                                },
                                                {
                                                    "label": "Energy",
                                                    "value": "Energy",
                                                },
                                            ],
                                            clearable=False,
                                            searchable=False,
                                            value = "Energy",
                                        ),
                                        drc.NamedSlider(
                                            name="Number of Stocks",
                                            id="slider-stock-size",
                                            min=2,
                                            max=10,
                                            step=2,
                                            marks={
                                                str(i): str(i)
                                                for i in [2, 4, 6, 8, 10]
                                            },
                                            value=10,
                                        )
                                    ],
                                ),
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
    Output("slider-stock-size", "value"),
    [Input("button-generate-solution", "n_clicks")],
    [State("user-input", "value")],
)
def update_stock_slider(n_clicks, value):
    num = IndexReplication.extract_number(str(value))
    #if input is empty or if no number constraint was given we give default value to the slider
    if len(num) == 0:
        return 5
    if num[0] > 10:
        return 10
    return num[0]


@app.callback(
    Output("dropdown-select-sector", "value"),
    [Input("button-generate-solution", "n_clicks")],
    [State("user-input", "value")],
)
def update_sector(n_clicks, value):
    pass



@app.callback(
    Output("div-graphs", "children"),
    [
        Input("dropdown-select-sector", "value"),
        Input("slider-stock-size", "value")
    ],
)
def update_graph(sector, num_stocks):
    print(f'num: {num_stocks}')
    print(f'sector: {sector}')
    best_portfolio = IndexReplication.best_portfolio(sector_constraint = sector, mth_constraint = num_stocks)
    top_10 = ['AAPL', 'MSFT', 'AMZN', 'TSLA', 'GOOGL', 'V', 'XOM', 'JNJ', 'JPM', 'NVDIA']
    d = pd.DataFrame({'Company': top_10,
                      'Returns (%)': [round(data[data['Symbol'] == stock]['Percent_Change'].sum() * 100, 2) for stock in top_10]})

    portfolio_holdings = pd.DataFrame({'Company': best_portfolio,
                      'Returns (%)': [round(data[data['Symbol'] == stock]['Percent_Change'].sum() * 100, 2) for stock in best_portfolio]})

    prediction_figure = spy_fig
    
    sp500_top_holdings_table = dash_table.DataTable(style_data={
                                    'overflowY': 'auto',
                                    'width': '100px'}, 
                                    data = d.to_dict('records'),
                                    fill_width=True,
                                    fixed_rows={'headers': True})

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
                children=dcc.Graph(id="graph-sklearn-svm", figure=prediction_figure),
                style={"display": "none"},
            ),
                dcc.Loading(
                className="graph-wrapper",
                children=dcc.Graph(id="SPY", figure=spy_fig),
                style={"display": "none"},
                ),
            ],
        ),
        html.Div(
            id="graphs-container",
            children=[
                html.Label("Top 10 Holdings", style={'text-align': 'center'}),
                sp500_top_holdings_table,
                html.Br(),
                html.Br(),
                html.Br(),
                html.Label("Portfolio Holdings", style={'text-align': 'center'}),
                portfolio_holdings_table,
            ],
        ),
    ]


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)
