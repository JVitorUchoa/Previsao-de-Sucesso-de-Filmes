import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Dashboard Mastodon - Hashtags de Filmes")

df = pd.read_csv("mastodon_hashtags.csv")


df = df.dropna(subset=["hashtag"])       
df = df[df["hashtag"].str.strip() != ""] 
df['quantidade_posts'] = pd.to_numeric(df['quantidade_posts'], errors='coerce').fillna(0).astype(int)

st.subheader("Tabela de Hashtags e Quantidade de Posts")
st.dataframe(df.sort_values("quantidade_posts", ascending=False))


st.subheader("Top 10 Hashtags Mais Populares")
top10 = df.sort_values("quantidade_posts", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10,6))
ax.bar(top10["hashtag"], top10["quantidade_posts"], color="teal")
ax.set_xlabel("Hashtag")
ax.set_ylabel("Quantidade de Posts")
ax.set_title("Top 10 Hashtags de Filmes no Mastodon")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig)

st.subheader(" Distribuição de Posts por Hashtag")
fig2, ax2 = plt.subplots(figsize=(8,8))
ax2.pie(df['quantidade_posts'], labels=df['hashtag'], autopct='%1.1f%%', startangle=140)
ax2.set_title("Distribuição de Posts por Hashtag")
st.pyplot(fig2)
