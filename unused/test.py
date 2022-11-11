import datetime
import numpy as np
import pandas as pd
import pandas_datareader.data as pdr
from CLASS import IndexReplication

# fetch multiple asset data
# def getMultiAssetData(ticketList, date_from, date_to):
#     def getData(ticker):
#         data = pdr.DataReader(ticker, 'yahoo', date_from, date_to)
#         return data
#     datas = map(getData, tickerList)
#     return pd.concat(datas, keys=tickerList, names=['Ticker', 'Date'])

# date_from = datetime.date(2020, 1, 1)
# date_to = datetime.date(2020, 8, 31)
# tickerList = ['AAPL', 'AMZN', 'CCEP', 'FB', 'JNJ', 'JWN', 'NVS', 'PG']
# multiData = getMultiAssetData(tickerList, date_from, date_to)
# df = multiData.copy()
# adjClosePrice = df[['Adj Close']]
# adjClosePrice = adjClosePrice.reset_index()
# adjClosePriceTable = adjClosePrice.pivot(index='Date', columns='Ticker', values='Adj Close')


if __name__ == "__main__":
    IndexReplication = IndexReplication()
    data = IndexReplication.data
    spy = IndexReplication.spy
    # print(x.compound_timeseries(['AAPL', 'GOOG']))
    # print(x.spy['Percent_Change'].reset_index()['Percent_Change'])
    # daily_pct_change = x.compound_timeseries(['AAPL', 'GOOG'])
    # cumprod_daily_pct_change = (1 + daily_pct_change).cumprod()
    # print(cumprod_daily_pct_change)
    # daily_pct_change = x.spy['Percent_Change'].reset_index()['Percent_Change']
    # cumprod_daily_pct_change = (1 + daily_pct_change).cumprod()
    # print(cumprod_daily_pct_change)
    # print(x.spy.tail(1))
    # print(x.spy.head(1))
    # daily_pct_change = spy['Percent_Change'].reset_index()['Percent_Change'] + 1
    # beggining = pd.Series([100])
    # daily_pct_change = beggining.append(daily_pct_change).reset_index()[0]
    # cumprod_daily_pct_change = (daily_pct_change).cumprod()
    # print(cumprod_daily_pct_change)
    # print(data[data['Symbol'] == "TSLA"].head(1))
    # print(data[data['Symbol'] == "TSLA"].tail(1))
    # print(cumprod_daily_pct_change)
    # print(daily_pct_change)
    # print(spy['Close']/spy['Close'].iloc[0])
    # print(cumprod_daily_pct_change)
    # print(type(daily_pct_change))
    # best_portfolio = IndexReplication.index_replicationV2('four stocks')
    port_time_series = IndexReplication.compound_timeseries(['TSLA']) 
    # print(data[data['Symbol'] == 'TSLA'].head(1)['Close'])
    print(port_time_series.sum())
    cumprod_daily_pct_change = ((1 + port_time_series).cumprod() - 1) * 100
    print(cumprod_daily_pct_change)

    #352 
    #29
    print(((352 - 29) / 29) * 100)


