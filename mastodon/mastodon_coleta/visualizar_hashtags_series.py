import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Ler os dados combinados
df_posts = pd.read_csv("mastodon_hashtags_series.csv")
df_info = pd.read_csv("series_hashtags.csv")
df = pd.merge(df_posts, df_info, on="hashtag", how="left")

df = df.dropna(subset=["hashtag"])  
df["hashtag"] = df["hashtag"].str.lower().str.strip() 
df = df.sort_values(by="quantidade_posts", ascending=False)

# Nuvem de palavras geral
hashtags_dict = dict(zip(df["hashtag"], df["quantidade_posts"]))
wordcloud = WordCloud(width=800, height=400, background_color="white", 
                     colormap="Purples").generate_from_frequencies(hashtags_dict)

plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Nuvem de Hashtags de Séries no Mastodon", fontsize=16)
plt.savefig("nuvem_hashtags_series.png", bbox_inches="tight")
plt.show()

# Top 10 hashtags
top10 = df.head(10)
plt.figure(figsize=(10, 6))
plt.barh(top10["hashtag"], top10["quantidade_posts"], color="purple")
plt.xlabel("Quantidade de Posts")
plt.ylabel("Hashtag")
plt.title("Top 10 Hashtags de Séries no Mastodon")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("top10_hashtags_series.png", bbox_inches="tight")
plt.show()


print(" Visualizações para séries geradas com sucesso!")