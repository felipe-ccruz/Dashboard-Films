import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração da página
st.set_page_config(page_title="Análise de ROI - Filmes", layout="wide")

### SIDEBAR ###
st.sidebar.header("📖 Páginas")
st.sidebar.markdown("[Home](./streamlitPages/home.py)")
st.sidebar.markdown("[Análise de ROI](./streamlitPages/roiGenre.py)")

# Título do dashboard
st.title("🎬 Dashboard de Análise de ROI por Gênero de Filme")

### Filtros ###
## FILTRO ANO
col1, gap, col2 = st.columns([0.55, 0.15, 0.3])
with col1:
    st.subheader("Período de Lançamento")
    min_year = int(df['ReleaseYear'].min())
    max_year = int(df['ReleaseYear'].max())

    year_range = st.slider(
        "Selecione o período (anos)",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        label_visibility="collapsed" # Oculta o label do slider para não repetir
    )
with gap:
    st.write("")
## FILTRO GENERO
with col2:
    selected_genres = []
    st.subheader("Gêneros")
    subcol1, subcol2 = st.columns(2)
    with subcol1:
        available_genres1 = ['Comedy', 'Documentary', 'Drama', 'Horror']
        for genre in available_genres1:
            if st.checkbox(genre, value=True):
                selected_genres.append(genre)
    with subcol2:
        available_genres2 = ['Action', 'Thriller', 'Romance', 'Sci-Fi']
        for genre in available_genres2:
            if st.checkbox(genre, value=True):
                selected_genres.append(genre)
### APLICANDO FILTROS ###
df_filtered = df.copy()

if year_range and 'ReleaseYear' in df.columns:
    df_filtered = df_filtered[(df_filtered['ReleaseYear'] >= year_range[0]) & 
                            (df_filtered['ReleaseYear'] <= year_range[1])]

if selected_genres:
    df_filtered = df_filtered[df_filtered['Genre'].isin(selected_genres)]
else:
    st.warning("⚠️ Selecione pelo menos um gênero para visualizar os dados.")
    st.stop()


### CALCULOS ###
## CALCULO ESTATISTICO
roi_by_genre = df_filtered.groupby('Genre').agg({
    'ROI': ['mean', 'median'],
    'Title': 'count'
}).round(2)

roi_by_genre.columns = ['ROI_Médio_%', 'ROI_Mediana_%', 'Quantidade_Filmes']
roi_by_genre = roi_by_genre.sort_values('ROI_Médio_%', ascending=False)


# Métricas principais
st.header("📊 Visão Geral")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Filmes", len(df_filtered))
with col2:
    st.metric("ROI Médio Geral", f"{df_filtered['ROI'].mean():.2f}%")
with col3:
    st.metric("Gêneros Analisados", len(selected_genres))
with col4:
    st.metric("Melhor Gênero", roi_by_genre.index[0] if len(roi_by_genre) > 0 else "N/A")

# Gráficos
st.header("📈 Análise de ROI por Gênero")

# Criar gráficos lado a lado
col1, col2 = st.columns(2)

with col1:
    st.subheader("ROI Médio por Gênero")
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    
    sns.barplot(data=roi_by_genre.reset_index(), 
                x='ROI_Médio_%', 
                y='Genre', 
                palette='viridis',
                ax=ax1)
    ax1.set_xlabel('ROI Médio (%)', fontsize=12)
    ax1.set_ylabel('Gênero', fontsize=12)
    ax1.set_title('Retorno sobre Investimento Médio', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    st.pyplot(fig1)

with col2:
    st.subheader("Distribuição de ROI por Gênero")
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    
    sns.boxplot(data=df_filtered, 
                y='Genre', 
                x='ROI',
                palette='Set2',
                ax=ax2)
    ax2.set_xlabel('ROI (%)', fontsize=12)
    ax2.set_ylabel('Gênero', fontsize=12)
    ax2.set_title('Distribuição de ROI', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    st.pyplot(fig2)

# Tabelas de dados
st.header("📋 Estatísticas Detalhadas")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 3 Gêneros - Melhor ROI")
    st.dataframe(roi_by_genre.head(3), use_container_width=True)

with col2:
    st.subheader("📉 Bottom 3 Gêneros - Pior ROI")
    st.dataframe(roi_by_genre.tail(3), use_container_width=True)