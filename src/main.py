from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests, json, os
from webscrapping import BS

app = FastAPI()

chave_api = "4315a5181d6f31a64e55172efb01bc64"

origins = ["http://localhost:5500"
           ,"http://127.0.0.1:5500"
           ] #porta do liveserver / apenas localhost com porta não funcionou

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

def limpar_dados_id(dados_sujos, id_heroi):
    try: alterego = dados_sujos["name"]
    except: alterego = ""

    try: img = dados_sujos["image"]["url"]
    except: img = ""

    try: nome = dados_sujos.get("biography")["full-name"]
    except: nome = ""

    dados_limpos = {"id" : id_heroi, "nome" : nome, "alterego" : alterego, "img" : img}
    return dados_limpos

def salvar_ultimo_heroi(id):
    with open("ultimo-heroi.json", "w") as arquivo:
        arquivo.write(str(id))

def ultimo_heroi_salvo():
    if not os.path.exists("./ultimo-heroi.json"):
        print(f"Erro: O arquivo não existe.")
        return 0
    
    with open("ultimo-heroi.json", "r") as arquivo:
        numero = json.load(arquivo)
    
    if not isinstance(numero, (int, float)):
            print("Erro: O arquivo não contém um número válido.")
            return 0
    
    return numero
    
def atualizar_banco_herois(qtd_herois):
    herois = []
    for id in range(1, qtd_herois+1):
        url = f"https://superheroapi.com/api/{chave_api}/{id}"
        try:
            resposta = requests.get(url)
            if resposta.status_code == 200:
                dados = resposta.json()
                dados_limpos = limpar_dados_id(dados, id)
                herois.append(dados_limpos)
            else: raise ValueError(f"status code: {resposta.status_code}")
        except Exception as ex1:
            print(f"Erro ao fazer o request do id {id} na função registrar_herois.\nErro: {ex1}\nExecutando segunda tentativa")
            try:
                resposta = requests.get(url)
                if resposta.status_code == 200:
                    dados = resposta.json()
                    dados_limpos = limpar_dados_id(dados, id)
                    herois.append(dados_limpos)
                    print(f"A segunda tentativa de coletar o heroi {id} foi bem sucedida.")
                else: raise ValueError(f"status code: {resposta.status_code}")
            except Exception as ex2:
                print(f"Erro ao executar a segunda tentativa no request do id {id}.\nErro: {ex2}")

    with open("herois.json", "w") as arquivo:
        json.dump(herois, arquivo, ensure_ascii=False, indent=4)

def ler_json_herois():
    if not os.path.exists("./ultimo-heroi.json"):
        print(f"Erro: O arquivo não existe.")
        return None
    
    with open("herois.json", "r") as arquivo:
        return json.load(arquivo)

@app.get("/")
async def home():
    return {"Olá":"Mundo"}

@app.get("/buscar")
def buscar_heroi(nome : str):
    url = f"https://superheroapi.com/api/{chave_api}/search/{nome}"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()
        dados_limpos = limpar_dados_busca(dados)
        return dados_limpos
    else:
        return {"Erro:": "Não foi possível achar o herói"} 
    
@app.put("/atualizar-banco")
def atualizar_banco():
    url = "https://superheroapi.com/ids.html"
    qtd_heroi_api = BS.verificar_ultimo_heroi(url)
    if qtd_heroi_api > ultimo_heroi_salvo():
        salvar_ultimo_heroi(qtd_heroi_api)
    qtd_herois = ultimo_heroi_salvo()
    atualizar_banco_herois(qtd_herois)
    return None

@app.get("/pegar-herois")
def pegar_herois():
    return ler_json_herois()