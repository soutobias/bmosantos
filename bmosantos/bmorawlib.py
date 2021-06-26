import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

def get_data(token):

    start_time = (datetime.utcnow() - timedelta(days=10)).strftime('%Y-%m-%d')
    time_now = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')
    url=f'http://143.198.233.67/api/v1/bmo_raws?start_date={start_time}&end_date={time_now}&token={token}'

    response = requests.get(url).json()
    df = pd.DataFrame(response)
    for i in df.columns:
        try:
            df[i] = pd.to_numeric(df[i])
        except:
            pass
    df['date_time'] = pd.to_datetime(df['date_time'], format='%Y-%m-%dT%H:%M:%S.000Z')
    df.sort_values('date_time', inplace=True)


    df = df[['id', 'buoy_id', 'date_time', 'lat', 'lon', 'battery', 'wspd1',
        'gust1', 'wdir1', 'wspd2', 'gust2', 'wdir2', 'atmp', 'rh', 'dewpt',
        'pres', 'sst', 'compass', 'arad', 'cspd1', 'cdir1', 'cspd2', 'cdir2',
        'cspd3', 'cdir3', 'swvht1', 'tp1', 'mxwvht1', 'wvdir1', 'wvspread1',
        'swvht2', 'tp2', 'wvdir2']]

    return df


def plot_graphs(df, variables):

    fig = go.Figure()
    for variable in variables:
        fig.add_trace(go.Scatter(x=df['date_time'], y=df[variable],
                            mode='lines',
                            name=variable))
    st.plotly_chart(fig)

