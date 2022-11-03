import pandas as pd
import numpy as np
import itertools

spy = pd.read_csv("data/spy.csv").drop(columns = "Unnamed: 0")
spy["Symbol"] = "SPY"
spy.dropna(inplace=True)

data = pd.read_csv("data/data.csv").drop(columns = "Unnamed: 0")
data.dropna(inplace=True)




def compound_timeseries(combination):
    #final compounded time series
    count = 0
    final_pct_change = 0
    for stock in combination:
        final_pct_change += data[data['Symbol'] == stock]['Percent_Change'].reset_index()['Percent_Change']
        count += 1
    final_pct_change /= count
    return final_pct_change



def best_portfolio(sector_constraint, mth_constraint):
    if not sector_constraint:
        sector_constraint = "Energy"
    if mth_constraint > 10:
        mth_constraint = 10
    time_series_spy = spy['Percent_Change']
    symbols = data[data['Sector'] == sector_constraint]['Symbol'].unique().tolist()
    if mth_constraint >= len(symbols):
        mth_constraint = len(symbols) - 2
    max_corr = -float('inf')
    res = ''
    count = 0
    for combo in itertools.combinations(symbols, mth_constraint):
        if count == 50:
            break
        count += 1
        corr = time_series_spy.corr(compound_timeseries(combo))
        if corr > max_corr:
            max_corr = max(corr, max_corr)
            res = combo
    return list(res)
