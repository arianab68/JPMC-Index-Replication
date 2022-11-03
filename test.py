from CLASS import IndexReplication



if __name__ == "__main__":
    x = IndexReplication()
    print(x.compound_timeseries(['AAPL', 'GOOG']))
    print(x.spy['Percent_Change'].reset_index()['Percent_Change'])
