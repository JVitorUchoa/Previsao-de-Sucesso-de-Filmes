import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

teste_biblioteca=os.path.abspath('../analise') 
sys.path.append(teste_biblioteca)

from analise import unificar_dados, normalizar_dados, calcular_sucesso


df_unificado = unificar_dados()
if df_unificado.empty:
    print("Nenhum dado foi carregado.")
    exit()

df_normalizado = normalizar_dados(df_unificado)

df_final = calcular_sucesso(df_normalizado)

# FILMES
df_filmes = df_final[df_final["tipo_obra_x"] == "filme"]
df_top15_filmes = df_filmes.sort_values(by ="sucesso_pontos", ascending=False).head(15)
# SÉRIES
df_series = df_final[df_final["tipo_obra_x"] == "serie"]
df_top15_series = df_series.sort_values(by= "sucesso_pontos", ascending=False).head(15)

sns.set(style='whitegrid')

fig,axes=plt.subplots(2,1,figsize=(10,12))

# FILMES
sns.barplot(
    data=df_top15_filmes,
    y='titulo_x',
    x='sucesso_pontos',
    hue='genero',
    dodge=False,
    palette='tab10',
    ax=axes[0]
)
axes[0].set_title('Top 15 filmes mais populares por Gênero',fontsize=10,pad=12)
axes[0].set_xlabel('Popularidade',fontsize=10)
axes[0].set_ylabel('Nome de filmes',fontsize=10)
axes[0].legend(title='Gênero',bbox_to_anchor=(1.05,1),loc='upper left',fontsize=8,title_fontsize=8)

# SÉRIES

sns.barplot(
    data=df_top15_series,
    y='titulo_x',
    x='sucesso_pontos',
    hue='genero',
    dodge=False,
    palette='tab10',
    ax=axes[1]
)
axes[1].set_title('Top 15 séries mais populares por Gênero',fontsize=10,pad=12)
axes[1].set_xlabel('Popularidade',fontsize=10)
axes[1].set_ylabel('Nome de séries',fontsize=10)
axes[1].legend(title='Gênero',bbox_to_anchor=(1.05,1),loc='upper left',fontsize=8,title_fontsize=8)


plt.tight_layout()
plt.show()