import pandas as pd
from datetime import datetime
import numpy as np

if __name__ == "__main__":
    df = pd.read_csv('sphist.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    bool_date = df['Date']>datetime(year=2015, month=4, day=1)
    df.sort_values(by='Date', inplace=True)
    #ME:
    #part3
    df = df.reset_index()
    d5=[]
    d30=[]
    d365=[]
    for i, row in df.iterrows():
        if i >= 5:
            d5.append(df.iloc[(i-5):i,5].mean())
        else:
            d5.append(np.NaN)
        if i >= 30:
            d30.append(df.iloc[(i-30):i,5].mean())
        else:
            d30.append(np.NaN)
        if i >= 365:
            d365.append(df.iloc[(i-365):i,5].mean())
        else:
            d365.append(np.NaN)
    df['5_days']=d5
    df['30_days']=d30
    df['365_days']=d365
    print(df.iloc[250:252,:])
    #part4
    df = df[df['Date']>datetime(year=1951,month=1,day=2)]
    df = df.dropna(axis=0)
    train = df[df['Date'] < datetime( year=2013, month=1, day=1)]
    test = df[df['Date'] >= datetime( year=2013, month=1, day=1)]
    #part5 MAE:
    from sklearn.linear_model import LinearRegression
    lr = LinearRegression()
    features = ['5_days', '30_days', '365_days']
    target = ['Close']
    lr.fit(train[features],train[target])
    close_test_pred = lr.predict(test[features])
    close_test_pred = [item for sublist in close_test_pred for item in sublist]
    close_test_actual = test.Close.tolist()
    absolute_diff = np.absolute(pd.Series(close_test_pred)-pd.Series(close_test_actual))
    print(absolute_diff[:5])
