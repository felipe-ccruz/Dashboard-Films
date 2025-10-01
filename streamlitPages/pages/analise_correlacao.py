# analise_correlacao.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from utils import load_data

# --- Configuração da Página ---
st.set_page_config(page_title="Análise de Correlações", layout="wide")

# --- Carregamento dos Dados ---
@st.cache_data
def load_cached_data():
    return load_data()

df = load_cached_data()

# --- Título do Dashboard ---
st.title("🔗 Dashboard de Análise de Correlações")
st.markdown("""
Esta página permite explorar a relação entre as diferentes variáveis numéricas do dataset. 
Use os filtros para construir um mapa de calor de correlações personalizado.
""")

# --- Filtros ---
st.header("🔍 Filtros de Variáveis")

# Lista de todas as variáveis numéricas disponíveis para seleção
all_numeric_cols = [
    'BudgetUSD', 'US_BoxOfficeUSD', 'Global_BoxOfficeUSD',
    'Opening_Day_SalesUSD', 'One_Week_SalesUSD',
    'IMDbRating', 'RottenTomatoesScore', 'NumVotesIMDb', 'NumVotesRT', 'ROI'
]

# Filtro para selecionar as variáveis para a matriz de correlação
selected_cols = st.multiselect(
    'Selecione duas ou mais variáveis para analisar:',
    options=all_numeric_cols,
    default=all_numeric_cols  # Todas as colunas são selecionadas por padrão
)

# --- Lógica de Validação ---
if len(selected_cols) < 2:
    st.warning("⚠️ Por favor, selecione pelo menos duas variáveis para calcular a correlação.")
    st.stop()

# --- Análise de Correlação ---
# Calculando a matriz de correlação com base nas colunas selecionadas
correlation_matrix = df[selected_cols].corr()

# --- Visualização do Mapa de Calor ---
st.header("🌡️ Mapa de Calor (Heatmap) de Correlações")

# Ocupa a largura total da coluna para melhor visualização
fig, ax = plt.subplots(figsize=(14, 10))

# Máscara para ocultar a parte superior da matriz (triângulo superior)
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))

sns.heatmap(
    correlation_matrix,
    mask=mask,
    annot=True,
    fmt='.2f',          # Formata os números com duas casas decimais
    cmap='RdBu_r',      # Paleta de cores (Vermelho-Branco-Azul)
    center=0,           # Centraliza a escala de cores em zero
    square=True,
    linewidths=1,
    cbar_kws={"shrink": 0.8, "label": "Coeficiente de Correlação"},
    vmin=-1, vmax=1,    # Garante que a escala de cores vá de -1 a 1
    ax=ax
)

ax.set_title('Mapa de Correlações entre as Variáveis Selecionadas', fontsize=16, pad=20)
st.pyplot(fig)

st.info("""
**Como interpretar o mapa:**
- **Valores próximos de +1 (azul escuro):** Indicam uma correlação positiva forte. Quando uma variável aumenta, a outra tende a aumentar também.
- **Valores próximos de -1 (vermelho escuro):** Indicam uma correlação negativa forte. Quando uma variável aumenta, a outra tende a diminuir.
- **Valores próximos de 0 (branco/cinza):** Indicam pouca ou nenhuma correlação linear entre as variáveis.
""")


# --- Análise de Correlações Fortes ---
st.header("💡 Identificando as Relações Mais Fortes")

# Slider para definir o que é uma "correlação forte"
threshold = st.slider(
    'Defina o limiar para correlação forte (valor absoluto):',
    min_value=0.5,
    max_value=1.0,
    value=0.7,  # Valor padrão de 0.7
    step=0.05
)

strong_correlations = []
# Iterando sobre a matriz para encontrar correlações acima do limiar
for i in range(len(correlation_matrix.columns)):
    for j in range(i + 1, len(correlation_matrix.columns)):
        corr_value = correlation_matrix.iloc[i, j]
        if abs(corr_value) > threshold:
            strong_correlations.append({
                'Variável 1': correlation_matrix.columns[i],
                'Variável 2': correlation_matrix.columns[j],
                'Correlação': round(corr_value, 3)
            })

if strong_correlations:
    # Criando um DataFrame para exibir os resultados de forma organizada
    df_strong = pd.DataFrame(strong_correlations)
    
    # Ordenando pela correlação mais forte (em valor absoluto)
    df_strong['Correlação_Abs'] = df_strong['Correlação'].abs()
    df_strong = df_strong.sort_values(by='Correlação_Abs', ascending=False).drop(columns=['Correlação_Abs'])
    
    st.subheader(f"Principais Relações com Correlação > {threshold}")
    st.dataframe(df_strong, use_container_width=True, hide_index=True)
else:
    st.success(f"✅ Nenhuma correlação com valor absoluto maior que {threshold} foi encontrada entre as variáveis selecionadas.")