import pandas as pd
import numpy as np
import requests
from bmosantos.distance import haversine
import folium
import plotly.express as px
from streamlit_folium import folium_static
import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go


def get_data(token):

    start_time = (datetime.utcnow() - timedelta(days=10)).strftime('%Y-%m-%d')
    time_now = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')
    url=f'http://143.198.233.67/api/v1/data_buoys?buoy=2&start_date={start_time}&end_date={time_now}&token={token}'

    response = requests.get(url).json()
    df = pd.DataFrame(response)
    for i in df.columns:
        try:
            df[i] = pd.to_numeric(df[i])
        except:
            pass
    df['date_time'] = pd.to_datetime(df['date_time'], format='%Y-%m-%dT%H:%M:%S.000Z')
    df.sort_values('date_time', inplace=True)

    df = df[['date_time', 'lat', 'lon', 'battery', 'compass',
           'rh', 'flag_rh', 'pres', 'flag_pres', 'atmp',
           'flag_atmp', 'dewpt', 'flag_dewpt', 'wspd', 'flag_wspd', 'wdir',
           'flag_wdir', 'gust', 'flag_gust', 'arad', 'flag_arad', 'sst',
           'flag_sst', 'cspd1', 'flag_cspd1', 'cdir1', 'flag_cdir1', 'cspd2',
           'flag_cspd2', 'cdir2', 'flag_cdir2', 'cspd3', 'flag_cspd3', 'cdir3',
           'flag_cdir3', 'swvht1', 'flag_swvht1', 'swvht2', 'flag_swvht2',
           'mxwvht1', 'flag_mxwvht1', 'tp1', 'flag_tp1', 'tp2', 'flag_tp2',
           'wvdir1', 'flag_wvdir1', 'wvdir2', 'flag_wvdir2', 'wvspread1',
           'flag_wvspread1']]

    df = df[(df['date_time'] < datetime(2021,6,23,13,0,0))|(df['date_time'] > datetime(2021,6,24,13,0,0))]

    return df

def calculate_distance(df):
    coordinates = []
    for index, row in df.iterrows():
        coordinate = [row['lat'], row['lon']]
        coordinates.append(coordinate)


    deployment_loc = [-25.508, -42.736]
    df['coordinates'] = coordinates


    df['distance'] = df.apply(lambda row: haversine(row, deployment_loc[1], deployment_loc[0]), axis=1)

    df['veloc'] = df['distance'].diff()/(df['date_time'].diff().dt.total_seconds()/3600)

    return df

def plot_map(df):

    deployment_loc = [-25.508, -42.736]

    m = folium.Map(location=deployment_loc, zoom_start=13)

    for index, row in df.iterrows():
        popup = str(row['date_time']) + ' - onda ' + \
         str(row['wspd']) + 'm/s / ' + str(row['wdir']) + ' - veloc ' + str(round(row['veloc'],3)) + 'nós'
        folium.Marker(row['coordinates'], tooltip=popup).add_to(m)

    folium.Marker(
        df['coordinates'].iloc[-1],
        tooltip=popup,
        icon=folium.Icon(icon_color="red", color='red')
    ).add_to(m)

    folium.Circle(deployment_loc, radius=1300).add_to(m)
    folium_static(m)

def plot_graphs(df, variables):

    fig = go.Figure()
    for variable in variables:
        name = f"flag_{variable}"
        df.loc[df[name] > 0, variable] = np.nan
        fig.add_trace(go.Scatter(x=df['date_time'], y=df[variable],
                            mode='lines',
                            name=variable))
    st.plotly_chart(fig)

if __name__ == "__main__":
    df = get_data()

    df = calculate_distance(df)

    plot_map(df)

    plot_graphs(df)
