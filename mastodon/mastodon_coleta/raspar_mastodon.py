import requests
import pandas as pd
from time import sleep

#nova alteração aqui:
# Lê as hashtags dos filmes e das séries
df_filmes = pd.read_csv("filmes_hashtags.csv")
df_series = pd.read_csv("series_hashtags.csv")

df = pd.concat([df_filmes, df_series], ignore_index=True)

hashtags = df["hashtag"].tolist()


resultados = []

print(" Coletando hashtags no Mastodon...")

for tag in hashtags:
    url = f"https://mastodon.social/api/v1/timelines/tag/{tag}?limit=5"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            posts = resp.json()
            resultados.append({
                "hashtag": tag,
                "quantidade_posts": len(posts)
            })
            print(f" #{tag}: {len(posts)} posts encontrados")
        else:
            print(f" Erro ao buscar #{tag}: {resp.status_code}")
    except Exception as e:
        print(f" Erro com #{tag}: {e}")
    sleep(2)  

df_result = pd.DataFrame(resultados)
df_result.to_csv("mastodon_hashtags.csv", index=False)
print("\nDados salvos em mastodon_hashtags.csv")
print(df_result.head())
