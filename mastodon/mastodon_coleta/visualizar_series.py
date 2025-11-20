import pandas as pd
import matplotlib.pyplot as plt

# Carrega o dataset de séries
df = pd.read_csv("series.csv")

print("📊 Análise Exploratória de Séries")

# Top 10 séries mais populares (geral)
top_series = df.sort_values(by="Popularidade", ascending=False).head(10)

plt.figure(figsize=(12, 6))
plt.barh(top_series["Nome"], top_series["Popularidade"], color='lightcoral')
plt.gca().invert_yaxis()
plt.title("Top 10 Séries Mais Populares")
plt.xlabel("Popularidade")
plt.ylabel("Série")
plt.tight_layout()
plt.show()


# Análise de gêneros
df["Gênero"] = df["Gênero"].fillna("Desconhecido")
generos = df["Gênero"].str.split(", ").explode().value_counts().head(10)

plt.figure(figsize=(10, 6))
generos.plot(kind='bar', color='lightseagreen')
plt.title("Top 10 Gêneros de Séries Mais Frequentes")
plt.xlabel("Gênero")
plt.ylabel("Quantidade de Séries")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

