from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests, json
from webscrapping import BS

app = FastAPI()

origins = ["http://localhost:5500"
           ,"http://127.0.0.1:5500"
           ] #porta do liveserver / apenas localhost não funcionou

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def limpar_dados_busca(dados_sujos):
    resultados = dados_sujos.get('results')
    dados_limpos = []
    for heroi in resultados:
        nome = heroi["biography"]["full-name"]
        alter_ego = heroi["name"]
        img = heroi["image"]["url"]
        dados_limpos.append({"nome" : nome, "alterego" : alter_ego, "img" : img})
    return dados_limpos

def limpar_dados_id(dados_sujos):
    try: alter_ego = dados_sujos["name"]
    except: alter_ego = ""

    try: img = dados_sujos["image"]["url"]
    except: img = ""

    try: nome = dados_sujos.get("biography")["full-name"]
    except: nome = ""

    dados_limpos = {"nome" : nome, "alterego" : alter_ego, "img" : img}
    return dados_limpos

def salvar_ultimo_heroi(id):
    with open("ultimo-heroi.json", "w") as arquivo:
        arquivo.write(str(id))

def ultimo_heroi_salvo():
    with open("ultimo-heroi.json", "r") as arquivo:
        return int(arquivo.read())

@app.get("/")
async def home():
    return {"Olá":"Mundo"}

@app.get("/buscar")
def buscar_heroi(nome : str):
    url = f"https://superheroapi.com/api/4315a5181d6f31a64e55172efb01bc64/search/{nome}"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()
        dados_limpos = limpar_dados_busca(dados)
        return dados_limpos
    else:
        return {"Erro:": "Não foi possível achar o herói"} 
    
@app.get("/atualizar-banco")
def atualizar_banco():
    #url = "https://superheroapi.com/ids.html"
    #ultimo_heroi_api = BS.verificar_ultimo_heroi(url)
    #if ultimo_heroi_api > ultimo_heroi_salvo():
    #    salvar_ultimo_heroi(ultimo_heroi_api)
    ultimo_heroi = ultimo_heroi_salvo()
    
    herois = []
    for i in range(ultimo_heroi):
        url = f"https://superheroapi.com/api/4315a5181d6f31a64e55172efb01bc64/{i}"
        resposta = requests.get(url)
        #if resposta.status_code == 200:
        #    dados = resposta.json()
        #    dados_limpos = limpar_dados_id(dados)
        #    herois.append(dados_limpos)
        herois.append(resposta.json())
    
    return herois
