import pandas as pd
import matplotlib.pyplot as plt

# Lê os resultados do Mastodon e combina com informações das séries
df_posts = pd.read_csv("mastodon_hashtags_series.csv")
df_info = pd.read_csv("series_hashtags.csv")

# Combina os dados
df = pd.merge(df_posts, df_info, on="hashtag", how="left")

print(" Prévia dos dados de séries:")
print(df.head())

df = df.sort_values("quantidade_posts", ascending=False)

print("\n Top 10 hashtags de séries com mais posts:")
print(df[["hashtag", "quantidade_posts", "Tipo", "Temporada"]].head(10))

# Gráfico geral
plt.figure(figsize=(12, 6))
df_top10 = df.head(10)
plt.bar(df_top10["hashtag"], df_top10["quantidade_posts"], color="purple")
plt.title("Top 10 Hashtags de Séries no Mastodon")
plt.xlabel("Hashtag")
plt.ylabel("Quantidade de Posts")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
