import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 1️ Ler o arquivo com as hashtags,limpa dados,gera nuvem,grafico 10 principais
df = pd.read_csv("mastodon_hashtags.csv")

df = df.dropna(subset=["hashtag"])  
df["hashtag"] = df["hashtag"].str.lower().str.strip() 
df = df.groupby("hashtag", as_index=False)["quantidade_posts"].sum() 
df = df.sort_values(by="quantidade_posts", ascending=False)

hashtags_dict = dict(zip(df["hashtag"], df["quantidade_posts"]))

wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(hashtags_dict)

plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title(" Nuvem de Hashtags mais usadas no Mastodon", fontsize=16)
plt.savefig("nuvem_hashtags.png", bbox_inches="tight")
plt.show()

top10 = df.head(10)
plt.figure(figsize=(8, 6))
plt.barh(top10["hashtag"], top10["quantidade_posts"], color="teal")
plt.xlabel("Quantidade de Posts")
plt.ylabel("Hashtag")
plt.title(" Top 10 Hashtags no Mastodon")
plt.gca().invert_yaxis()
plt.savefig("top10_hashtags.png", bbox_inches="tight")
plt.show()

print(" Nuvem e gráfico de barras gerados com sucesso!")
