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
        "Código da Bacia",
        "Unidade Federativa",
        "Código da Estação",
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
    estacao
    print(f"\n{estacao['Latitude']} {estacao['Longitude']}\n")
    url = f"https://www.google.com/maps/search/?api=1&query={estacao['Latitude']},{estacao['Longitude']}"
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
    print(filtros)
    return get_estacoes(token, filtros)
    
def listar_estacoes(estacoes, estacoes_filtradas):
    items = estacoes_filtradas
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
            file.write(f"{estacao['codigoestacao']} - {estacao['Tipo_Estacao']} em {estacao['Municipio_Nome']}: {estacao['Estacao_Nome']} -> {estacao['Latitude']},{estacao['Longitude']}\n")
    with open("output/estacoes/estacoes.json", "w") as file:
        file.write(estacoes.text)
    with open("output/estacoes/estacoes.csv", "w") as file:
        for key in items[0].keys():
            file.write(f"{key},")
        file.write("\n")
        for estacao in items:
            for valor in estacao.values():
                file.write(f"{valor},")
            file.write("\n")

def filtrar_estacoes(estacoes):
    estacoes_filtradas = []
    filtros = {
        1: ("codigobacia", None),
        2: ("Tipo_Estacao", None),
        3: ("Sub_Bacia_Nome", None),
        4: ("Sub_Bacia_Codigo", None),
        5: ("Rio_Nome", None),
        6: ("Rio_Codigo", None),
        7: ("Municipio_Nome", None),
        8: ("Municipio_Codigo", None),
        9: ("Bacia_Nome", None),
        10: ("Operando", "1")
    }   
    print("Filtros disponíveis:")
    for key, (field, _) in filtros.items():
        print(f"{key} - {field.replace('_', ' ').title()}")
    print("0 - Voltar")
    while True:
        valor = None
        opcao = input("Escolha um filtro (ou 0 para voltar): ")
        if opcao == "0":
            return estacoes
        if opcao == "2":
            print("\nTipos de Estação:")
            print("1 - Pluviométrica")
            print("2 - Fluviométrica")
            tipo_estacao = input("Digite o tipo de estação (ou deixe em branco para ignorar): ")
            if tipo_estacao:
                valor = "Pluviometrica" if tipo_estacao == "1" else "Fluviometrica" if tipo_estacao == "2" else None
            else:
                print("Filtro ignorado.")
        if opcao.isdigit() and int(opcao) in filtros:
            field, _ = filtros[int(opcao)]
            if valor is None:
                valor = input(f"Digite o valor para {field.replace('_', ' ').title()} (ou deixe em branco para ignorar): ")
            if valor:
                for estacao in estacoes:
                    if field in estacao and valor in estacao[field]:
                        estacoes_filtradas.append(estacao)

                return estacoes_filtradas
            else:
                print("Filtro ignorado.")
        else:
            print("Opção inválida, tente novamente.")

def menu_acoes_estacoes(estacoes):
    estacoes_json = estacoes.json()
    estacoes_filtradas = estacoes_json.get("items", [])
    while True:
        # limpar_terminal()
        print("=" * 40)
        print("Ações:")
        print(
            "1 - Gerar mapa com estações filtradas\n"
            "2 - Listar todas as estações\n"
            "3 - Ver coordenadas da estação específica\n"
            "4 - Ver detalhes da estação específica\n"
            "5 - Filtrar estações\n"
            "0 - Voltar\n"
        )
        print("=" * 40)
        print("\n")
        opcao = str(input("Digite a opção: "))
        match opcao:
            case "1":
                mostrar_todas = str(input("Deseja mostrar todas as estações? (s/n): ")).lower() == "s"
                raio=0
                if mostrar_todas:
                    raio = str(input("Digite o raio em km para buscar estações próximas (deixe em branco para não filtrar): "))
                    raio = float(raio) if raio else 0
                plotar_estacoes(estacoes_filtradas, estacoes.json().get("items", []), mostrar_todas, raio)
            case "2":
                listar_estacoes(estacoes, estacoes_filtradas)
            case "3":
                codigo_estacao = str(input("Digite o código da estação: "))
                estacao = next((e for e in estacoes_filtradas if e['codigoestacao'] == codigo_estacao), None)
                if estacao:
                    get_estacao_coords(estacao)
                else:
                    print("Estação não encontrada.")
            case "4":
                codigo_estacao = str(input("Digite o código da estação: "))
                estacao = next((e for e in estacoes_filtradas if e['codigoestacao'] == codigo_estacao), None)
                if estacao:
                    print(estacao)
                    with open("output/estacoes/estacao_detalhes.json", "w") as file:
                        file.write(str(estacao))
                else:
                    print("Estação não encontrada.")
            case "5":
                estacoes_filtradas = filtrar_estacoes(estacoes_filtradas)
            case "0":
                return
            case _:
                print("Opção inválida, tente novamente.")
                limpar_terminal()
        # listar_estacoes(token, filtros)


def menu_estacoes(token):
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
