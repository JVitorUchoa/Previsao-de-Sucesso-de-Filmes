import pandas as pd #importação do pandas para a manipulação dos dados
import json #importação da formatação JSON, formato em que os dados devem ser retornados

#arquivos de entrada e saída 
CSV_INPUT = "filmes_futuros_filtrados.csv" #nome do arquivo csv em que contém todos os filmes futuros
CSV_OUTPUT = "filmes_top100.csv" #nome do novo arquivo csv  gerado
JSON_OUTPUT = "filmes_top100.json" #nome do novo arquivo json  gerado

#carregar CSV 
df = pd.read_csv(CSV_INPUT, encoding="utf-8-sig") #lê o arquivo CSV de entrada para um DataFrame do Pandas

#ordenar por popularidade (decrescente) e manter apenas os 100 primeiros
df_top100 = df.sort_values(by="Popularidade", ascending=False).head(100).reset_index(drop=True)

print(f"✅ {len(df_top100)} filmes selecionados (os mais populares):") #imprimi uma mensagem de confirmação e imprimi as cinco primeiras linhas do dataframe
print(df_top100.head())

#salva o DataFrame do Top 100 no arquivo CSV de saída
df_top100.to_csv(CSV_OUTPUT, index=False, encoding="utf-8-sig")

#salva o DataFrame no formato JSON
df_top100.to_json(JSON_OUTPUT, orient="records", force_ascii=False, indent=4)

#imprime a mensagem final, confirmando a criação dos dois arquivos de saída
print(f"\nArquivos criados com sucesso:")
print(f" {CSV_OUTPUT}")
print(f" {JSON_OUTPUT}")
