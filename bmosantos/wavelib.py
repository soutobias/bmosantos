import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
from datetime import datetime, timedelta
import streamlit as st
import seaborn as sns
from scipy.stats import norm

def get_data(token):

    start_time = (datetime.utcnow() - timedelta(days=5)).strftime('%Y-%m-%d')
    time_now = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')
    url=f'http://remobsapi.herokuapp.com/api/v1/waves?buoy=2&start_date={start_time}&end_date={time_now}&token={token}'

    response = requests.get(url).json()
    df = pd.DataFrame(response)
    df = adjust_data(df.copy())

    df = create_norm(df.copy())

    return df


def adjust_data(df):

    df['buoy_id'] = pd.to_numeric(df['buoy_id'])
    df['data_id'] = pd.to_numeric(df['data_id'])
    df['period'] = pd.to_numeric(df['period'])
    df['energy'] = pd.to_numeric(df['energy'])
    df['wvdir'] = pd.to_numeric(df['wvdir'])
    df['spread'] = pd.to_numeric(df['spread'])
    df['mean_average_direction'] = pd.to_numeric(df['mean_average_direction'])
    df['spread_direction'] = pd.to_numeric(df['spread_direction'])
    df['date_time'] = pd.to_datetime(df['date_time'], format='%Y-%m-%dT%H:%M:%S.000Z')
    df.sort_values('date_time', inplace=True)
    df[(df['date_time'] > datetime(2021,6,23,13,0,0))&(df['date_time'] < datetime(2021,6,24,13,0,0))] = np.nan

    df['values'] = pd.cut(df['period'], [2, 4, 7.5, 12, 18.4])
    df['wvdir'] = df['wvdir'].astype(float)
    df = df.groupby(['date_time', 'values']).agg({'energy': 'sum', 'wvdir': 'mean'}).reset_index()

    df = df.dropna()

    df['wvdir'] = np.round(df['wvdir']).astype('int')

    return df

def create_norm(df):

    date_time_norm = []
    wvdir_norm = []
    energy_norm = []
    values_norm = []
    for index, row in df.iterrows():
        if row['date_time'].hour % 3 == 0:
            wvd  = np.arange(row['wvdir'] - 4.75, row['wvdir'] + 4.75, 0.4)
            ener = norm.pdf(np.arange(-11,11 , 1),0,4.7) * row['energy'] * 80
            ener = np.insert(ener,[0],[0])
            ener = np.append(ener, [0])
            for i in range(len(ener)):
                date_time_norm.append(row['date_time'])
                values_norm.append(row['values'])
                wvdir_norm.append(wvd[i])
                energy_norm.append(ener[i])

    final_df = pd.DataFrame(np.array([date_time_norm, values_norm, wvdir_norm, energy_norm]).T, \
                        columns=['date_time', 'period', 'wvdir', 'energy'])

    final_df['energy'] = final_df['energy'].astype(float) * 100
    final_df['wvdir'] = final_df['wvdir'].astype(float)

    return final_df


def plot_pleds(final_df):

    sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

    sns.color_palette("cubehelix", as_cmap=True)

    pal = sns.cubehelix_palette(10, rot=-.25, light=.7)

    g = sns.FacetGrid(final_df, row='date_time', hue='period', aspect=60, height=0.4)
    g.map(sns.lineplot, 'wvdir', 'energy')


    for ax in g.axes:
        for i in ax[0].lines:
            x1 = i.get_xydata()[:,0]
            y2 = i.get_xydata()[:,1]
            color = i.get_color()
            y1 = y2*0
            ax[0].fill_between(x1, y1=y1, y2=y2, color=color, alpha=0.5)
        ax[0].grid()
        ax[0].spines['right'].set_color('none')
        ax[0].spines['left'].set_color('none')
        ax[0].spines['bottom'].set_color('black')
        ax[0].spines['bottom'].set_alpha(0.3)
        ax[0].set_ylabel('')
        data = ax[0].title.get_text()[17:-16].replace('T', ' ') + "h"
        ax[0].text(0, 0.05, data, fontweight="bold", color=sns.xkcd_rgb['black'],
                ha="left", va="center", transform=ax[0].transAxes, fontsize=20)

    # g.map(label, label="date_time")
    g.set_titles("")
    g.set_xlabels("Direction", fontsize=25)

    # ticks = ['30', '60', '90', '120', '150', '180', '210', '240', '270', '300', '330', '360']
    g.set_xticklabels(fontsize=25)
    g.set (yticks=[])
    # g.set(ylim=(10, max(total_df['name'])), xlim=(min(total_df['value']), max(total_df['value']) - 1))
    # g.set(xlim=(0, 359))

    # Set the subplots to overlap
    g.fig.subplots_adjust(hspace=-.9)
    # plt.legend(loc="lower left", ncol=5)
    label = ['2.0-4.0s', '4.0-7.5s', '7.5-12.0s', '12.0-18.4s']
    plt.legend(bbox_to_anchor=(0.5, -0.3), loc=9, ncol=5, facecolor='white', \
               fontsize=30, markerscale=20, labels=label, title='Wave Period', \
              title_fontsize=20)
    # Remove axes details that don't play well with overlap
    # plt.savefig("pleds.png")
    st.pyplot(g)
