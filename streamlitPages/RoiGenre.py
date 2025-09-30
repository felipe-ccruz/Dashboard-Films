import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuração da página
st.set_page_config(
    page_title="Análise por Gênero - Cinema Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 20px;
    }
    h2, h3 {
        color: #2c3e50;
        padding-top: 20px;
    }
    .plot-container {
        background-color: black;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .insight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Função para carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv('movies_dataset.csv')
    df['ROI'] = ((df['Global_BoxOfficeUSD'] - df['BudgetUSD']) / df['BudgetUSD']) * 100
    return df

# Sidebar
st.sidebar.header("🎯 Filtros de Análise")
st.sidebar.markdown("---")

# Título principal
st.title("🎬 Análise de Gêneros Cinematográficos")
st.markdown("### Sucesso de Notas, Bilheteria e Retorno sobre Investimento")
st.markdown("---")

try:
    df = load_data()
    
    # Filtros na sidebar
    anos_disponiveis = sorted(df['ReleaseYear'].unique())
    ano_min, ano_max = st.sidebar.select_slider(
        "📅 Período de Análise",
        options=anos_disponiveis,
        value=(min(anos_disponiveis), max(anos_disponiveis))
    )
    
    generos_disponiveis = sorted(df['Genre'].unique())
    generos_selecionados = st.sidebar.multiselect(
        "🎭 Gêneros para Análise",
        options=generos_disponiveis,
        default=generos_disponiveis
    )
    
    roi_max = st.sidebar.slider(
        "📊 ROI Máximo para Visualização (%)",
        min_value=100,
        max_value=2000,
        value=1000,
        step=100,
        help="Filtra outliers extremos para melhor visualização"
    )
    
    # Aplicar filtros
    df_filtered = df[
        (df['ReleaseYear'] >= ano_min) & 
        (df['ReleaseYear'] <= ano_max) &
        (df['Genre'].isin(generos_selecionados))
    ]
    
    # ==================== SEÇÃO 1: NOTAS IMDB ====================
    st.markdown("## 🌟 Análise de Notas IMDb por Gênero")
    st.markdown("#### Qual gênero teve maior sucesso de notas?")
    
    # Calcular médias e medianas de notas
    rating_mean = df_filtered.groupby('Genre')['IMDbRating'].mean().sort_values(ascending=False)
    rating_median = df_filtered.groupby('Genre')['IMDbRating'].median().sort_values(ascending=False)
    
    # Métricas de notas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🥇 Melhor Nota Média",
            f"{rating_mean.iloc[0]:.2f}",
            delta=rating_mean.index[0]
        )
    
    with col2:
        st.metric(
            "🥈 Melhor Nota Mediana",
            f"{rating_median.iloc[0]:.2f}",
            delta=rating_median.index[0]
        )
    
    with col3:
        st.metric(
            "📊 Nota Média Geral",
            f"{df_filtered['IMDbRating'].mean():.2f}"
        )
    
    with col4:
        st.metric(
            "🎯 Mediana Geral",
            f"{df_filtered['IMDbRating'].median():.2f}"
        )
    
    st.markdown("---")
    
    # Gráficos de Notas
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        st.markdown("#### 📊 Nota Média IMDb por Gênero")
        
        fig1 = go.Figure(go.Bar(
            x=rating_mean.values,
            y=rating_mean.index,
            orientation='h',
            marker=dict(
                color=rating_mean.values,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Nota")
            ),
            text=[f"{val:.2f}" for val in rating_mean.values],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Nota Média: %{x:.2f}<extra></extra>'
        ))
        
        fig1.update_layout(
            height=500,
            xaxis_title="Nota Média IMDb",
            yaxis_title="",
            margin=dict(l=0, r=50, t=10, b=0),
            xaxis=dict(range=[5.5, rating_mean.max() + 0.3])
        )
        
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        st.markdown("#### 📈 Nota Mediana IMDb por Gênero")
        
        fig2 = go.Figure(go.Bar(
            x=rating_median.values,
            y=rating_median.index,
            orientation='h',
            marker=dict(
                color=rating_median.values,
                colorscale='Plasma',
                showscale=True,
                colorbar=dict(title="Nota")
            ),
            text=[f"{val:.2f}" for val in rating_median.values],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Nota Mediana: %{x:.2f}<extra></extra>'
        ))
        
        fig2.update_layout(
            height=500,
            xaxis_title="Nota Mediana IMDb",
            yaxis_title="",
            margin=dict(l=0, r=50, t=10, b=0),
            xaxis=dict(range=[5.5, rating_median.max() + 0.3])
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabela comparativa de notas
    st.markdown("#### 📋 Top 5 Gêneros - Comparação de Notas")
    comparison_df = pd.DataFrame({
        'Gênero': rating_mean.head().index,
        'Nota Média': rating_mean.head().values,
        'Nota Mediana': [rating_median[genre] for genre in rating_mean.head().index]
    }).round(2)
    
    st.dataframe(
        comparison_df.style.background_gradient(subset=['Nota Média', 'Nota Mediana'], cmap='YlGn'),
        use_container_width=True,
        hide_index=True
    )
    
    # ==================== SEÇÃO 2: BILHETERIA ====================
    st.markdown("---")
    st.markdown("## 💰 Análise de Bilheteria por Gênero")
    st.markdown("#### Qual gênero teve maior mediana de bilheteria?")
    
    # Calcular médias e medianas de bilheteria
    boxoffice_mean = df_filtered.groupby('Genre')['Global_BoxOfficeUSD'].mean().sort_values(ascending=False)
    boxoffice_median = df_filtered.groupby('Genre')['Global_BoxOfficeUSD'].median().sort_values(ascending=False)
    
    # Métricas de bilheteria
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🎯 Maior Mediana",
            f"${boxoffice_median.iloc[0]/1e6:.1f}M",
            delta=boxoffice_median.index[0]
        )
    
    with col2:
        st.metric(
            "💎 Maior Média",
            f"${boxoffice_mean.iloc[0]/1e6:.1f}M",
            delta=boxoffice_mean.index[0]
        )
    
    with col3:
        st.metric(
            "📊 Bilheteria Média Geral",
            f"${df_filtered['Global_BoxOfficeUSD'].mean()/1e6:.1f}M"
        )
    
    with col4:
        st.metric(
            "🎬 Total de Filmes",
            f"{len(df_filtered):,}"
        )
    
    st.markdown("---")
    
    # Gráficos de Bilheteria
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        st.markdown("#### 💵 Bilheteria Mediana por Gênero")
        
        fig3 = go.Figure(go.Bar(
            x=boxoffice_median.values / 1e6,
            y=boxoffice_median.index,
            orientation='h',
            marker=dict(
                color=boxoffice_median.values,
                colorscale='Blues',
                showscale=True,
                colorbar=dict(title="USD")
            ),
            text=[f"${val/1e6:.1f}M" for val in boxoffice_median.values],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Bilheteria Mediana: $%{x:.1f}M<extra></extra>'
        ))
        
        fig3.update_layout(
            height=500,
            xaxis_title="Bilheteria Mediana (Milhões USD)",
            yaxis_title="",
            margin=dict(l=0, r=50, t=10, b=0)
        )
        
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        st.markdown("#### 💰 Bilheteria Média por Gênero")
        
        fig4 = go.Figure(go.Bar(
            x=boxoffice_mean.values / 1e6,
            y=boxoffice_mean.index,
            orientation='h',
            marker=dict(
                color=boxoffice_mean.values,
                colorscale='Greens',
                showscale=True,
                colorbar=dict(title="USD")
            ),
            text=[f"${val/1e6:.1f}M" for val in boxoffice_mean.values],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Bilheteria Média: $%{x:.1f}M<extra></extra>'
        ))
        
        fig4.update_layout(
            height=500,
            xaxis_title="Bilheteria Média (Milhões USD)",
            yaxis_title="",
            margin=dict(l=0, r=50, t=10, b=0)
        )
        
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabela comparativa de bilheteria
    st.markdown("#### 📋 Top 5 Gêneros - Comparação de Bilheteria")
    boxoffice_comparison = pd.DataFrame({
        'Gênero': boxoffice_median.head().index,
        'Mediana (M USD)': (boxoffice_median.head().values / 1e6).round(2),
        'Média (M USD)': [(boxoffice_mean[genre] / 1e6) for genre in boxoffice_median.head().index]
    }).round(2)
    
    st.dataframe(
        boxoffice_comparison.style.background_gradient(subset=['Mediana (M USD)', 'Média (M USD)'], cmap='BuGn'),
        use_container_width=True,
        hide_index=True
    )
    
    # ==================== SEÇÃO 3: ROI ====================
    st.markdown("---")
    st.markdown("## 📈 Análise de ROI (Return on Investment)")
    st.markdown("#### Retorno sobre Investimento por Gênero")
    
    # Calcular ROI por gênero
    roi_by_genre = df_filtered.groupby('Genre').agg({
        'ROI': ['mean', 'median'],
        'Title': 'count'
    }).round(2)
    roi_by_genre.columns = ['ROI_Médio_%', 'ROI_Mediana_%', 'Quantidade_Filmes']
    roi_by_genre = roi_by_genre.sort_values('ROI_Médio_%', ascending=False)
    
    # Métricas de ROI
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🚀 Melhor ROI Médio",
            f"{roi_by_genre.iloc[0]['ROI_Médio_%']:.1f}%",
            delta=roi_by_genre.index[0]
        )
    
    with col2:
        st.metric(
            "📊 ROI Médio Geral",
            f"{df_filtered['ROI'].mean():.1f}%"
        )
    
    with col3:
        lucrativos = (df_filtered['ROI'] > 0).sum()
        pct = (lucrativos / len(df_filtered)) * 100
        st.metric(
            "✅ Filmes Lucrativos",
            f"{pct:.1f}%",
            delta=f"{lucrativos} filmes"
        )
    
    with col4:
        st.metric(
            "⚠️ Pior ROI Médio",
            f"{roi_by_genre.iloc[-1]['ROI_Médio_%']:.1f}%",
            delta=roi_by_genre.index[-1],
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # Gráficos de ROI
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        st.markdown("#### 📊 ROI Médio por Gênero")
        
        fig5 = go.Figure(go.Bar(
            x=roi_by_genre.reset_index()['ROI_Médio_%'],
            y=roi_by_genre.reset_index()['Genre'],
            orientation='h',
            marker=dict(
                color=roi_by_genre.reset_index()['ROI_Médio_%'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="ROI %"),
                cmid=0
            ),
            text=[f"{val:.1f}%" for val in roi_by_genre.reset_index()['ROI_Médio_%']],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>ROI Médio: %{x:.1f}%<extra></extra>'
        ))
        
        fig5.update_layout(
            height=500,
            xaxis_title="ROI Médio (%)",
            yaxis_title="",
            margin=dict(l=0, r=50, t=10, b=0)
        )
        
        st.plotly_chart(fig5, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        st.markdown("#### 📦 Distribuição de ROI por Gênero")
        
        df_roi_filtered = df_filtered[df_filtered['ROI'] < roi_max]
        
        fig6 = go.Figure()
        
        for genre in df_roi_filtered['Genre'].unique():
            genre_data = df_roi_filtered[df_roi_filtered['Genre'] == genre]['ROI']
            fig6.add_trace(go.Box(
                x=genre_data,
                y=[genre] * len(genre_data),
                name=genre,
                orientation='h',
                showlegend=False,
                marker=dict(opacity=0.7)
            ))
        
        fig6.update_layout(
            height=500,
            xaxis_title="ROI (%)",
            yaxis_title="",
            margin=dict(l=0, r=20, t=10, b=0),
            hovermode='closest'
        )
        
        st.plotly_chart(fig6, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabelas de ROI
    st.markdown("#### 🏆 Rankings de ROI")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🥇 Top 5 Gêneros - Melhor ROI")
        top5_roi = roi_by_genre.head()[['ROI_Médio_%', 'ROI_Mediana_%', 'Quantidade_Filmes']]
        st.dataframe(
            top5_roi.style.background_gradient(subset=['ROI_Médio_%'], cmap='Greens'),
            use_container_width=True
        )
    
    with col2:
        st.markdown("##### 📉 Bottom 5 Gêneros - Pior ROI")
        bottom5_roi = roi_by_genre.tail()[['ROI_Médio_%', 'ROI_Mediana_%', 'Quantidade_Filmes']]
        st.dataframe(
            bottom5_roi.style.background_gradient(subset=['ROI_Médio_%'], cmap='Reds_r'),
            use_container_width=True
        )
    
    # ==================== INSIGHTS FINAIS ====================
    st.markdown("---")
    st.markdown("## 💡 Principais Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="insight-box">
            <h4>🌟 Qualidade vs Quantidade</h4>
            <p><b>{rating_mean.index[0]}</b> lidera em nota média (<b>{rating_mean.iloc[0]:.2f}</b>), 
            enquanto <b>{boxoffice_median.index[0]}</b> tem a maior mediana de bilheteria 
            (<b>${boxoffice_median.iloc[0]/1e6:.1f}M</b>).</p>
            <p><i>💡 Filmes de {boxoffice_median.index[0]} podem ser uma escolha mais segura para investimento.</i></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="insight-box">
            <h4>📈 Média vs Mediana</h4>
            <p><b>{boxoffice_mean.index[0]}</b> tem a maior média de bilheteria (<b>${boxoffice_mean.iloc[0]/1e6:.1f}M</b>), 
            sugerindo potencial para grandes sucessos, apesar de maior variabilidade.</p>
            <p><i>💡 Alto risco, alto retorno - ideal para investidores arrojados.</i></p>
        </div>
        """, unsafe_allow_html=True)

except FileNotFoundError:
    st.error("⚠️ Arquivo de dados não encontrado. Por favor, carregue o dataset.")
    st.info("💡 Dica: Atualize o caminho do arquivo na função `load_data()`")
except Exception as e:
    st.error(f"❌ Erro ao processar dados: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 20px;'>
    <p>📊 Cinema Analytics Dashboard | Página 1 de 6</p>
</div>
""", unsafe_allow_html=True)