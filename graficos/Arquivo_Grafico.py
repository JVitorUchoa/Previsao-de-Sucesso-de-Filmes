import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# SÉRIE
arquivo_serie=pd.read_csv('../dados/series_futuras_com_renovadas.csv')
arquivo_filme=pd.read_csv('../dados/filmes_top100.csv')

arquivo_serie=arquivo_serie.sort_values(by='Popularidade',ascending=False).head(15)
arquivo_filme=arquivo_filme.sort_values(by='Popularidade',ascending=False).head(15)

sns.set(style='whitegrid')

fig,axes=plt.subplots(2,1,figsize=(12,12))
# SÉRIES
sns.barplot(
    data=arquivo_serie,
    y='Nome',
    x='Popularidade',
    hue='Gênero',
    dodge=False,
    palette='tab10',
    ax=axes[0]
)
axes[0].set_title('Top 15 Séries mais populares por Gênero',fontsize=14,pad=15)
axes[0].set_xlabel('Popularidade',fontsize=12)
axes[0].set_ylabel('Nome da Série',fontsize=12)
axes[0].legend(title='Gênero',bbox_to_anchor=(1.05,1),loc='upper left')

# FILMES
sns.barplot(
    data=arquivo_filme,
    y='Nome',
    x='Popularidade',
    hue='Gênero',
    dodge=False,
    palette='tab10',
    ax=axes[1],
    
    
)
axes[1].set_title('Top 15 Filmes mais populares por Gênero',fontsize=14,pad=15)
axes[1].set_xlabel('Popularidade',fontsize=12)
axes[1].set_ylabel('Nome da Filme',fontsize=12)
axes[1].legend(title='Gênero',bbox_to_anchor=(1.05,1),loc='upper left')

plt.tight_layout()
plt.show()