import os
import requests
from dotenv import load_dotenv
from src.utils.utils import abrir_chrome, limpar_terminal
import gmplot


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def listar_estacoes(token: str):
    url = (
        "https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/"
        "HidroInventarioEstacoes/v1?C%C3%B3digo%20da%20Bacia=8"
    )
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

    # Filtra estações do rio 86001000
    latitudes = []
    longitudes = []
    for item in items:
        if item.get('Rio_Codigo') == "86001000":
            try:
                lat = float(item['Latitude'])
                lng = float(item['Longitude'])
                latitudes.append(lat)
                longitudes.append(lng)
            except (ValueError, TypeError):
                continue  # Ignora entradas inválidas

    if not latitudes or not longitudes:
        print("Nenhuma estação válida encontrada para o Rio 86001000.")
        return None

    # Cria o mapa centrado na primeira coordenada
    gmap = gmplot.GoogleMapPlotter(latitudes[0], longitudes[0], 10, apikey=GOOGLE_API_KEY)

    # Adiciona os marcadores
    gmap.scatter(latitudes, longitudes, color='red', size=40, marker=True)

    # Salva o mapa em um arquivo HTML
    mapa_path = "mapa_interativo.html"
    gmap.draw(mapa_path)
    print(f"Mapa gerado com sucesso: {mapa_path}")
    abrir_chrome(f"file://{os.path.abspath(mapa_path)}")
    return response_json


def get_estacao(codigo_estacao: str, token: str):
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
    else:
        print(f"Erro {response.status_code}: {response.text}")
        return None

def get_estacao_coords(estacao: dict):
    items = estacao["items"][0]
    print(f"\n{items['Latitude']} {items['Longitude']}\n")
    url = f"https://www.google.com/maps/search/?api=1&query={items['Latitude']},{items['Longitude']}"
    abrir_chrome(url)

def menu_estacoes(token):
    codigo_estacao = 0
    while True:
        # estacao = resultado["items"][0]
        print("=" * 40)
        # print(f"\n{estacao['codigoestacao']} - Estação {estacao['Tipo_Estacao']} em {estacao['Municipio_Nome']}: {resultado['items'][0]['Estacao_Nome']}\n")
        print("O que deseja fazer?")
        print(
            "1 - Ver estação específica\n"
            "2 - Listar estações em mapa\n"
            "3 - Próxima estação\n"
            "0 - Sair\n"
        )
        opcao = str(input("Digite a opção: "))
        match opcao:
            case "1":
                if codigo_estacao == 0:
                    codigo_estacao = str(input("Digite o código da estação: "))
                if codigo_estacao.lower() == "q":
                    break
                if not codigo_estacao.isdigit() or codigo_estacao is None or codigo_estacao == "":
                    codigo_estacao = 0
                    continue
                try:
                    resultado = get_estacao(codigo_estacao, token)
                    codigo_estacao = 0 
                    if resultado is None:
                        continue
                except Exception as e:
                    print(e)
                get_estacao_coords(resultado)
            case "2":
                listar_estacoes(token)
            case "0":
                break
            case _:
                print("Opção inválida, tente novamente.")
                continue
