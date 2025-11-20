import pandas as pd

# Lê o arquivo único de séries
df = pd.read_csv("series.csv")

# Gera hashtags a partir do nome
df["hashtag"] = df["Nome"].str.replace(r"[^a-zA-Z0-9]", "", regex=True).str.lower()

print("✅ Hashtags para séries geradas com sucesso!")
print(df[["Nome", "hashtag", "Tipo", "Temporada"]].head())

# Salva o mapeamento
df[["Nome", "hashtag", "Tipo", "Temporada"]].to_csv("series_hashtags.csv", index=False)
print("📂 Arquivo salvo como series_hashtags.csv")