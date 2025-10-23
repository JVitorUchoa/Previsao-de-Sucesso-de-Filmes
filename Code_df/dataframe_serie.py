#código responsável pela a leitura e carregamento de dados das séries dentro da estrutura Dataframe do pandas
import pandas as pd
import json

#carregando CSV em DataFrame
df_series_csv = pd.read_csv("series_futuras_filtradas.csv", encoding="utf-8-sig")#utiliza a função read_csv do pandas para carregar o arquivo csv diretamente em um DataFrame chamado df_series_csv
print("CSV carregado:")#imprimi a confirmação do carregamento do dataframe
print(df_series_csv.head())#exibe as primeiras cinco linhas do DataFrame do csv

#carregando JSON em DataFrame 
with open("series_futuras_filtradas.json", "r", encoding="utf-8") as f:
    dados_json = json.load(f) #utiliza o formato json para a leitura e converter em dicionário

df_series_json = pd.DataFrame(dados_json) #exibe as primeiras cinco linhas do DataFrame
print("\nJSON carregado:") #imprimi a confirmação do carregamento do dataframe
print(df_series_json.head()) #exibe as primeiras cinco linhas do DataFrame do json
