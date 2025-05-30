import requests

from src.utils.utils import limpar_terminal

def listar_municipios(token: str):
    url = "https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/HidroMunicipio/v1"
    headers = {
        "accept": "*/*",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        if len(response_json["items"]) != 0:
            with open("output/municipios/municipios.txt", "w") as file:
                for item in response_json["items"]:
                    file.write(f"{item['codigomunicipio']} - {item['Municipio_Nome']} - Estado: {item['Estado_Codigo']}\n")
            with open("output/municipios/municipios.json", "w") as file:
                file.write(response.text)

            with open("output/municipios/municipios.csv", "w") as file:
                for key in response_json["items"][0].keys():
                    file.write(f"{key},")
                file.write("\n")
                for municipio in response_json["items"]:
                    for valor in municipio.values():
                        valor = str(valor).replace(",", "-")  
                        file.write(f"{valor},")
                    file.write("\n")
            return response.json()
        else:
            print(response_json["message"])
            return None
    else:
        print(f"Erro {response.status_code}: {response.text}")
        return None

def listar_estados(token: str):
    url = "https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/HidroUF/v1"
    headers = {
        "accept": "*/*",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        if len(response_json["items"]) != 0:
            with open("output/estados/estados.txt", "w") as file:
                for item in response_json["items"]:
                    file.write(f"{item['codigouf']} - {item['Estado_Sigla']} - {item['Estado_Nome']}\n")
            with open("output/estados/estados.json", "w") as file:
                file.write(response.text)
            with open("output/estados/estados.csv", "w") as file:
                for key in response_json["items"][0].keys():
                    file.write(f"{key},")
                file.write("\n")
                for estado in response_json["items"]:
                    for valor in estado.values():
                        valor = str(valor).replace(",", "-")  
                        file.write(f"{valor},")
                    file.write("\n")

            return response.json()
        else:
            print(response_json["message"])
            return None
    else:
        print(f"Erro {response.status_code}: {response.text}")
        return None

def menu_localidades(token):
    while True:
        print("=" * 40)
        print("Módulo Localidades")
        print(
            "1 - Listar municipios\n"
            "2 - Listar estados\n"
            "0 - Sair\n"
        )
        opcao = str(input("Digite a opção: "))
        match opcao:
            case "1":
                listar_municipios(token)
            case "2":
                listar_estados(token)
            case "0":
                break
            case _:
                print("Opção inválida, tente novamente.")
                limpar_terminal()
                continue