import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Carregar os dados,cria uma analise classifica,grafico barra e nuvem de palavras
df = pd.read_csv("mastodon_hashtags.csv")

df = df.dropna(subset=["hashtag"])

def analisar_sentimento(texto):
    blob = TextBlob(str(texto))
    return blob.sentiment.polarity

df["sentimento"] = df["hashtag"].apply(analisar_sentimento)

def classificar(p):
    if p > 0.1:
        return "positivo"
    elif p < -0.1:
        return "negativo"
    else:
        return "neutro"

df["classificacao"] = df["sentimento"].apply(classificar)

print(df["classificacao"].value_counts())

df["classificacao"].value_counts().plot(kind="bar", color=["green", "red", "gray"])
plt.title("Distribuição de Sentimentos nas Hashtags")
plt.xlabel("Sentimento")
plt.ylabel("Quantidade")
plt.show()

texto_todos = " ".join(df["hashtag"].astype(str))
nuvem = WordCloud(width=800, height=400, background_color="white").generate(texto_todos)
plt.imshow(nuvem, interpolation="bilinear")
plt.axis("off")
plt.show()
