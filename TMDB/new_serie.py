#importações de bibliotecas 
import requests #faz as requisições HTTP à API do TMDB
import pandas as pd #importando o pandas para a coleta dos dados
import json #grava os dados em formato .json
from concurrent.futures import ThreadPoolExecutor, as_completed #permite processar várias séries em paralelo, acelerando o programa
from time import sleep #cria pequenas pausas entre as requisições, evitando sobrecarregar a API

API_KEY = "283e88fb6be72ac17405ed4a1701bbd5" #chave de acesso da API TMDB
BASE_URL = "https://api.themoviedb.org/3" #URL base da API
CSV_FILE_SERIES = "series_futuras_com_renovadas.csv" #nomes dos arquivos csv e json
JSON_FILE_SERIES = "series_futuras_com_renovadas.json"

#lista de países relevantes,de acordo com sua relevância cinematógrafica,onde define que apenas séries produzidas nesses lugares que devem ser coletadas
PAISES_RELEVANTES = {
    "US","GB","FR","DE","IT","ES","IN","JP","KR","CN","BR","CA","MX","RU","AU"
}

# função responsável por buscar séries futuras, que não tiveram nenhuma temporada lançada ainda, dentro do limite de data pré-estabelecida
def discover_tv_future(api_key, start_date="2025-11-01", end_date="2028-12-31"):
    series = [] # lista vazia onde será usada para armazenar as séries coletadas
    page = 1 # referente a página um, onde vai sendo interada de acordo com as páginas acessadas
    while True:
        url = f"{BASE_URL}/discover/tv" #endpoint para a busca das séries
        params = { #parâmetros de busca, onde faz a filtragem de acordo com as datas de estreias
            "api_key": api_key,
            "language": "pt-BR",
            "sort_by": "first_air_date.asc",  #ordena por data de estreia
            "first_air_date.gte": start_date, #data inicial
            "first_air_date.lte": end_date, #data final
            "page": page  #pagina referente
        }
        r = requests.get(url, params=params).json() #faz a requisição HTTP GET para a URL com os parâmetros definidos

        if "results" not in r: #se não houver resultados, encerra o loop
            break

        series.extend(r["results"]) #adiciona os resultados à lista principal
        print(f" [NOVAS] Página {page} coletada, total acumulado: {len(series)} séries")#imprime uma mensagem que retorna qual página foi coletada e quais as séries armazenadas

        if page >= r.get("total_pages", 1): #se a página atual for maior ou igual ao número total de páginas,significa que todos os resultados foram coletados,e o loop é interrompido
            break
        page += 1
        sleep(0.2)
    return series #retorna a lista de séries futuras, juntando todas as páginas


#função para obter os detalhes de cada nova série e filtra por país
def get_tv_info(s):
    tv_id = s["id"]  # ID da série para buscar detalhes


    detalhes = requests.get( #faz uma nova requisição, mas este referente as detalhes da série  que está sendo tratada no momento
        f"{BASE_URL}/tv/{tv_id}",
        params={"api_key": API_KEY, "language": "pt-BR"} #definindo um parametro para que as respostas cheguem em português
    ).json() #converte as respostas para um dicionário python, chamado detalhes

    # filtra os países de origem das séries
    paises = detalhes.get("origin_country", [])
    if not any(p in PAISES_RELEVANTES for p in paises):  # só mantém séries de países relevantes
        return None

   #obtém os gêneros da série
    generos = ", ".join([g["name"] for g in detalhes.get("genres", [])]) or "Não informado"

    return { #retorna os detalhes dos filmes, onde será retornadas informações que foram indicadas
        "Nome": s.get("name"),
        "Data": s.get("first_air_date"),
        "Popularidade": s.get("popularity"),
        "Gênero": generos,
        "Tipo": "Nova Série",
        "Temporada": 1
    }

#função responsável pela a busca de séries já existentes, que terão novas temporadas de acordo com as datas estibuladas
def get_renewed_series(api_key, start_date="2025-11-01", max_pages=20):
    renewed = [] #lista de séries renovadas
    page = 1 #referente a página um, onde vai sendo interada de acordo com as páginas acessadas
    while page <= max_pages: #continua a execução enquanto a página atual for menor ou igual ao limite definido max_pages
        url = f"{BASE_URL}/tv/popular" #endpoint de séries populares
        params = {"api_key": api_key, "language": "pt-BR", "page": page} 
        r = requests.get(url, params=params).json() #executa a requisição e converte a resposta em JSON

        if "results" not in r: #se não houver resultados, encerra o loop
            break

        for s in r["results"]: #inicia a iteração sobre cada série encontrada na página de populares.
            detalhes = requests.get( #faz uma requisição separada para obter informações completas,incluindo a lista de temporadas, sobre a série atual
                f"{BASE_URL}/tv/{s['id']}",
                params={"api_key": api_key, "language": "pt-BR"} #que os dados retornados estejam em português
            ).json()

            paises = detalhes.get("origin_country", []) #extrai a lista de países de origem da série
            if not any(p in PAISES_RELEVANTES for p in paises):  # só mantém séries de países relevantes
                continue

            generos = ", ".join([g["name"] for g in detalhes.get("genres", [])]) or "Não informado" #formata a lista de gêneros em uma string legível

            for temporada in detalhes.get("seasons", []): #inicia a iteração sobre a lista de temporadas dentro dos detalhes da série
                air_date = temporada.get("air_date")
                if air_date and air_date >= start_date: #Verifica se a data de lançamento existe e se é igual ou posterior à data de início especificada (start_date), indicando uma temporada futura
                    renewed.append({
                        "Nome": s["name"],
                        "Data": air_date,
                        "Popularidade": s["popularity"],
                        "Gênero": generos,
                        "Tipo": "Renovada",
                        "Temporada": temporada.get("season_number")
                    })
                    break  # já achou uma futura, não precisa checar mais temporadas

        print(f" [RENOVADAS] Página {page} processada, total até agora: {len(renewed)}") 
        if page >= r.get("total_pages", 1):
            break
        page += 1 #incrementa o contador para ir para a próxima página de séries populares
        sleep(0.2)
    return renewed #retorna a lista completa de temporadas futuras encontradas.

#função para salvar CSV 
def save_csv(data, file=CSV_FILE_SERIES):  #cria um DataFrame e salva em .csv, ordenado por popularidade decrescente
    df = pd.DataFrame(data)
    if not df.empty:
        df = df.drop_duplicates(subset=["Nome", "Temporada"])  #evita duplicatas
        df = df.sort_values(by="Popularidade", ascending=False)  #ordena por popularidade
    df.to_csv(file, index=False, encoding="utf-8-sig") #exporta o CSV

#função para salvar JSON 
def save_json(data, file=JSON_FILE_SERIES): #salva a mesma lista de dicionários em formato .json
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

#Execução principal (processamento)
print("\n Coletando séries futuras (Novas + Renovadas) do TMDB...")

# coleta das novas séries
series_raw = discover_tv_future(API_KEY, start_date="2025-11-01", end_date="2028-12-31")
linhas_novas = []
# processa as novas séries em paralelo (acelera a coleta)
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(get_tv_info, s) for s in series_raw]
    for future in as_completed(futures):
        result = future.result()
        if result:
            linhas_novas.append(result)

#coleta das séries renovadas
linhas_renovadas = get_renewed_series(API_KEY, start_date="2025-11-01")

#combina os dois conjuntos de dados, ou seja, mescla as novas séries e as séries renovadas
todas_series = linhas_novas + linhas_renovadas

# salva os resultados em CSV e JSON
save_csv(todas_series)
save_json(todas_series)

print(f"\n Coleta finalizada!")
print(f" → Novas séries: {len(linhas_novas)}")
print(f" → Renovadas: {len(linhas_renovadas)}")
print(f" → Total combinado: {len(todas_series)} salvas em '{CSV_FILE_SERIES}' e '{JSON_FILE_SERIES}'")
