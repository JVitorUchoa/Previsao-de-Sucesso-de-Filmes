import pandas as pd
import matplotlib.pyplot as plt

# aqui ta lendo os resultados do Mastodon,mostra as 10 mais e cria um grafico simples
df = pd.read_csv("mastodon_hashtags.csv")

print("📊 Prévia dos dados:")
print(df.head())

df = df.sort_values("quantidade_posts", ascending=False)

print("\n🔥 Top 10 hashtags com mais posts:")
print(df.head(10))

plt.figure(figsize=(10,6))
df = df.dropna(subset=["hashtag"])

plt.bar(df["hashtag"].head(10), df["quantidade_posts"].head(10), color="teal")
plt.title("Top 10 Hashtags de Filmes no Mastodon")
plt.xlabel("Hashtag")
plt.ylabel("Quantidade de Posts")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
