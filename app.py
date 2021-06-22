import streamlit as st
from bmosantos.lib import *
from dotenv import load_dotenv
import os

load_dotenv()

df = get_data(os.getenv('REMOBS_TOKEN'))

df = calculate_distance(df)

st.write("# DADOS BMO-BR BACIA DE SANTOS")
st.write(f"### {(df['date_time'].min())} até {(df['date_time'].max())}")
st.write(f"### Última posição: LAT {(df['lat'].iloc[-1])}, LON {(df['lon'].iloc[-1])}")


st.write("## MAPA")

plot_map(df)

st.write("## GRÁFICOS")

st.write("### Velocidade do vento")
plot_graphs(df, ['wspd'])
st.write("### Direção do vento")
plot_graphs(df, ['wdir'])


st.write("### Altura de ondas")
plot_graphs(df, ['swvht1', 'swvht2'])
st.write("### Direção de ondas")
plot_graphs(df, ['wvdir1', 'wvdir2'])
st.write("### Período das ondas")
plot_graphs(df, ['tp1', 'tp2'])


st.write("### Intensidade das Correntes")
plot_graphs(df, ['cspd1', 'cspd2', 'cspd3'])
st.write("### Direção das correntes")
plot_graphs(df, ['cdir1', 'cdir2', 'cdir3'])
