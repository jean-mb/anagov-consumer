import requests
import json
from dotenv import load_dotenv
import os
import subprocess

load_dotenv()


identificador = os.getenv("IDENTIFICADOR", "xxxx")
senha = os.getenv("SENHA", "xxxx")
token = None

def limpar_terminal():
    os.system('clear')

def auth(login: str, senha: str, reload: bool = False):

    global token

    if token is None and reload is False:
        try:
            with open("token.txt", "r") as file:
                token = file.read().strip()
                if token:
                    print("Usando o token salvo.")
                    return token
                else:
                    new_token = auth(login, senha, reload=True)
                    return new_token
        except Exception as e:
            print(f"Erro ao ler o token: {e}")
            raise Exception(f"Erro {response.status_code}: {response.text}")
    else:
        url = "https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/OAUth/v1"

        headers = {
            "accept": "*/*",
            "Content-Type": "application/json",
            "Identificador": login,
            "Senha": senha
        }
        print("Fazendo login...")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            try:
                response_json = response.json()
                local_token = response_json["items"]["tokenautenticacao"]
                with open("token.txt", "w") as file:
                    file.write(local_token)
                print("Login bem-sucedido")
                return local_token
            except Exception as e:
                print(f"Erro ao salvar o token: {e}")
                return None
        else:
            raise Exception(f"Erro {response.status_code}: {response.text}")

def abrir_chrome(url: str):
    try:
        subprocess.run(
            ["flatpak", "run", "com.google.Chrome", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )
    except Exception as e:
        print(f"Erro: {e}")

def get_estacao(codigo_estacao: str):
    global token
    url = (
        "https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/"
        f"HidroInventarioEstacoes/v1?C%C3%B3digo%20da%20Esta%C3%A7%C3%A3o={codigo_estacao}"
    )

    headers = {
        "accept": "*/*",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
         response_json = response.json()
         if len(response_json["items"]) != 0:
             return response.json()
         else:
             print(response_json["message"])
             return None
    elif response.status_code == 401:
        token = auth(identificador, senha, reload=True)
        return None
    else:
        print(f"Erro {response.status_code}: {response.text}")
        return None

def get_estacao_coords(estacao: dict):
    items = estacao["items"][0]
    print(f"\n{items['Latitude']} {items['Longitude']}\n")
    url = f"https://www.google.com/maps/search/?api=1&query={items['Latitude']},{items['Longitude']}"
    abrir_chrome(url)

if __name__ == "__main__":
    codigo_estacao = 0
    token = auth(identificador, senha)
    while True:
        if codigo_estacao == 0:
            codigo_estacao = str(input("Digite o código da estação: "))
            if codigo_estacao.lower() == "q":
                break
        if not codigo_estacao.isdigit():
            codigo_estacao = 0
            continue
        if codigo_estacao is None or codigo_estacao == "":
            codigo_estacao = 0
            continue
        try:
            resultado = get_estacao(codigo_estacao)
            codigo_estacao = 0 
            if resultado is None:
                continue
        except Exception as e:
            print(e)

        estacao = resultado["items"][0]
        print("=" * 40)
        print(f"\n{estacao["codigoestacao"]} - Estação {estacao["Tipo_Estacao"]} em {estacao["Municipio_Nome"]}: {resultado['items'][0]['Estacao_Nome']}\n")
        print("O que deseja fazer?")
        print(
            "1 - Ver coordenadas da estação\n"
            "2 - Ver dados da estação\n"
            "3 - Próxima estação\n"
            "4 - Sair\n"
        )
        opcao = str(input("Digite a opção: "))
        match opcao:
            case "1":
                get_estacao_coords(resultado)
            case "4":
                break
            case _:
                print("Opção inválida, tente novamente.")
                continue

    print("\nBye")