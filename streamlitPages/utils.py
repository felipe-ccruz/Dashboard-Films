"""
Arquivo de utilidades para compartilhar dados e funções entre páginas
"""

import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    """
    Carrega e processa os dados dos filmes.
    O decorator @st.cache_data garante que os dados sejam carregados apenas uma vez.
    """
    try:
        df = pd.read_csv('movies_dataset.csv')
        
        # Cálculo do ROI
        if 'ROI' not in df.columns:
            df['ROI'] = ((df['Global_BoxOfficeUSD'] - df['BudgetUSD']) / df['BudgetUSD']) * 100
        
        # Garantir que ReleaseYear existe
        if 'ReleaseYear' not in df.columns:
            if 'ReleaseDate' in df.columns:
                df['ReleaseYear'] = pd.to_datetime(df['ReleaseDate'], errors='coerce').dt.year
            elif 'Year' in df.columns:
                df['ReleaseYear'] = df['Year']
        
        return df
    
    except FileNotFoundError:
        st.error("❌ Arquivo 'movies_dataset.csv' não encontrado!")
        st.stop()
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        st.stop()

# def create_sidebar():
#     """
#     Cria a sidebar de navegação padrão para todas as páginas
#     """
#     st.sidebar.header("📖 Navegação")
    
#     if st.sidebar.button("🏠 Home", use_container_width=True):
#         st.switch_page("streamlitPages/Home.py")
    
#     if st.sidebar.button("📊 Análise de ROI", use_container_width=True):
#         st.switch_page("streamlitPages/pages/roiGenre.py")
    
#     if st.sidebar.button("📈 Example 1", use_container_width=True):
#         st.switch_page("streamlitPages/pages/example1.py")
    
#     if st.sidebar.button("📉 Example 2", use_container_width=True):
#         st.switch_page("streamlitPages/pages/example2.py")
    
#     if st.sidebar.button("🎯 Example 3", use_container_width=True):
#         st.switch_page("streamlitPages/pages/example3.py")