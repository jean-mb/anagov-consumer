import os
import requests
from dotenv import load_dotenv
from src.utils.utils import abrir_chrome, limpar_terminal
import gmplot
from bs4 import BeautifulSoup
from urllib.parse import urlencode

from src.utils.plot_mapa import plotar_estacoes


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_estacoes(token: str, filtros: tuple = None):
    base_url = "https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/HidroInventarioEstacoes/v1"
    param_names = [
        "Código da Estação",
        "Unidade Federativa",
        "Código da Bacia"
    ]
    params = {
        name: value for name, value in zip(param_names, filtros or ()) if value
    }
    
    query_string = urlencode(params)
    url = f"{base_url}?{query_string}" if query_string else base_url
    headers = {
        "accept": "*/*",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Erro {response.status_code}: {response.text}")
        return None

    response_json = response.json()
    items = response_json.get("items", [])
    if not items:
        print(response_json.get("message", "Nenhuma estação encontrada"))
        return None
    
    return response

def get_estacao_coords(estacao: dict):
    items = estacao["items"][0]
    print(f"\n{items['Latitude']} {items['Longitude']}\n")
    url = f"https://www.google.com/maps/search/?api=1&query={items['Latitude']},{items['Longitude']}"
    abrir_chrome(url)


def menu_listar_estacoes(token):
    limpar_terminal()
    print("=" * 40)
    print("Filtros")
    codigo_estacao = str(input("Digite o código da estação (ou deixe em branco para todas): "))
    bacia = str(input("Digite o código da bacia (ou deixe em branco para todas): "))
    estado = str(input("Digite o código do estado (ou deixe em branco para todos): "))
    filtros = (bacia, estado, codigo_estacao)
    print("=" * 40)
    print("\n")
    return get_estacoes(token, filtros)
    
def listar_estacoes(estacoes):
    estacoes_json = estacoes.json()
    items = estacoes_json.get("items", [])
    if not estacoes:
        print("Nenhuma estação encontrada.")
        return

    print("=" * 40)
    print("Lista de Estações:")
    for estacao in items:
        print(f"{estacao['codigoestacao']} - {estacao['Tipo_Estacao']} em {estacao['Municipio_Nome']}: {estacao['Estacao_Nome']}")
        
    print("=" * 40)
    print("\n")
    # print(estacoes)
    with open("output/estacoes/estacoes.txt", "w") as file:
        for estacao in items:
            file.write(f"{estacao['codigoestacao']} - {estacao['Tipo_Estacao']} em {estacao['Municipio_Nome']}: {estacao['Estacao_Nome']}\n")
    with open("output/estacoes/estacoes.json", "w") as file:
        file.write(estacoes.text)

def menu_acoes_estacoes(estacoes):
    limpar_terminal()
    print("=" * 40)
    print("Ações:")
    print(
        "1 - Gerar mapa com estações filtradas\n"
        "2 - Listar todas as estações\n"
        "3 - Ver coordenadas da estação específica\n"
        "4 - Ver detalhes da estação específica\n"
        "0 - Voltar\n"
    )
    print("=" * 40)
    print("\n")
    opcao = str(input("Digite a opção: "))
    match opcao:
        case "1":
            plotar_estacoes(estacoes)
        case "2":
            listar_estacoes(estacoes)
        case "3":
            codigo_estacao = str(input("Digite o código da estação: "))
            estacao = next((e for e in estacoes if e['codigoestacao'] == codigo_estacao), None)
            if estacao:
                get_estacao_coords(estacao)
            else:
                print("Estação não encontrada.")
        case "4":
            codigo_estacao = str(input("Digite o código da estação: "))
            estacao = next((e for e in estacoes if e['codigoestacao'] == codigo_estacao), None)
            if estacao:
                print(estacao)
            else:
                print("Estação não encontrada.")
        case "0":
            return
        case _:
            print("Opção inválida, tente novamente.")
            limpar_terminal()
    # listar_estacoes(token, filtros)


def menu_estacoes(token):
    codigo_estacao = 0
    while True:
        # estacao = resultado["items"][0]
        print("=" * 40)
        # print(f"\n{estacao['codigoestacao']} - Estação {estacao['Tipo_Estacao']} em {estacao['Municipio_Nome']}: {resultado['items'][0]['Estacao_Nome']}\n")
        print("O que deseja fazer?")
        print(
            "1 - Listar estações\n"
            "0 - Sair\n"
        )
        opcao = str(input("Digite a opção: "))
        match opcao:
            case "1":
                estacoes = menu_listar_estacoes(token)
                menu_acoes_estacoes(estacoes)
            case "0":
                break
            case _:
                print("Opção inválida, tente novamente.")
                continue
