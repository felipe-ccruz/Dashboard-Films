import streamlit as st
from utils import load_data

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Filmes",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# # Criar sidebar
# create_sidebar()

# Carregar dados
df = load_data()

### HOME PAGE ###
st.title("🎬 Bem-vindo ao Dashboard de Análise Cinematográfica")

st.markdown("""
### Descubra o fascinante mundo dos filmes através dos dados!

Os filmes são uma das formas de arte e entretenimento mais poderosas da nossa era. 
Eles não apenas contam histórias que nos emocionam, mas também representam um 
mercado bilionário com investimentos massivos e retornos extraordinários.

Este dashboard foi criado para você explorar e entender os aspectos financeiros 
por trás da indústria cinematográfica. Aqui, você poderá analisar como diferentes 
gêneros de filmes performam, quais trazem os melhores retornos sobre investimento (ROI), 
e muito mais!

**Nosso objetivo** é tornar os dados do cinema acessíveis e compreensíveis, permitindo 
que você descubra padrões interessantes e insights valiosos sobre o que torna um filme 
financeiramente bem-sucedido.
""")

st.markdown("---")

# Informações rápidas sobre o dataset
st.header("📊 Visão Geral dos Dados")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🎬 Total de Filmes",
        value=f"{len(df):,}"
    )

with col2:
    st.metric(
        label="🎭 Gêneros Únicos",
        value=df['Genre'].nunique()
    )

with col3:
    receita_total = df['Global_BoxOfficeUSD'].sum() / 1e9
    st.metric(
        label="💰 Bilheteria Total",
        value=f"${receita_total:.1f}B"
    )

with col4:
    st.metric(
        label="📊 ROI Médio",
        value=f"{df['ROI'].mean():.1f}%"
    )

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🎬 Dashboard de Análise Cinematográfica | Desenvolvido com Streamlit</p>
</div>
""", unsafe_allow_html=True)