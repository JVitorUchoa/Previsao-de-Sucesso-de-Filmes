import requests #faz as requisições HTTP à API do TMDB
import pandas as pd #importando o pandas para a coleta dos dados
import json #grava os dados em formato .json
from concurrent.futures import ThreadPoolExecutor, as_completed #permite processar vários filmes em paralelo, acelerando o programa
from time import sleep #cria pequenas pausas entre as requisições, evitando sobrecarregar a API

API_KEY = "283e88fb6be72ac17405ed4a1701bbd5" #chave para ter acesso a API
BASE_URL = "https://api.themoviedb.org/3"  #URL base da API
CSV_FILE = "filmes_futuros_filtrados.csv" #nomes dos arquivos csv e json
JSON_FILE = "filmes_futuros_filtrados.json"

#lista de países relevantes,de acordo com sua relevância cinematógrafica,onde define que apenas filmes produzidos nesses lugares que devem ser coletados
PAISES_RELEVANTES = {
    "US","GB","FR","DE","IT","ES","IN","JP","KR","CN","BR","CA","MX","RU","AU"
}

#função para buscar filmes entre 2025-11-01 e 2028-12-31
def discover_movies_future(api_key, start_date="2025-11-01", end_date="2028-12-31"):
    filmes = [] #inicializa uma lista vazia onde os filmes coletados serão armazenados
    page = 1 #inicializa o contador de página
    while True: #O loop continuará executando requisições página por página até que a condição de parada seja atingida
        url = f"{BASE_URL}/discover/movie" #endpoint para a busca dos filmes
        params = {
            "api_key": api_key,
            "language": "pt-BR",
            "sort_by": "primary_release_date.asc",
            "primary_release_date.gte": start_date,
            "primary_release_date.lte": end_date,
            "page": page
        }
        r = requests.get(url, params=params) #faz a requisição HTTP GET para a URL com os parâmetros definidos
        data = r.json() #converte a resposta da API,que está no formato JSON, em um dicionário python

        if "results" not in data:
            break

        filmes.extend(data["results"])
        print(f"Página {page} coletada, total acumulado: {len(filmes)} filmes")#imprime uma mensagem que retorna qual página foi coletada e quais os filmes amazendados
        #condição de parada
        if page >= data.get("total_pages", 1):#se a página atual for maior ou igual ao número total de páginas,significa que todos os resultados foram coletados,e o loop é interrompido
            break
        page += 1
        sleep(0.2)
    return filmes #retorna a lista final de filmes, juntando todas as páginas

#função para obter dados filtrados
def get_movie_info(f):
    movie_id = f["id"] #recebe um filme obtido no discover, por meio do id

    detalhes = requests.get( #faz uma nova requisição, mas este referente as detalhes do filme que está sendo tratado no momento
        f"{BASE_URL}/movie/{movie_id}",
        params={"api_key": API_KEY, "language": "pt-BR"} #definindo um parametro para que as respostas cheguem em português
    ).json() #converte as respostas para um dicionário python, chamado detalhes

    # países do filme
    paises = [p["iso_3166_1"] for p in detalhes.get("production_countries", [])]

    # só mantém filmes de países relevantes
    if not any(p in PAISES_RELEVANTES for p in paises):
        return None

    # extrai os gêneros dos filmes
    generos = ", ".join([g["name"] for g in detalhes.get("genres", [])])

    return { #retorna os detalhes dos filmes, onde será retornadas informações que foram indicadas
        "Nome": f.get("title"),
        "Data": f.get("release_date"),
        "Popularidade": f.get("popularity"),
        "Gênero": generos
    }

# função para salvar CSV progressivamente
def save_csv(data, file=CSV_FILE): #cria um DataFrame e salva em .csv, ordenado por popularidade decrescente
    df = pd.DataFrame(data)
    if not df.empty:
        df = df.sort_values(by="Popularidade", ascending=False)
    df.to_csv(file, index=False, encoding="utf-8-sig")

#  função para salvar JSON 
def save_json(data, file=JSON_FILE): #salva a mesma lista de dicionários em formato .json
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Coleta principal 
print(" Coletando filmes futuros do TMDB (Novembro/2025 a 2028)...")
filmes_raw = discover_movies_future(API_KEY, start_date="2025-11-01", end_date="2028-12-31")
print(f"📝 {len(filmes_raw)} filmes encontrados no Discover.")

linhas = [] #inicializa uma lista vazia que irá armazenar os dicionários de filmes formatados e filtrados
batch_size = 20 #significa que, a cada 20 filmes processados, o código irá executar uma ação de salvar os dados
#processamento paralelo 
with ThreadPoolExecutor(max_workers=10) as executor: #cria um executor de threads, onde limita o número de requisição a 10, não sobrecarregando API
    futures = [executor.submit(get_movie_info, f) for f in filmes_raw] #para cada filme na lista, uma tarefa é criada e submetida ao executor
    for i, future in enumerate(as_completed(futures), 1): #coleta dos resultados e salve em lotes
        try:
            result = future.result()
            if result:
                linhas.append(result)
        except Exception as e:
            print(f" Erro ao processar filme: {e}")

        if i % batch_size == 0:
            save_csv(linhas)
            save_json(linhas)
            print(f" {i} filmes processados e salvos em CSV e JSON...")

#salva o restante,garante que todos os filmes que foram processados e adicionados à lista linhas,sejam gravados no arquivo CSV e JSON
save_csv(linhas) #chama a função de salvamento em formato CSV
save_json(linhas) #chama a função de salvamento em formato JSON
print(f"✅ Coleta finalizada! {len(linhas)} filmes futuros (Nov/2025-2028) filtrados, ordenados por popularidade e salvos em CSV e JSON.")
