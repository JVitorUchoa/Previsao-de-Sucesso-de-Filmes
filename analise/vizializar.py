import pandas as pd
from analise import unificar_dados, normalizar_dados, calcular_sucesso

print("\n Iniciando Análise dos Filmes e Séries... \n")

# Unificação dos dados 
df_unificado = unificar_dados()
if df_unificado.empty:
    print("Nenhum dado foi carregado.")
    exit()

# Normalização (padronizão)
df_normalizado = normalizar_dados(df_unificado)

# Cálculo de sucesso 
df_final = calcular_sucesso(df_normalizado)

# Lista dos 15 filmes/séries de sucesso
print("\n Top 15 Obras de Sucesso:")
df_top15 = df_final.sort_values("sucesso_pontos", ascending=False).head(15)
colunas_exibicao = ["titulo_x", "sucesso_classificar", "sucesso_pontos"]
print(df_top15[colunas_exibicao].to_string(index=False))

# Top 10 Filmes de sucesso
print("\n Top 10 Filmes de Sucesso:")
df_filmes = df_final[df_final["tipo_obra_x"] == "filme"]
df_top10_filmes = df_filmes.sort_values("sucesso_pontos", ascending=False).head(10)
print(df_top10_filmes[colunas_exibicao].to_string(index=False))

# Top 10 Séries de sucesso
print("\n Top 10 Séries de Sucesso:")
df_series = df_final[df_final["tipo_obra_x"] == "serie"]
df_top10_series = df_series.sort_values("sucesso_pontos", ascending=False).head(10)
print(df_top10_series[colunas_exibicao].to_string(index=False))
