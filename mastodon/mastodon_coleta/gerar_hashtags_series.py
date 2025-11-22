import pandas as pd

# Lê o arquivo único de séries
df = pd.read_csv("series.csv")

# Gera hashtags a partir do nome
df["hashtag"] = (
    df["Nome"]
    .astype(str)
    .str.replace(r"[^a-zA-Z0-9]", "", regex=True)
    .str.lower()
)

print("✅ Hashtags para séries geradas com sucesso!")
print(df[["Nome", "hashtag", "Tipo", "Temporada"]].head())

# Salva no PRÓPRIO arquivo original, agora com a nova coluna
df.to_csv("series.csv", index=False)

print("📂 O arquivo series.csv foi atualizado com a coluna 'hashtag'")