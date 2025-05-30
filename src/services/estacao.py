import requests
from src.utils.utils import abrir_chrome, limpar_terminal



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

        estacao = resultado["items"][0]
        print("=" * 40)
        print(f"\n{estacao['codigoestacao']} - Estação {estacao['Tipo_Estacao']} em {estacao['Municipio_Nome']}: {resultado['items'][0]['Estacao_Nome']}\n")
        print("O que deseja fazer?")
        print(
            "1 - Ver coordenadas da estação\n"
            "2 - Ver dados da estação\n"
            "3 - Próxima estação\n"
            "0 - Sair\n"
        )
        opcao = str(input("Digite a opção: "))
        match opcao:
            case "1":
                get_estacao_coords(resultado)
            case "0":
                break
            case _:
                print("Opção inválida, tente novamente.")
                continue
