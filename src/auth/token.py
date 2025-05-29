import requests
import json
from dotenv import load_dotenv
import os
import subprocess

load_dotenv()

def auth(reload: bool = False):
    identificador = os.getenv("IDENTIFICADOR", "xxxx")
    senha = os.getenv("SENHA", "xxxx")
    token = None
    if token is None and reload is False:
        try:
            with open("src/auth/token.txt", "r") as file:
                token = file.read().strip()
                if token:
                    print("Usando o token salvo.")
                    return token
                else:
                    new_token = auth(reload=True)
                    return new_token
        except Exception as e:
            print(f"Erro ao ler o token: {e}")
            raise Exception(f"Erro {response.status_code}: {response.text}")
    else:
        url = "https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/OAUth/v1"

        headers = {
            "accept": "*/*",
            "Content-Type": "application/json",
            "Identificador": identificador,
            "Senha": senha
        }
        print("Fazendo login...")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            try:
                response_json = response.json()
                local_token = response_json["items"]["tokenautenticacao"]
                with open("src/auth/token.txt", "w") as file:
                    file.write(local_token)
                print("Login bem-sucedido")
                return local_token
            except Exception as e:
                print(f"Erro ao salvar o token: {e}")
                return None
        else:
            raise Exception(f"Erro {response.status_code}: {response.text}")
        

def check_token(token):
    url = 'https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/HidroUF/v1'
    headers = {
        "accept": "*/*",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 401:
        print("Token inválido ou expirado. Realizando novo login...")
        token = auth(reload=True)
        if token is None:
            raise Exception("Falha ao obter um novo token.")
    elif response.status_code != 200:
        raise Exception(f"Erro {response.status_code}: {response.text}")
    return token