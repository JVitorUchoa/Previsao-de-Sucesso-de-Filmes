import pandas as pd
import matplotlib.pyplot as plt

# Carrega o dataset top 10,generos mais frequente
df = pd.read_csv("filmes.csv")

top_filmes = df.sort_values(by="Popularidade", ascending=False).head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_filmes["Nome"], top_filmes["Popularidade"], color='skyblue')
plt.gca().invert_yaxis()
plt.title(" Top 10 Filmes Mais Populares")
plt.xlabel("Popularidade")
plt.ylabel("Filme")
plt.tight_layout()
plt.show()

df["Gênero"] = df["Gênero"].fillna("Desconhecido")
generos = df["Gênero"].str.split(", ").explode().value_counts().head(10)

plt.figure(figsize=(8, 5))
generos.plot(kind='bar', color='orange')
plt.title(" Top 10 Gêneros Mais Frequentes")
plt.xlabel("Gênero")
plt.ylabel("Quantidade de Filmes")
plt.tight_layout()
plt.show()
