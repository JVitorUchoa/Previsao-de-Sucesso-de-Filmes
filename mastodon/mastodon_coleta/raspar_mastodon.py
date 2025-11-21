import requests
import pandas as pd
from time import sleep

# Lê as hashtags dos filmes,cria lista de hashtags,cria data frame e salva os resultados
df = pd.read_csv("filmes_hashtags.csv")

hashtags = df["hashtag"].tolist()[:30]

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
