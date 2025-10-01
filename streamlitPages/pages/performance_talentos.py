# performance_talentos.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import load_data

# --- Configuração da Página ---
st.set_page_config(page_title="Performance de Talentos", layout="wide")

# --- Carregamento dos Dados ---
@st.cache_data
def load_cached_data():
    return load_data()

df = load_cached_data()

# --- Título do Dashboard ---
st.title("🏆 Análise de Performance: Diretores e Atores")
st.markdown("Compare o desempenho de diretores e atores principais com base em métricas financeiras e de avaliação.")

# --- Filtros Interativos ---
st.header("🔍 Filtros da Análise")

# Colunas para organizar os filtros
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Filtro para escolher entre Diretor e Ator
    talent_type = st.radio(
        "Selecione o Talento para Análise:",
        ('Diretor', 'Ator Principal'),
        key='talent_type'
    )
    # Define a coluna do DataFrame a ser usada com base na seleção
    group_col = 'Director' if talent_type == 'Diretor' else 'LeadActor'

with col2:
    # Filtro para o número mínimo de filmes
    min_films = st.slider(
        "Mínimo de Filmes Realizados:",
        min_value=1,
        max_value=10,
        value=2, # Valor padrão de 2 filmes
        help="Filtra talentos que participaram de um número mínimo de filmes na amostra."
    )

with col3:
    # Filtro para a métrica de ordenação do Top N
    sort_metric = st.selectbox(
        "Ordenar Top N por:",
        options=['Total_Bilheteria', 'ROI_Médio', 'Rating_Médio', 'Bilheteria_por_Filme'],
        index=0 # 'Total_Bilheteria' como padrão
    )

with col4:
    # Filtro para definir o tamanho do Top (N)
    top_n = st.number_input(
        f"Número de {talent_type}es no Top:",
        min_value=5,
        max_value=25,
        value=15, # Padrão Top 15
        step=1
    )


# --- Processamento dos Dados ---
# Agrupamento e cálculo das estatísticas com base no talento selecionado
stats = df.groupby(group_col).agg({
    'Global_BoxOfficeUSD': 'sum',
    'Title': 'count',
    'IMDbRating': 'mean',
    'ROI': 'mean'
}).round(2)

stats.columns = ['Total_Bilheteria', 'Num_Filmes', 'Rating_Médio', 'ROI_Médio']
stats['Bilheteria_por_Filme'] = (stats['Total_Bilheteria'] / stats['Num_Filmes']).round(2)

# Aplicando o filtro de número mínimo de filmes
stats_filtered = stats[stats['Num_Filmes'] >= min_films]

# Selecionando o Top N com base na métrica escolhida
top_talents = stats_filtered.nlargest(top_n, sort_metric)


# --- Visualizações ---
st.header(f"📊 Gráficos de Performance para {talent_type}es")

if top_talents.empty:
    st.warning(f"Nenhum {talent_type} atende aos critérios de filtro selecionados.")
    st.stop()

# Layout em duas colunas para os gráficos
plot_col1, plot_col2 = st.columns(2)

with plot_col1:
    # Gráfico 1: Top N Talentos pela métrica selecionada
    st.subheader(f"Top {top_n} {talent_type}es por {sort_metric.replace('_', ' ')}")
    
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    
    # Invertendo a ordem para o maior valor ficar no topo
    data_to_plot = top_talents[sort_metric].sort_values(ascending=True)
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(data_to_plot)))
    
    ax1.barh(data_to_plot.index, data_to_plot, color=colors)
    ax1.set_xlabel(f"{sort_metric.replace('_', ' ')}")
    ax1.grid(True, alpha=0.3, axis='x')
    
    st.pyplot(fig1)

with plot_col2:
    # Gráfico 2: Scatter plot de Produtividade vs. Performance
    st.subheader("Produtividade vs. Performance Financeira")
    
    fig2, ax2 = plt.subplots(figsize=(8, 8))
    
    scatter = ax2.scatter(
        stats_filtered['Num_Filmes'],
        stats_filtered['Bilheteria_por_Filme'] / 1e6, # Em milhões
        c=stats_filtered['Rating_Médio'],
        s=100,
        alpha=0.7,
        cmap='coolwarm'
    )
    
    ax2.set_xlabel('Número de Filmes')
    ax2.set_ylabel('Bilheteria Média por Filme (Milhões USD)')
    ax2.grid(True, alpha=0.3)
    
    # Adicionando a colorbar
    cbar = plt.colorbar(scatter, ax=ax2)
    cbar.set_label('Rating IMDb Médio')
    
    st.pyplot(fig2)


# --- Tabela de Dados ---
st.header(f"📋 Tabela de Dados: Top {top_n} {talent_type}es")
st.dataframe(
    top_talents.style.format({
        'Total_Bilheteria': '${:,.0f}',
        'Bilheteria_por_Filme': '${:,.0f}',
        'ROI_Médio': '{:.2f}%',
        'Rating_Médio': '{:.2f}'
    }),
    use_container_width=True
)