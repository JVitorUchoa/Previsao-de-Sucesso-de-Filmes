
import os #importa o módulo os responsável pelo acesso os arquivos e diretórios do projeto
import sys
import matplotlib.pyplot as plt #importa a biblioteca responsável por gerar os gráficos
import seaborn as sns #importa a biblioteca que faz com que o gráfico fique visualmente bonito

sns.set(style="whitegrid")  # estilo agradável para gráficos

# menciona a aplicação em que pasta o código responsável pela normalização está
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../analise")))

from analise import unificar_dados, normalizar_dados, calcular_sucesso  # pega as funções do script de analise

# execução do main, programa principal
if __name__ == "__main__":

    # parte responsávelpor carregar e processar os dados unificados
    df_unificado = unificar_dados()
    if df_unificado.empty:
        exit()  # sai se não houver dados

    df_normalizado = normalizar_dados(df_unificado)
    df_final = calcular_sucesso(df_normalizado)

    # filtra apenas filmes e exibe Top 10 por sucesso
    df_top10_filmes = df_final[df_final["tipo_obra_x"] == "filme"].nlargest(10, "sucesso_pontos")

    # gera gráfico de barras horizontal
    plt.figure(figsize=(10,6)) # tamanho do gráfico
    sns.barplot(
        x="sucesso_pontos",   # eixo X = pontos de sucesso
        y="titulo_x",        # eixo Y = nome do filme
        data=df_top10_filmes,
        palette="magma" #palheta de cor
    )
    plt.title("Top 10 Filmes de Sucesso", fontsize=16)  # título do gráfico
    plt.xlabel("Pontuação de Sucesso") # nome do eixo X
    plt.ylabel("Título do Filme") # nome do eixo Y
    plt.tight_layout() # ajeita pra não cortar nada
    plt.show() # mostra o gráfico na tela
