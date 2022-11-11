import pandas as pd
import numpy as np
import re
import itertools
from word2number import w2n
from sklearn.cluster import KMeans


class IndexReplication:
    def __init__(self):
        self.spy = pd.read_csv("data/spy.csv").drop(columns = "Unnamed: 0")
        self.spy["Symbol"] = "SPY"
        self.spy.dropna(inplace=True)

        self.data = pd.read_csv("data/data.csv").drop(columns = "Unnamed: 0")
        self.data.dropna(inplace=True)

        self.corr_df = pd.read_csv("data/corr_df.csv").drop(columns = "Unnamed: 0")

        self.log_df = pd.read_csv("data/log_df.csv").drop(columns = "Unnamed: 0")

    
    def extract_number(self, inp):
        res = re.findall(r'\d+', inp)
        if len(res) > 0:
            res = [int(res[0])]
        #if it comes here that means the input doesn't have a numeric form and probably word format
        if not res:
            for w in inp.split():
                if not res:
                    try:
                        res = [w2n.word_to_num(w)]
                    except:
                        res = []
        return res


    def extract_mathematical(self, inp):
        #dictionary of key words for inequalities
        d = {
            "=": ["only", "exactly"],
            ">=": ["at least", "minimum", "no less than", "no fewer than", "greater than or equal to"],
            "<=": ["at most", "maximum", "no more than", "not above", "does not exceed", "less than or equal to"],
            ">": ["more than", "exceeds", "over", "above", "greater than"],
            "<": ["under", "below", "fewer than", "beneath", "less than"]
        }
        res = []
        for key, value in d.items():
            for w in value:
                if w in inp.lower():
                    res.append(key)
        return res

#NEED TO ADD CATEGORICAL EXTRACTION CODE


    def extraction(self, inp):
        res = []
        mth = self.extract_mathematical(inp)
        num = self.extract_number(inp)
        cat = False
        if len(mth) > 0:
            res.append((mth[0], 'mth'))
        else:
            res.append(("None", "mth"))
        if len(num) > 0:
            res.append((num[0], 'num'))
        else:
            res.append(("None", "num"))
        if cat:
            res.append((cat, "cat"))
        else:
            res.append(("None", "cat"))
        return res



    def compound_timeseries(self, combination):
        #final compounded time series
        count = 0
        final_pct_change = 0
        for stock in combination:
            final_pct_change += self.data[self.data['Symbol'] == stock]['Percent_Change'].reset_index()['Percent_Change']
            count += 1
        final_pct_change /= count
        return final_pct_change



    def index_replicationV2(self, inp):
        #this method will include the new optimization code we came up with
        nlp = self.extraction(inp)
        num = None
        mth = None
        filt = None
        num_stocks = 5
        add = 0

        #adding all NLP extraction into variable
        for x, y in nlp:
            #assigning math constraint into mth as long as user has given one
            if y == 'mth' and x != "None":
                mth = x
            #assigning num constraint into num_stocks as long as user has given one
            elif y == 'num' and x != "None":
                num = True
                num_stocks = x
            #assigning cat constraint into filt as long as user have given certain sectors to invest into
            elif y == "cat" and x != "None":
                if x != "None":
                    filt = x
  
        #if user gave a mathematical constraint
        if mth:
            if mth == ">=" or mth == ">":
            #if the user wants more than the certain number, we give them two extra stocks
                add = 2
            else:
                #if the user wants less than the certain number, we give them one less stock
                add = -1
        #if no sector constraint given, we give a default sector which is Technology
        if not filt:
            filt = "Information Technology"

        #accounting for the mathematical constraint
        num_stocks += add
        
        return self.optimization(num_stocks, filt)
    

    def create_matrix(self, sector):
        corr_m = pd.DataFrame()
        companies = self.log_df[self.log_df['Sector'] == sector]['Symbol'].unique().tolist()
        for stock in companies:
            temp = pd.DataFrame({stock: self.log_df[self.log_df['Symbol'] == stock].copy()['Log Returns'] }).reset_index()[stock]
            corr_m = pd.concat([corr_m, temp], axis=1)
        matrix = corr_m.corr()
        return matrix
    
    
    def optimization(self, mth, sector = "Information Technology"):
        df = pd.DataFrame()
        #initializing the resulting list of companies
        res = []
        #creating the matrix based on sector
        matrix = self.create_matrix(sector)
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
        return res

        
    

