import streamlit as st
from bmosantos import lib
from bmosantos import bmorawlib
from bmosantos import wavelib

from dotenv import load_dotenv
import os
from PIL import Image

load_dotenv()
pnboia_img = Image.open('images/logo_pnboia.png')
remo_img = Image.open('images/logo_remo.png')


df = lib.get_data(os.getenv('REMOBS_TOKEN'))

raw_df = bmorawlib.get_data(os.getenv('REMOBS_TOKEN'))


# wave_df = wavelib.get_data(os.getenv('REMOBS_TOKEN'))

df = lib.calculate_distance(df)

st.image([pnboia_img, remo_img], caption=None, width=50, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

st.markdown("<h1 style='text-align: center;'>BMO-BR BACIA DE CAMPOS</h1>", unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center; margin: 0;'>{(df['date_time'].min().strftime('%d-%m-%Y %H:%M'))}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; margin: 0;'>até</p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; margin: 0;'>{(df['date_time'].max().strftime('%d-%m-%Y %H:%M'))}</p>", unsafe_allow_html=True)

st.markdown(f"<h3 style='text-align: center;'>Última posição:</h3>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center; margin: 0;'>LAT {(df['lat'].iloc[-1])}, LON {(df['lon'].iloc[-1])}</h3>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>MAPA</h2>", unsafe_allow_html=True)

lib.plot_map(df)

st.markdown("<h2 style='text-align: center;'>GRÁFICOS</h2>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Dados Brutos de Vento</h2>", unsafe_allow_html=True)

st.write("### Velocidade do vento")
bmorawlib.plot_graphs(raw_df, {'wspd1':'Velocidade do Vento 3.6 m', 'wspd2': 'Velocidade do Vento 3.2 m'})
st.write("### Direção do vento")
bmorawlib.plot_graphs(raw_df, {'wdir1':'Direção do Vento 3.6 m', 'wdir2': 'Direção do Vento 3.2 m'})

st.markdown("<h2 style='text-align: center;'>Melhor Vento</h2>", unsafe_allow_html=True)

st.write("### Velocidade do vento")
lib.plot_graphs(df, {'wspd':'Velocidade do Vento 10 m'})
st.write("### Direção do vento")
lib.plot_graphs(df, {'wdir':'Direção do Vento 10 m'})

st.markdown("<h2 style='text-align: center;'>Altura de Ondas</h2>", unsafe_allow_html=True)

lib.plot_graphs(df, {'swvht1':'Triaxys', 'swvht2':'UCMO-Messen'})
# st.write("### Direção de ondas")
# lib.plot_graphs(df, ['wvdir1', 'wvdir2'])
st.write("### Período das ondas")
lib.plot_graphs(df, {'tp1':'Triaxys', 'tp2':'UCMO-Messen'})

st.markdown("<h2 style='text-align: center;'>Intensidade das Correntes</h2>", unsafe_allow_html=True)

lib.plot_graphs(df, {'cspd1':'Velocidade Correntes 4.5 m', 'cspd2':'Velocidade Correntes 7.5 m', 'cspd3':'Velocidade Correntes 10.5 m'})
st.write("### Direção das correntes")
lib.plot_graphs(df, {'cdir1':'Direção Correntes 4.5 m', 'cdir2':'Direção Correntes 7.5 m', 'cdir3':'Direção Correntes 10.5 m'})

# st.write("### Espectro Direcional de ondas")
# wavelib.plot_pleds(wave_df)
