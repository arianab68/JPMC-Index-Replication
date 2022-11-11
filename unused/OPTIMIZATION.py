import pandas as pd
import numpy as np
import itertools
from sklearn.cluster import KMeans

spy = pd.read_csv("../data/spy.csv").drop(columns = "Unnamed: 0")
spy["Symbol"] = "SPY"
spy.dropna(inplace=True)

data = pd.read_csv("../data/data.csv").drop(columns = "Unnamed: 0")
data.dropna(inplace=True)

log_df = pd.read_csv("../data/log_df.csv").drop(columns = "Unnamed: 0")



def compound_timeseries(combination):
    #final compounded time series
    count = 0
    final_pct_change = 0
    for stock in combination:
        final_pct_change += data[data['Symbol'] == stock]['Percent_Change'].reset_index()['Percent_Change']
        count += 1
    final_pct_change /= count
    return final_pct_change


def create_matrix(sector):
    corr_m = pd.DataFrame()
    companies = log_df[log_df['Sector']== sector]['Symbol'].unique().tolist()
    for stock in companies:
        temp = pd.DataFrame({stock:log_df[log_df['Symbol'] == stock].copy()['Log Returns'] }).reset_index()[stock]
        corr_m = pd.concat([corr_m, temp], axis=1)
    matrix = corr_m.corr()
    return matrix


def optimization(mth, sector = "Information Technology"):
    df = pd.DataFrame()
    #initializing the resulting list of companies
    res = []
    #creating the matrix based on sector
    matrix = create_matrix(sector)
    #this gives us the list of companies within the matrix
    companies = matrix.index.tolist()
    df.index = companies
    #pulling all values from matrix correlation
    X = matrix.values
    #fitting Kmeans model and using math constraint as the number of clusters
    kmeans = KMeans(n_clusters = mth).fit(X)
    df['cluster'] = kmeans.labels_
    for i in range(mth):
        res.append(df[df.cluster == i].head(1).index[0])
    return res, df















#NOT USED
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
