#script responsável por gerar um dashboard que mostra os resultados encontrados a partir da normalização
import streamlit as st #importando a biblioteca responsável por gerar a página web
import os #importa o módulo os responsável pelo acesso aos arquivos e diretórios do projeto
import sys #importando o módulo sys responsável por permitir usar funções e variáveis de outro script que está em uma pasta diferente

#menciona a aplicação em que pasta o código responsável pela normalização está
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../analise")))

from analise.analise import unificar_dados, normalizar_dados, calcular_sucesso  #pega as funções do script de analise
from buscar_poster import buscar_poster # função que busca o poster do filme e série pelo nome no código buscar_poster

# configuração básica da página do Streamlit
st.set_page_config(page_title="Top Filmes e Séries", layout="wide") 

# título do dashboard
st.title("🎬 Dashboard Visual – Top 10 Filmes e Séries")
st.write("Baseado em: **sucesso_pontos**")

#pega e junta todos os dados das fontes
df = unificar_dados()

#parte que informa uma condição de parada caso não encontre os dados
if df.empty:
    st.error("Nenhum dado foi encontrado.")
    st.stop()

df = normalizar_dados(df)  #normaliza os números pra ficarem na mesma escala
df = calcular_sucesso(df) #leva em consideração a função calcular_sucesso para gerar o dashboard

# deixar tudo minúsculo pra não dar erro
df["tipo_obra_x"] = df["tipo_obra_x"].str.lower() #utiliza esta coluna no dashboard


#filtra apenas a coluna equivalente a filme
df_filmes = df[df["tipo_obra_x"] == "filme"]
top10_filmes = df_filmes.sort_values(by="sucesso_pontos", ascending=False).head(10) #ordena pelos mais bem sucedidos e mostra só os 10 primeiros

#filtra apenas a coluna equivalente a serie
df_series = df[df["tipo_obra_x"] == "serie"]
top10_series = df_series.sort_values(by="sucesso_pontos", ascending=False).head(10) #ordena pelos mais bem sucedidos e mostra só os 10 primeiros


# título da seção
st.header("🍿 Top 10 Filmes")

#gera o gráfico de filmes a partir da ornenação anterior, pega como referência o título da obra
st.bar_chart(
    top10_filmes.set_index("titulo_x")["sucesso_pontos"]
)

colunas = st.columns(5) # cria 5 colunas pra organizar os posteres na tela

# percorre os 10 filmes e exibe cada um com seu poster
for i, row in enumerate(top10_filmes.itertuples()):
    with colunas[i % 5]:
        poster = buscar_poster(row.titulo_x)  #busca a imagem do poster pelo título

        if poster:
            st.image(poster, use_container_width=True) #condição que se satisfeita, mostrará o poster

        st.caption(f"{row.titulo_x} | 🎯 {round(row.sucesso_pontos,2)}")  #mostra o nome e a pontuação embaixo da imagem


# título da seção
st.header("📺 Top 10 Séries")

#gera o gráfico de séries a partir da ornenação anterior, pega como referência o título da obra
st.bar_chart( 
    top10_series.set_index("titulo_x")["sucesso_pontos"]
)

#outra coluna para as séries, definindo cinco colunas
colunas2 = st.columns(5)

# percorre as 10 series e exibe cada um com seu poster
for i, row in enumerate(top10_series.itertuples()):
    with colunas2[i % 5]:
        poster = buscar_poster(row.titulo_x) #busca a imagem do poster pelo título

        if poster:
            st.image(poster, use_container_width=True) #condição que se satisfeita, mostrará o poster

        st.caption(f"{row.titulo_x} | 🎯 {round(row.sucesso_pontos,2)}")  #mostra o nome e a pontuação embaixo da imagem


