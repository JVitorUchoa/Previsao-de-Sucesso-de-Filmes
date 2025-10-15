import pandas as pd

# Lê o arquivo de filmes,e mostra 
df = pd.read_csv("filmes.csv")

print(" Arquivo carregado com sucesso!\n")

print(" Primeiras linhas do dataset:")
print(df.head(), "\n")

print(" Colunas do dataset:")
print(df.columns, "\n")

print("ℹ Informações gerais:")
print(df.info(), "\n")

print(" Estatísticas numéricas:")
print(df.describe(), "\n")

print(f" Total de linhas: {df.shape[0]}")
print(f" Total de colunas: {df.shape[1]}")
