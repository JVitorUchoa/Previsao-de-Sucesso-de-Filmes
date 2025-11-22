import requests
import pandas as pd
from time import sleep

# Lê as hashtags dos filmes e das séries
df_filmes = pd.read_csv("filmes_hashtags.csv")
df_series = pd.read_csv("series_hashtags.csv")

df = pd.concat([df_filmes, df_series], ignore_index=True)

# Limpa as hashtags
hashtags = (
    df["hashtag"]
    .dropna()
    .astype(str)
    .str.strip()
    .tolist()
)

resultados = []

print("📡 Coletando hashtags no Mastodon...")

for tag in hashtags:
    if tag == "":
        continue

    url = f"https://mastodon.social/api/v1/timelines/tag/{tag}?limit=5"

    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            posts = resp.json()

            resultados.append({
                "hashtag": tag,
                "quantidade_posts": len(posts)
            })

            print(f"✅ #{tag}: {len(posts)} posts encontrados")

        else:
            print(f"⚠️ Erro ao buscar #{tag}: {resp.status_code}")

    except Exception as e:
        print(f"❌ Erro com #{tag}: {e}")

    sleep(2)  

# Salva tudo em um único arquivo
df_result = pd.DataFrame(resultados)
df_result.to_csv("mastodon_filmes_series.csv", index=False)

print("\n📂 Dados salvos em mastodon_filmes_series.csv")
print(df_result.head())