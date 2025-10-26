import pandas as pd
import os
import requests

# Caminho do arquivo CSV (ajuste conforme necessário)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Caminhos automáticos. Acessam os arquivos dos filmes e séries dados pela TMDB
filmes = os.path.join(base_dir, "..", "dados", "top50_filmes.json")
series = os.path.join(base_dir, "..", "dados", "top50_filmes.json")

# Ler os arquivos
df_filmes = pd.read_json(filmes)
df_series = pd.read_json(series)

# Apenas uma API key
API_KEY = "AIzaSyCnb8SYLcxzTP1Tf9V5D7zC5JtaE9hKt2Q"

# Endpoint do YouTube
URL_SEARCH = 'AIzaSyCz0LBJhe0Rxwx7RAaaQnngPUI9N1I0meM'

# Lista para armazenar os resultados
resultados = []

for index, linha in df_filmes.iterrows():
    titulo = linha["Nome"]
    data = linha.get("Data", "")
    ano = data.split("-")[0] if data else ""
    
    pesquisar = f"Trailer {titulo} - {ano}".strip()

    # Monta os parâmetros da requisição
    params = {
        "part": "snippet",
        "q": pesquisar,
        "key": API_KEY,
        "maxResults": 3
    }

    # Faz a requisição ao YouTube
    resposta = requests.get(URL_SEARCH, params=params)

    # Verifica se funcionou
    if resposta.status_code != 200:
        print(f"Erro {resposta.status_code} ao buscar: {pesquisar}")
        continue

    resposta_json = resposta.json()
    items = resposta_json.get("items", [])
    
    obra_result = {"obra": titulo, "videos": []}

    for item in items:
        kind = item["id"].get("kind", "")
        video_id = item["id"].get("videoId") if kind == "youtube#video" else None
        titulo_video = item["snippet"]["title"]
        obra_result["videos"].append({
            "titulo_video": titulo_video,
            "video_id": video_id,
            "kind": kind
        })

    resultados.append(obra_result)

# Exibir resultados
for r in resultados:
    print(f"\n🎬 Obra: {r['obra']}")
    for v in r["videos"]:
        vid = v["video_id"] if v["video_id"] else "SEM ID"
        print(f" - {v['titulo_video']} | ID: {vid} | Kind: {v['kind']}")
