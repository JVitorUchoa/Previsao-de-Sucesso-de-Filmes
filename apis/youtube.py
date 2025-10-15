import pandas as pd
import requests

#Arquivo dos dados dos filmes
arquivo = pd.read_json("Previsao-de-Sucesso-de-Filmes/apis/filmes_futuros_filtrados.json")

#Função para se conectar com o Youtube
def conexao_youtube(pesquisar):
    #A chave API
    api_key = 'AIzaSyCcE_YpT1UQ7DSQWvz-PSvQC2u85_2EwYI'
    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",  #É a parte que vai puxar. Snippet é os dados básicos (nome, canal...)
        'q': pesquisar,  #q é usado na busca.
        "key": api_key,
        "maxResults": 1
    }

    #Testar se tá tendo resposta
    resposta = requests.get(url, params=params)

    if resposta.status_code == 200:
        resposta_json = resposta.json()
        print("Video: ", resposta_json["items"][0]["snippet"]["title"])

    else:
        print("Não foi possível se conectar ao Youtube.")
        print("Status Code:", resposta.status_code)

#Puxar os dados necessários do arquivo
for index, linha in arquivo.iterrows(): #Lê linha por linha
    titulo = linha["Nome"]
    data = linha["Data"] #Data completa. Ex: 2024-03-29
    ano = data.split("-")[0]   #Pega apenas o ano
    pesquisar = f"Trailer {titulo} - {ano}"

    #Pesquisa cada obra no Youtube
    conexao_youtube(pesquisar)