import os #importa o módulo os responsável pelo acesso os arquivos e diretórios do projeto
import sys
import matplotlib.pyplot as plt #importa a biblioteca responsável por gerar os gráficos
import seaborn as sns #importa a biblioteca que faz com que o gráfico fique visualmente bonito

sns.set(style="whitegrid")  # estilo agradável para gráficos

#menciona a aplicação em que pasta o código responsável pela normalização está
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../analise")))

from analise import unificar_dados, normalizar_dados, calcular_sucesso #pega as funções do script de analise

#execução do main, programa principal
if __name__ == "__main__":

   #parte responsávelpor carregar e processar os dados unificados
    df_unificado = unificar_dados()
    if df_unificado.empty:
        exit()  # se não tiver dado, sai do script

    #normaliza os números pra ficarem na mesma escala
    df_normalizado = normalizar_dados(df_unificado)

    #calcula a pontuação de sucesso das obras
    df_final = calcular_sucesso(df_normalizado)

    # filtra apenas series e exibe Top 10 por sucesso
    df_top10_series = df_final[df_final["tipo_obra_x"] == "serie"].nlargest(10, "sucesso_pontos")

    #gera gráfico de barras horizontal
    plt.figure(figsize=(10,6))  # tamanho do gráfico
    sns.barplot(
        x="sucesso_pontos",  # eixo X = pontuação de sucesso
        y="titulo_x",  # eixo Y = nome da série
        data=df_top10_series,
        palette="coolwarm"  #palheta de cor
    )
    plt.title("Top 10 Séries de Sucesso", fontsize=16)  # título do gráfico
    plt.xlabel("Pontuação de Sucesso")  # nome do eixo X
    plt.ylabel("Título da Série")  # nome do eixo Y
    plt.tight_layout()  #ajeita pra não cortar nada
    plt.show()  #mostra o gráfico na tela
