import streamlit as st
import altair as alt
import pandas as pd
from library.conexao import Scraper

# Configuração de layout
st.set_page_config(layout="wide")

# Função para carregar e processar os dados
def load_data():
    obj = Scraper()

    # Obtendo dados Twitch e Steam
    df_steam = obj.get_dados_steam()
    df_twitch = obj.get_dados_twitch()
    obj.fechar_navegador()

    # DF da união das duas tabelas
    df_merge = df_twitch.merge(df_steam, on='Jogo', how='inner')
    return df_steam, df_twitch, df_merge

# Função para plotar gráficos
def plot_charts(df_steam, df_twitch, df_merge):
    # Gráficos de categorias da Twitch
    st.header("Principais Categorias da Twitch")

    col1, col2 = st.columns(2)

    with col1:
        twitch_bar_chart = alt.Chart(df_twitch.head(10)).mark_bar().encode(
            x=alt.X('Jogo', sort=None, title='Categoria'),
            y=alt.Y('Viewer Hours', title='Horas Assistidas'),
            color=alt.Color('Viewer Hours', scale=alt.Scale(scheme='blues')),
            tooltip=['Jogo', 'Viewer Hours']
        ).properties(
            title="Horas Assistidas por Categoria - Twitch"
        )
        st.altair_chart(twitch_bar_chart, use_container_width=True)

    with col2:
        twitch_avg_channels_chart = alt.Chart(df_twitch.sort_values(by='Avg Live Channels', ascending=False).head(10)).mark_bar().encode(
            x=alt.X('Avg Live Channels', title='Canais ao Vivo (Média)'),
            y=alt.Y('Jogo', sort=None, title='Categoria'),
            color=alt.Color('Avg Live Channels', scale=alt.Scale(scheme='greens')),
            tooltip=['Jogo', 'Avg Live Channels']
        ).properties(
            title="Média de Canais ao Vivo por Categoria - Twitch"
        )
        st.altair_chart(twitch_avg_channels_chart, use_container_width=True)

    # Gráficos de jogos populares na Steam
    st.header("Jogos Mais Populares na Steam")

    col3, col4 = st.columns(2)

    with col3:
        steam_bar_chart = alt.Chart(df_steam.sort_values(by="jogadores_at_moment", ascending=False).head(10)).mark_bar().encode(
            x=alt.X('Jogo', sort=None, title="Jogo"),
            y=alt.Y('jogadores_at_moment', title="Jogadores no Momento"),
            color=alt.Color('jogadores_at_moment', scale=alt.Scale(scheme='reds')),
            tooltip=['Jogo', 'jogadores_at_moment']
        ).properties(
            title="Jogadores no Momento - Steam"
        )
        st.altair_chart(steam_bar_chart, use_container_width=True)

    with col4:
        steam_line_chart = alt.Chart(df_steam.head(10)).mark_line(point=True).encode(
            x=alt.X('Jogo', sort=None, title="Jogo"),
            y=alt.Y('24h_peek', title="Pico de 24h"),
            color=alt.value('orange'),
            tooltip=['Jogo', '24h_peek']
        ).properties(
            title="Pico de Jogadores (24h) - Steam"
        )
        st.altair_chart(steam_line_chart, use_container_width=True)

    # Gráfico de correlação entre Twitch e Steam
    st.header("Correlação Entre Popularidade na Twitch e Steam")

    scatter_chart = alt.Chart(df_merge).mark_point(filled=True, size=100).encode(
        x=alt.X('jogadores_at_moment:Q', title='Jogadores no Momento - Steam'),
        y=alt.Y('Viewer Hours:Q', title='Horas Assistidas - Twitch'),
        color=alt.Color('Jogo:N', scale=alt.Scale(scheme='set2')),
        tooltip=['Jogo', 'jogadores_at_moment', 'Viewer Hours']
    ).properties(
        title="Relação Entre Jogos Mais Assistidos e Mais Jogados"
    )
    st.altair_chart(scatter_chart, use_container_width=True)

    # Disponibilização da Base de dados
    st.markdown('---')
    st.subheader('Bases de Dados')

    col5, col6 = st.columns(2)

    with col5:
        with st.expander("Base de Dados da Twitch"):
            st.dataframe(df_twitch, use_container_width=True)

    with col6:
        with st.expander("Base de Dados da Steam"):
            st.dataframe(df_steam, use_container_width=True)

# Título do Dashboard
st.title("Dashboard de Análise: Twitch vs. Steam")

# Adiciona o botão na barra lateral
st.sidebar.header("Configurações")
if st.sidebar.button("Atualizar Dados"):
    df_steam, df_twitch, df_merge = load_data()
    plot_charts(df_steam, df_twitch, df_merge)
else:
    # Carrega e exibe os gráficos na primeira abertura
    df_steam, df_twitch, df_merge = load_data()
    plot_charts(df_steam, df_twitch, df_merge)
