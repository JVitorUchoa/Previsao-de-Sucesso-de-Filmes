import pandas as pd
from analise import unificar_dados, normalizarlizacao, calcular_sucesso

print("\n Iniciando Análise dos Filmes e Séries...")   

df_unificado = unificar_dados()
if df_unificado is None:
    print("Execução interrompida.")

df_normalizado = normalizarlizacao(df_unificado)
df_final = calcular_sucesso(df_normalizado)

# Lista os 15 filmes/séries de sucesso
print("\n Top 15 Obras de Sucesso: ")
df_top15 = df_final.sort_values("sucesso_pontos", ascending=False).head(15)
colunas_exibicao = ["titulo"]
print(df_top15[colunas_exibicao].to_string(index=False))

# Filtrando apenas filmes
filme = df_final["tipo_obra"] == "filme"
df_filme = df_final[filme]

# Filtrando apenas séries
serie = df_final["tipo_obra"] == "serie"
df_serie = df_final[serie]

print("\n Top 10 Filmes de Sucesso: ")
df_top10_filmes = df_filme.sort_values("sucesso_pontos", ascending=False).head(10)
print(df_top10_filmes[colunas_exibicao].to_string(index=False))

print("\n  Top 10 Séries de Sucesso: ")
df_top10_serie = df_serie.sort_values("sucesso_pontos", ascending=False).head(10)
print(df_top10_serie[colunas_exibicao].to_string(index=False))