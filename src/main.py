from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

origins = ["http://localhost:5500"]

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
        dados_limpos.append({"nome" : nome, "alter-ego" : alter_ego, "img" : img})
    return dados_limpos


@app.get("/")
async def home():
    return {"Olá":"Mundo"}

@app.get("/imc-heroi")
def calcularImc(altura: float, peso: int):
    return {"IMC":f"O IMC do herói é {peso / (altura / 100 * 2)}"}

class Heroi(BaseModel):
    nome: str
    peso: int
    altura: float

@app.post("/heroi")
def postagem(heroi: Heroi):
    return {"Heroi": f"O(A) {heroi.nome} de altura {heroi.altura} e peso {heroi.peso} foi cadastrado(a) com sucesso."}

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