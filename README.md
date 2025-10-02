# 🎬 Dashboard Interativo: Análise da Indústria Cinematográfica

**Integrantes:** Felipe Cruz, Gabriel Mattos
**Turma:** CC6NA

## 1\. Introdução e Objetivo

Este projeto foi desenvolvido como parte da avaliação da disciplina de Estatística, com o objetivo de aplicar técnicas de análise de dados para explorar o cenário mundial da indústria cinematográfica. Utilizando um conjunto de dados abrangente, buscamos entender as tendências de produção, os investimentos (orçamentos) e os retornos financeiros (bilheteria) dos filmes ao longo dos anos e entre diferentes mercados.

O resultado final é um **dashboard interativo**, construído com Streamlit, que transforma dados brutos em insights visuais e acessíveis, permitindo que qualquer usuário explore e compreenda as dinâmicas complexas do cinema global.

## 2\. O Conjunto de Dados

Para realizar nossa análise, selecionamos um dataset público da plataforma Kaggle, que se mostrou ideal pela riqueza de suas variáveis financeiras, temporais e de avaliação.

  * **Fonte:** [Movie Dataset for Analytics and Visualization](https://www.kaggle.com/datasets/mjshubham21/movie-dataset-for-analytics-and-visualization)
  * **Justificativa da Escolha:** O dataset foi escolhido por conter informações detalhadas sobre orçamento, bilheteria (global e doméstica), gênero, diretores, atores e avaliações (IMDb, Rotten Tomatoes). Essa variedade nos permitiu criar um dashboard multifacetado, com análises que vão desde o retorno sobre investimento (ROI) por gênero até a performance comparativa entre países.

## 3\. Etapas do Projeto

Nosso fluxo de trabalho foi dividido em quatro etapas principais, desde a obtenção dos dados até a entrega da aplicação final.

#### Etapa 1: Exploração e Limpeza dos Dados

Após o download, a primeira etapa consistiu em uma análise exploratória inicial para visualizar os dados e verificar a existência de possíveis erros, outliers e valores nulos. Como se tratava de um dataset curado para fins de análise (dados fictícios), ele apresentava uma alta qualidade, com poucos problemas que demandassem tratamentos complexos.

Todo o processo de verificação e as poucas limpezas realizadas foram documentados no notebook:

  * 📄 **`Tratamento-e-Limpeza.ipynb`**

#### Etapa 2: Análise e Geração de Insights

Com os dados limpos e preparados, partimos para a análise aprofundada. Nesta fase, utilizamos a biblioteca Pandas para realizar agregações, calcular novas métricas (como ROI e Década) e criar as lógicas de negócio que serviriam de base para cada página do nosso dashboard.

As principais análises e os "rascunhos" dos gráficos foram desenvolvidos no notebook:

  * 📄 **`analise.ipynb`**

#### Etapa 3: Estruturação e Desenvolvimento do Dashboard

Com os insights em mãos, o próximo passo foi estruturar o projeto do dashboard em Streamlit. Optamos por uma arquitetura multi-página para organizar as diferentes análises de forma lógica e intuitiva, facilitando a navegação do usuário.

A estrutura de pastas do projeto foi organizada da seguinte forma:

```plaintext
streamlitPages/
│
├── 📄 Home.py                 # Página inicial de apresentação do dashboard
├── 📄 utils.py                 # Funções auxiliares (ex: carregamento de dados)
│
└── 📁 pages/                   # Diretório para as sub-páginas do dashboard
    ├── 📄 1_roi_por_genero.py
    ├── 📄 2_tendencias_temporais.py
    ├── 📄 3_analise_correlacao.py
    ├── 📄 4_performance_talentos.py
    └── 📄 5_analise_paises.py
```

  * **`Home.py`**: Serve como a porta de entrada, apresentando o projeto.
  * **`utils.py`**: Centraliza funções úteis, como o carregamento dos dados, para evitar repetição de código.
  * **`pages/`**: O diretório especial do Streamlit onde cada arquivo `.py` se torna automaticamente uma nova página na barra de navegação.

## 4\. Ferramentas Utilizadas

  * **Linguagem:** Python
  * **Análise de Dados:** Pandas, NumPy
  * **Visualização de Dados:** Matplotlib, Seaborn
  * **Dashboard Interativo:** Streamlit

## 5\. Como Executar o Projeto

Para explorar o dashboard em sua máquina local, siga os passos abaixo:

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/felipe-ccruz/Dashboard-Films.git
    ```

2.  **Crie um ambiente virtual (recomendado):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação Streamlit:**

    ```bash
    streamlit run .\streamlitPages\Home.py
    ```

-----