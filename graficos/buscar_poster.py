#este script tem como foco fazer uma requisição a API do TMDB para retornar posteres de filmes e séries
import requests #importa a biblioteca de requisição

API_KEY = "283e88fb6be72ac17405ed4a1701bbd5"  #chave de acesso única a api
BASE_URL = "https://api.themoviedb.org/3" #url base do site do TMDB

def buscar_poster(titulo): #definindo uma função para buscar as imagens pelo título da obra
    # procura pelo nome do filme ou série
    url = f"{BASE_URL}/search/multi"

    params = { #parametros da requisição
        "api_key": API_KEY,  # manda a chave pra poder acessar
        "query": titulo,    # manda o título que a gente quer buscar
        "language": "pt-BR" #definindo que os dados venham em português
    }

    resposta = requests.get(url, params=params) # faz a requisição pro site
    dados = resposta.json()  # transforma a resposta em formato de dicionário JSON

    if dados.get("results"): #estrutura de condição que diz se achar resultados estes devem ser mostrados pelo método get
        poster_path = dados["results"][0].get("poster_path")  # pega o caminho do poster do primeiro resultado

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}" # monta a URL final da imagem e retorna ela

    return None #caso não encontre ou ocorra algum erro, retorna none
