# analise_paises.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import load_data

# --- Configuração da Página ---
st.set_page_config(page_title="Análise por Países", layout="wide")

# --- Carregamento dos Dados ---
@st.cache_data
def load_cached_data():
    return load_data()

df = load_cached_data()

# --- Título do Dashboard ---
st.title("🌎 Análise Comparativa da Indústria Cinematográfica por País")
st.markdown("Explore e compare as métricas de produção, performance financeira e avaliação dos filmes de diferentes países.")

# --- Processamento de Dados (executado antes dos filtros) ---
# Agrupamento para obter as estatísticas de todos os países
country_stats = df.groupby('Country').agg({
    'Title': 'count',
    'BudgetUSD': 'mean',
    'Global_BoxOfficeUSD': 'mean',
    'IMDbRating': 'mean',
    'ROI': 'mean'
}).round(2)
country_stats.columns = ['Num_Filmes', 'Orçamento_Médio', 'Bilheteria_Média', 'Rating_Médio', 'ROI_Médio']
country_stats = country_stats.sort_values('Num_Filmes', ascending=False)

# --- Filtros Interativos ---
st.header("🔍 Filtros da Análise")

# Filtro para selecionar países
all_countries = country_stats.index.tolist()
default_top_10 = all_countries[:10] # Pré-seleciona os 10 países com mais filmes

selected_countries = st.multiselect(
    'Selecione os países que deseja analisar:',
    options=all_countries,
    default=default_top_10
)

# --- Validação dos Filtros ---
if not selected_countries:
    st.warning("⚠️ Por favor, selecione pelo menos um país para visualizar a análise.")
    st.stop()

# Filtra o DataFrame de estatísticas com base na seleção
stats_filtered = country_stats.loc[selected_countries]

# --- Métricas Principais (KPIs) ---
st.header("📊 Visão Geral dos Países Selecionados")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Países na Análise", len(selected_countries))
kpi2.metric("Total de Filmes (na amostra)", f"{stats_filtered['Num_Filmes'].sum():,}")
kpi3.metric("ROI Médio Geral", f"{stats_filtered['ROI_Médio'].mean():.2f}%")

# --- Visualizações ---
st.header("📈 Gráficos Comparativos")

# Layout para os gráficos
col1, col2 = st.columns(2)

with col1:
    # 1. Gráfico de Pizza: Distribuição de Filmes
    st.subheader("Distribuição de Filmes por País")
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    colors_pie = plt.cm.Set3(np.linspace(0, 1, len(stats_filtered)))
    
    data_pie = stats_filtered['Num_Filmes']
    labels_pie = stats_filtered.index
    
    wedges, texts, autotexts = ax1.pie(
        data_pie,
        labels=labels_pie,
        autopct='%1.1f%%',
        colors=colors_pie,
        startangle=90
    )
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(10)
    st.pyplot(fig1)

    # 2. Gráfico de Barras: Orçamento Médio
    st.subheader("Orçamento Médio de Produção")
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    data_bar = stats_filtered['Orçamento_Médio'] / 1e6
    colors_bar = plt.cm.YlOrRd(np.linspace(0.4, 0.9, len(data_bar)))
    ax2.barh(data_bar.index, data_bar, color=colors_bar)
    ax2.set_xlabel('Orçamento Médio (Milhões USD)')
    ax2.grid(True, alpha=0.3, axis='x')
    st.pyplot(fig2)

    # 3. Gráfico de Barras: Rating Médio
    st.subheader("Avaliação Média (IMDb)")
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    data_rating = stats_filtered['Rating_Médio']
    colors_rating = plt.cm.Purples(np.linspace(0.4, 0.9, len(data_rating)))
    ax3.barh(data_rating.index, data_rating, color=colors_rating)
    ax3.set_xlabel('Rating IMDb Médio')
    ax3.set_xlim(left=max(0, data_rating.min() - 0.5)) # Ajuste dinâmico do eixo
    ax3.grid(True, alpha=0.3, axis='x')
    st.pyplot(fig3)


with col2:
    st.subheader("Relação Orçamento vs. Bilheteria")
    fig4, ax4 = plt.subplots(figsize=(8, 6))
    
    # --- CORREÇÃO APLICADA AQUI ---
    # 1. Defina o tamanho mínimo e máximo que você quer para as bolhas
    min_bubble_size = 30
    max_bubble_size = 1000

    # 2. Pega os valores mínimo e máximo da sua variável de tamanho
    min_val = stats_filtered['Num_Filmes'].min()
    max_val = stats_filtered['Num_Filmes'].max()

    # 3. Normaliza os tamanhos para o intervalo desejado
    # Evita divisão por zero se todos os valores forem iguais
    if max_val == min_val:
        scaled_sizes = [min_bubble_size] * len(stats_filtered)
    else:
        scaled_sizes = min_bubble_size + (stats_filtered['Num_Filmes'] - min_val) * \
                       (max_bubble_size - min_bubble_size) / (max_val - min_val)
    # --- FIM DA CORREÇÃO ---

    scatter = ax4.scatter(
        stats_filtered['Orçamento_Médio'] / 1e6,
        stats_filtered['Bilheteria_Média'] / 1e6,
        s=scaled_sizes * 5, # Use os tamanhos normalizados aqui
        c=stats_filtered['ROI_Médio'],
        cmap='coolwarm',
        alpha=0.7, # Reduzir um pouco a opacidade ajuda na sobreposição
        edgecolors='black',
        linewidth=1
    )
    
    ax4.set_xlabel('Orçamento Médio (Milhões USD)')
    ax4.set_ylabel('Bilheteria Média (Milhões USD)')
    ax4.grid(True, alpha=0.3)
    cbar = plt.colorbar(scatter, ax=ax4)
    cbar.set_label('ROI Médio (%)')
    
    st.pyplot(fig4)

    # 5. Gráfico de Barras: Bilheteria Média
    st.subheader("Bilheteria Média Global")
    fig5, ax5 = plt.subplots(figsize=(8, 6))
    data_box = stats_filtered['Bilheteria_Média'] / 1e6
    colors_box = plt.cm.GnBu(np.linspace(0.4, 0.9, len(data_box)))
    ax5.barh(data_box.index, data_box, color=colors_box)
    ax5.set_xlabel('Bilheteria Média (Milhões USD)')
    ax5.grid(True, alpha=0.3, axis='x')
    st.pyplot(fig5)

    # 6. Gráfico de Barras: ROI Médio
    st.subheader("Retorno sobre Investimento (ROI) Médio")
    fig6, ax6 = plt.subplots(figsize=(8, 6))
    data_roi = stats_filtered['ROI_Médio']
    colors_roi = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(data_roi)))
    ax6.barh(data_roi.index, data_roi, color=colors_roi)
    ax6.set_xlabel('ROI Médio (%)')
    ax6.grid(True, alpha=0.3, axis='x')
    st.pyplot(fig6)


st.header("📋 Dados Detalhados")

col1, col2 = st.columns([0.7, 0.3])
with col2:
    st.subheader("Ordenar por:")
    
    # Opções de ordenação baseadas nas colunas do DataFrame
    sort_options = ['Bilheteria_Média', 'Orçamento_Médio', 'ROI_Médio', 'Rating_Médio']
    
    sort_by_option = st.radio(
        "Selecione o critério de ordenação:",
        options=sort_options,
        label_visibility="collapsed" # Oculta o label principal do radio
    )

    sorted_df = stats_filtered.sort_values(by=sort_by_option, ascending=False)

with col1:
    # Tabela 1: Estatísticas Gerais
    st.subheader("Estatísticas Consolidadas por País")
    
    st.dataframe(
        sorted_df.style.format({
            'Orçamento_Médio': '${:,.0f}',
            'Bilheteria_Média': '${:,.0f}',
            'ROI_Médio': '{:.2f}%',
            'Rating_Médio': '{:.2f}'
        }),
        use_container_width=True
    )


# Tabela 2: Performance Internacional
st.subheader("Performance no Mercado Internacional")
df_filtered_countries = df[df['Country'].isin(selected_countries)]
df_filtered_countries['International_BoxOffice'] = df_filtered_countries['Global_BoxOfficeUSD'] - df_filtered_countries['US_BoxOfficeUSD']
# Evitar divisão por zero se bilheteria global for 0
df_filtered_countries['International_Percentage'] = (
    df_filtered_countries['International_BoxOffice'] / df_filtered_countries['Global_BoxOfficeUSD'] * 100
).fillna(0)

international_by_country = df_filtered_countries.groupby('Country')['International_Percentage'].mean().round(2)
international_by_country = international_by_country.sort_values(ascending=False).to_frame()

st.dataframe(
    international_by_country.style.format('{:.2f}%'),
    use_container_width=True
)