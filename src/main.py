from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

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
        dados_heroi = resposta.json()
        return dados_heroi
    else:
        return {"Erro:": "Não foi possível achar o herói"} 