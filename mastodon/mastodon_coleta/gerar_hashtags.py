import pandas as pd

# Lê o arquivo de filmescria lista,mostra e salva com nome e hashtag
df = pd.read_csv("filmes.csv")

df["hashtag"] = df["Nome"].str.replace(r"[^a-zA-Z0-9]", "", regex=True).str.lower()

print("✅ Hashtags geradas com sucesso!")
print(df[["Nome", "hashtag"]].head())

df[["Nome", "hashtag"]].to_csv("filmes_hashtags.csv", index=False)
print("📂 Arquivo salvo como filmes_hashtags.csv")
