#esse script mostra um gráfico das 15 obras mais populares usando a popularidade normalizada
import os #importa o módulo os responsável pelo acesso os arquivos e diretórios do projeto
import sys
import matplotlib.pyplot as plt #importa a biblioteca responsável por gerar os gráficos
import seaborn as sns  #importa a biblioteca que faz com que o gráfico fique visualmente bonito


sns.set(style="whitegrid")  #estilo agradável para gráficos

#menciona a aplicação em que pasta o código responsável pela normalização está
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../analise")))

from analise import unificar_dados, normalizar_dados, calcular_sucesso  #pega as funções do script de analise

#execução do main, programa principal
if __name__ == "__main__": 

    #parte responsávelpor carregar e processar os dados unificados
    df_unificado = unificar_dados()
    if df_unificado.empty:
        exit() #se não tiver dado, sai do script

    #normaliza os números pra ficarem todos na mesma escala (0 a 100)
    df_normalizado = normalizar_dados(df_unificado)
    
    df_final = calcular_sucesso(df_normalizado) #calcula a pontuação de sucesso, mesmo que o foco é só usar popularidade

    # filtra top 15 obras por popularidade normalizada
    df_top15_populares = df_final.nlargest(15, "popular_normalizacao")

    #gera gráfico de barras horizontal
    plt.figure(figsize=(12,8)) #tamanho do gráfico
    sns.barplot(
        x="popular_normalizacao",  # eixo X = popularidade normalizada
        y="titulo_x", # eixo Y = nome da obra
        data=df_top15_populares,
        palette="viridis"  #palheta de cor
    
    )
    plt.title("Top 15 Obras Mais Populares (Normalizado)", fontsize=16) #título do gráfico
    plt.xlabel("Popularidade Normalizada")  #nome do eixo X
    plt.ylabel("Título")   #nome do eixo Y
    plt.tight_layout()   #ajeita pra não cortar nada
    plt.show() #mostra o gráfico na tela
