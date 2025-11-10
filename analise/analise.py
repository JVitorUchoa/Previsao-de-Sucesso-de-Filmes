import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os
import json

# Variavel está armazenando o caminho dos arquivos!
DADOS_PATH = "./dados/"
MASTODON_PATH = "./mastodon/mastodon_coleta/"
YOUTUBE_PATH =  "./youtube/"

# Carregando dados do TMDB
def carregar_dados_tmdb(nome_arquivo, tipo_obra, categoria):
    nome_base, _ = os.path.splitext(nome_arquivo)

    colunas_tmdb = ["titulo", "popularidade", "hashtag_chave", "tipo_obra", "categoria_status", "fonte_arquivo"]
    
    df_csv_tmdb = pd.DataFrame(columns=colunas_tmdb)
    df_json_tmdb = pd.DataFrame(columns=colunas_tmdb)
    
    # Aqui carrega os arquivos .csv
    caminho_csv = os.path.join(DADOS_PATH, nome_base + ".csv")
    try:
        df_csv_tmdb = pd.read_csv(caminho_csv)
        print(f"Lido com sucesso: {nome_base}.csv")
    except:
        print(f"\n Atenção: Falha ao ler csv") 
    
    # Aqui carrega os arquivos .json
    caminho_json = os.path.join(DADOS_PATH, nome_base + ".json")
    try:
        df_json_tmdb = pd.read_json(caminho_json)
        print(f"Lido com sucesso: {nome_base}.json")
    except:
        print(f"\n Atenção: Falha ao ler json")

    df = pd.concat([df_csv_tmdb, df_json_tmdb], ignore_index=True)

    df = df.rename(columns={"Popularidade": "popularidade", "Nome": "titulo"})
             
    df["hashtag_chave"] = (df["titulo"].astype(str).str.lower().str.replace(r'[^a-z0-9]', '' , regex=True))

    df["tipo_obra"] = tipo_obra
    df["categoria_status"] = categoria
    df["fonte_arquivo"] = nome_arquivo

    df_final_dados = df[colunas_tmdb].copy()
    print(f"📂 Foi carregado {df_final_dados.shape[0]} registros.")
    return df_final_dados

# Juntando os dados do TMDB
def unificar_dados_tmdb():
    df_lista_tmdb = [
        carregar_dados_tmdb("filmes_top100.csv", tipo_obra="filme", categoria="sucesso"),
        carregar_dados_tmdb("filmes_futuros_filtrados.csv", tipo_obra="filme", categoria="futuro"),
        carregar_dados_tmdb("series_futuras_com_renovadas.csv", tipo_obra="serie", categoria="sucesso"),
        carregar_dados_tmdb("series_futuras_filtradas.csv", tipo_obra="serie", categoria="futuro")        
    ]

    df_unificado = pd.concat(df_lista_tmdb, ignore_index=True)

    df_unificado.drop_duplicates(subset=["hashtag_chave"], keep="first", inplace=True)
    if df_unificado.empty:
        print("\n Atenção: Nenhum dado do TMDB foi carregado.")
        return None

    print(f"DataFrame TMDB final: {df_unificado.shape[0]} registros carregados.")
    return df_unificado

# Carregando dados do Mastodon
def carregar_dados_mastodon():
    caminho_arquivo_mastodon = os.path.join(MASTODON_PATH, "mastodon_hashtags.csv")
    try:
        df_mastodon = pd.read_csv(caminho_arquivo_mastodon)
        df_mastodon.rename(columns={"hashtag": "hashtag_chave"}, inplace=True)

        df_mastodon["hashtag_chave"] = (
            df_mastodon["hashtag_chave"].astype(str).str.lower().str.replace(r'[^a-z0-9]', '', regex=True))

        df_mastodon.dropna(subset=["hashtag_chave"], inplace=True)
        df_mastodon.drop_duplicates(subset=["hashtag_chave"], keep="first", inplace=True)

        print(f"\n 📂 Foram carregados do Mastodon: {df_mastodon.shape[0]} registros.")
        return df_mastodon
    except:
        print("\n Atenção: Arquivo do Mastodon não encontrado.")

# Carregando dados do YouTube
def carregar_dados_youtube(nome_arquivo, tipo_obra, categoria):
    nome_base, _ = os.path.splitext(nome_arquivo)

    colunas_youtube = ["titulo", "views", "hashtag_chave", "tipo_obra", "categoria_status", "fonte_arquivo"]

    df_json_youtube = pd.DataFrame(columns=colunas_youtube)

    # Aqui carrega o arquivo .json 
    caminho_json = os.path.join(YOUTUBE_PATH, nome_base + ".json")
    try:
        df_json_youtube = pd.read_json(caminho_json)
        print(f"Lido com sucesso: {nome_base}.json")

    except:
        print(f"\n Atenção: Falha ao ler json")
        
    df_json_youtube.rename(columns={"Views": "views", "Nome": "titulo"}, inplace=True) 
     
    df_json_youtube["hashtag_chave"] = (df_json_youtube["titulo"].astype(str).str.lower().str.replace(r'[^a-z0-9]', '' , regex=True))

    df_json_youtube['views'] = pd.to_numeric(df_json_youtube['views'], errors='coerce').fillna(0).astype(int)
    df_json_youtube["tipo_obra"] = tipo_obra
    df_json_youtube["categoria_status"] = categoria
    df_json_youtube["fonte_arquivo"] = nome_arquivo

    df_final = df_json_youtube[colunas_youtube].copy()
    print(f"\n 📂 Foi carregado do YouTube: {df_final.shape[0]} registros.")
    return df_final

def dados_youtube():
    df_youtube = carregar_dados_youtube("resultados_youtube.json", tipo_obra="mistudado", categoria="sucesso")
    if not df_youtube.empty:
         df_youtube.drop_duplicates(subset=["hashtag_chave"], keep="first", inplace=True)
    return df_youtube 

# Juntando os dados do TMDB, Mastodon e YouTube
def unificar_dados():
    df_tmdb_final = unificar_dados_tmdb()
    
    df_mastodon_final = carregar_dados_mastodon()

    df_youtube_final = dados_youtube()
 
    df_tmdb_mastodon = pd.merge(df_tmdb_final, df_mastodon_final[["hashtag_chave", "quantidade_posts"]], on="hashtag_chave", how="left")
    df_unificado_tudo = pd.merge(df_tmdb_mastodon, df_youtube_final[["hashtag_chave", "views"]], on="hashtag_chave", how="left")

    df_unificado_tudo["quantidade_posts"] = df_unificado_tudo["quantidade_posts"].fillna(0)
    df_unificado_tudo["views"] = df_unificado_tudo["views"].fillna(0)

    print(f"\n Todos os dados foram unificados.")
    return df_unificado_tudo

# Normalizando (ou padronizar) os dados
def normalizarlizacao(df):
    df_normalizar = df.copy()
    scaler = MinMaxScaler()

    df_normalizar["popular_normalizacao"] = (scaler.fit_transform(df_normalizar[["popularidade"]]) * 100)

    df_normalizar["posts_normalizacao"] = (scaler.fit_transform(df_normalizar[["quantidade_posts"]]) * 100)

    if "views" in df_normalizar.columns:
        df_normalizar["views_normalizacao"] = (scaler.fit_transform(df_normalizar[["views"]]) * 100)
    else:
        df_normalizar["views_normalizacao"] = 0  
        print(f"\n Aviso: Coluna 'views' não encontrada para normalização. Atribuindo 0.")  

    print(f"\n Dados foram normalizados, estão padronizados e prontos para análise!")
    return df_normalizar

# Fazendo o calcúlo de sucesso
def calcular_sucesso(df):
    df["sucesso_pontos"] = (df["popular_normalizacao"] * 0.5 + 
                            df["posts_normalizacao"] * 0.3 + 
                            df["views_normalizacao"] * 0.2).round(2)

    df["sucesso_classificar"] = pd.cut(
        df["sucesso_pontos"], bins=[0, 20, 50, 60, 80, 100],
        labels=["Muito Baixo", "Baixo", "Médio", "Alto", "Muito Alto"],
        include_lowest=True)
    
    print(f"\n Acaba de ser calculado a previsão de sucesso das obras!")
    return df

