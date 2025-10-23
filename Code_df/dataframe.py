#código responsável pela a leitura e carregamento de dados dentro da estrutura Dataframe do pandas
import pandas as pd
import json

#carregando CSV em DataFrame 
df_csv = pd.read_csv("filmes_futuros_filtrados.csv")#utiliza a função read_csv do pandas para carregar o arquivo csv diretamente em um DataFrame chamado df_csv
print("CSV carregado:") #imprimi a confirmação do carregamento do dataframe
print(df_csv.head()) #exibe as primeiras cinco linhas do DataFrame do csv

#carregando JSON em DataFrame
with open("filmes_futuros_filtrados.json", "r", encoding="utf-8") as f:
    dados_json = json.load(f) #utiliza o formato json para a leitura e converter em dicionário

df_json = pd.DataFrame(dados_json) #exibe as primeiras 5 linhas do DataFrame
print("\nJSON carregado:") #imprimi a confirmação do carregamento do dataframe
print(df_json.head())  #exibe as primeiras cinco linhas do DataFrame do json
