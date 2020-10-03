import plotly.graph_objects as go
import plotly.express as px
import requests, json
import pandas as pd
import os
from urllib.request import urlopen, urlretrieve
import numpy as np

def chart_1_data():
    covid_requests = requests.get("https://finnhub.io/api/v1/covid19/us?token=btcrspf48v6s23u166pg")
    json_data = covid_requests.json()
    df = pd.DataFrame(json_data)
    df = df.drop(df.index[47])
    df = df[:52]

    state_codes = ["NY", "NJ", "CA", "MI", "FL", "MA", "WA", "LA", "IL", "PA", "GA", 
          "TX", "CO", "CT", "OH", "IN", "TN", "MD", "NC", "WI", "AZ", 
          "VA", "MO", "NV", "AL", "MS", "SC", "UT", "MN", "OR", "OK", 
          "AR", "IA", "DC", "KY", "ID", "RI", "KS", "NH", "ME", "VT", 
          "NM", "DE", "PR", "HI", "MT", "NE", "WV", "ND", "AK", "WY", "SD"]
        
    df['state code'] = state_codes

    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv'
    df2 = pd.read_csv(url, error_bad_lines=False, dtype={"fips":str})
    df2 = df2[df2.county != 'Unknown'] # error for missouri
    df2['fips'].replace('', np.nan, inplace=True)
    df2.dropna(subset=['fips'], inplace=True)

    return df, df2

def chart_2_data():
    url2 = requests.get('https://api.covidtracking.com/v1/states/current.json')
    json_data_2 = url2.json()
    df3 = pd.DataFrame(json_data_2)

    val = df3['date'][2]
    df3 = df3[df3.date == val]

    return df3

def chart_3_data():
    url3 = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
    df4 = pd.read_csv(url3, error_bad_lines=False)

    return df4

def update_chart_layout(figure, title):
    return figure.update_layout(title={
        'text': title,
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

