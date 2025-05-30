import os
import requests
from dotenv import load_dotenv
from src.utils.utils import abrir_chrome, limpar_terminal
import gmplot
from bs4 import BeautifulSoup


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
    estacoes = []
    for item in items:
        if item.get('Municipio_Codigo') == "24157000" and item.get("Operando") == "1":
            try:
                lat = float(item['Latitude'])
                lng = float(item['Longitude'])
                nome = item['codigoestacao']
                estacoes.append((lat, lng, nome))
            except (ValueError, TypeError):
                continue  # Ignora entradas inválidas

    gmap = gmplot.GoogleMapPlotter(estacoes[0][0], estacoes[0][1], 10, apikey=GOOGLE_API_KEY)

    for lat, lng, title in estacoes:
        gmap.marker(lat, lng, title=title, color='red')
        
    mapa_path = "html/index.html"
    gmap.draw(mapa_path)
    script_cru = '''
    setTimeout(function() {
        console.log('Mapa carregado');
        document.querySelectorAll('div[role="img"]').forEach(function(div) {
            div.addEventListener('click', function() {
                const title = div.getAttribute('title') || 'Sem título';
                navigator.clipboard.writeText(title).then(function() {
                    alert('Código da estação copiado: ' + title);
                }, function(err) {
                    console.error('Erro ao copiar: ', err);
                });
            });
        });
    }, 5000);
    '''
    with open(mapa_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    script_onclick = soup.new_tag('script', type='text/javascript')
    script_onclick.string = script_cru

    if soup.body:
        soup.body.append(script_onclick)
    else:
        print("A tag <body> não foi encontrada no arquivo HTML.")

    with open(mapa_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print(f"Mapa gerado com sucesso: {mapa_path}")
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
