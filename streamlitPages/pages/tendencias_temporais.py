# tendencias_temporais.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import load_data

# --- Configuração da Página ---
st.set_page_config(page_title="Análise de Tendências Temporais", layout="wide")

# --- Carregamento dos Dados ---
# Garante que os dados sejam carregados apenas uma vez
@st.cache_data
def load_cached_data():
    return load_data()

df = load_cached_data()

# --- Título do Dashboard ---
st.title("🎬 Dashboard de Análise de Tendências Temporais")
st.markdown("Explore como as métricas de orçamento, bilheteria e avaliação de filmes evoluíram ao longo do tempo.")

# --- Filtros ---
st.header("🔍 Filtros Interativos")
min_year = int(df['ReleaseYear'].min())
max_year = int(df['ReleaseYear'].max())

year_range = st.slider(
    "Selecione o período que deseja analisar:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year) # Inicia com o período completo selecionado
)

# --- Aplicação dos Filtros ---
df_filtered = df[(df['ReleaseYear'] >= year_range[0]) & (df['ReleaseYear'] <= year_range[1])]

if df_filtered.empty:
    st.warning("⚠️ Nenhum dado disponível para o período selecionado. Por favor, ajuste o filtro.")
    st.stop()

# --- Análise de Dados ---
# Agrupando os dados pelo ano de lançamento após filtrar
df_temporal = df_filtered.groupby('ReleaseYear').agg({
    'BudgetUSD': 'mean',
    'Global_BoxOfficeUSD': 'mean',
    'US_BoxOfficeUSD': 'mean',
    'IMDbRating': 'mean',
    'Title': 'count'
}).reset_index()

# --- Visualizações ---
st.header("📊 Análise Gráfica da Indústria Cinematográfica")

# Organizando os gráficos em uma grade 2x2
col1, col2 = st.columns(2)

with col1:
    # 1. Evolução do orçamento médio ao longo dos anos
    st.subheader("Evolução do Orçamento Médio")
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1.plot(df_temporal['ReleaseYear'], df_temporal['BudgetUSD'] / 1e6,
             marker='o', linewidth=2, markersize=4, color='#2E86AB')
    ax1.fill_between(df_temporal['ReleaseYear'], df_temporal['BudgetUSD'] / 1e6,
                     alpha=0.3, color='#2E86AB')
    ax1.set_xlabel('Ano de Lançamento')
    ax1.set_ylabel('Orçamento Médio (Milhões USD)')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(df_temporal['ReleaseYear'].min(), df_temporal['ReleaseYear'].max())
    st.pyplot(fig1)

    # 3. Quantidade de filmes lançados por ano
    st.subheader("Quantidade de Filmes Lançados por Ano")
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    colors = plt.cm.coolwarm(np.linspace(0.3, 0.8, len(df_temporal)))
    ax3.bar(df_temporal['ReleaseYear'], df_temporal['Title'], color=colors)
    ax3.set_xlabel('Ano de Lançamento')
    ax3.set_ylabel('Quantidade de Filmes')
    ax3.grid(True, alpha=0.3, axis='y')
    st.pyplot(fig3)

with col2:
    # 2. Comparação Bilheteria Global vs US
    st.subheader("Evolução da Bilheteria: Global vs. USA")
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.plot(df_temporal['ReleaseYear'], df_temporal['Global_BoxOfficeUSD'] / 1e6,
             label='Global', marker='s', linewidth=2, color='#A23B72')
    ax2.plot(df_temporal['ReleaseYear'], df_temporal['US_BoxOfficeUSD'] / 1e6,
             label='USA', marker='^', linewidth=2, color='#F18F01')
    ax2.set_xlabel('Ano de Lançamento')
    ax2.set_ylabel('Bilheteria Média (Milhões USD)')
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    st.pyplot(fig2)

    # 4. Evolução da nota média IMDb
    st.subheader("Evolução da Nota Média no IMDb")
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    ax4.plot(df_temporal['ReleaseYear'], df_temporal['IMDbRating'],
             marker='o', linewidth=2, markersize=6, color='#C73E1D')
    ax4.fill_between(df_temporal['ReleaseYear'], df_temporal['IMDbRating'],
                     df_temporal['IMDbRating'].min() * 0.95, alpha=0.3, color='#C73E1D')
    ax4.set_xlabel('Ano de Lançamento')
    ax4.set_ylabel('Nota Média IMDb')
    ax4.set_ylim(5.5, max(7.5, df_temporal['IMDbRating'].max() * 1.05)) # Ajuste dinâmico do eixo Y
    ax4.grid(True, alpha=0.3)
    st.pyplot(fig4)

# --- Análise por Década ---
st.header("🗓️ Análise Consolidada por Década")

# Adiciona a coluna 'Decade' e agrupa os dados
df_filtered['Decade'] = (df_filtered['ReleaseYear'] // 10) * 10
decade_analysis = df_filtered.groupby('Decade').agg({
    'BudgetUSD': 'mean',
    'Global_BoxOfficeUSD': 'mean',
    'ROI': 'mean',
    'IMDbRating': 'mean'
})

# Renomeando colunas para melhor apresentação
decade_analysis.columns = [
    "Orçamento Médio (USD)",
    "Bilheteria Global Média (USD)",
    "ROI Médio (%)",
    "Nota Média IMDb"
]

# --- Layout de Colunas e Ordenação para a Tabela de Década ---
col_decade1, col_decade2 = st.columns([0.7, 0.3])

with col_decade2:
    st.subheader("Ordenar por:")
    
    # Opções de ordenação baseadas nas colunas da tabela de década
    decade_sort_options = [
        "Década (Mais Recente)", 
        "Bilheteria Global Média (USD)", 
        "Orçamento Médio (USD)", 
        "ROI Médio (%)", 
        "Nota Média IMDb"
    ]
    
    decade_sort_by = st.radio(
        "Selecione o critério para a tabela de décadas:",
        options=decade_sort_options,
        label_visibility="collapsed",
        key='decade_sorter' # Chave única para este widget de rádio
    )

# Lógica de Ordenação para a tabela de década
if decade_sort_by == "Década (Mais Recente)":
    # Ordena pelo índice (década) em ordem decrescente
    sorted_decade_df = decade_analysis.sort_index(ascending=False)
else:
    # Ordena pela coluna selecionada em ordem decrescente
    sorted_decade_df = decade_analysis.sort_values(by=decade_sort_by, ascending=False)


with col_decade1:
    st.subheader("Desempenho por Década") # Adicionei um subheader para clareza
    
    # Exibe o DataFrame de década JÁ ORDENADO
    st.dataframe(
        sorted_decade_df.style.format({
            "Orçamento Médio (USD)": "${:,.0f}",
            "Bilheteria Global Média (USD)": "${:,.0f}",
            "ROI Médio (%)": "{:.2f}%",
            "Nota Média IMDb": "{:.2f}"
        }), 
        use_container_width=True
    )


st.info("""
**Observações:**
- **Orçamento e Bilheteria:** Os valores são apresentados em médias por ano para normalizar a análise.
- **ROI (Retorno sobre Investimento):** O ROI médio por década oferece uma visão de longo prazo da rentabilidade.
- **Nota IMDb:** Reflete a percepção de qualidade dos filmes pelo público ao longo do tempo.
""")