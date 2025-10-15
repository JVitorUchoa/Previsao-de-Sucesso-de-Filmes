import pandas as pd

# Tenta abrir o arquivo filmes.csv mostra só as 5 primeiras linha
try:
    df = pd.read_csv("filmes.csv")

    print("✅ Arquivo filmes.csv carregado com sucesso!")
    print("Primeiras linhas do arquivo:")
    print(df.head()) 
except FileNotFoundError:
    print("❌ Arquivo filmes.csv não encontrado. Verifique se está na pasta mastodon_coleta.")
except Exception as e:
    print(f"⚠️ Ocorreu um erro: {e}")
