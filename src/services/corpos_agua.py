import requests

from src.utils.utils import limpar_terminal

def listar_rios(token: str):
    url = "https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/HidroRio/v1"
    headers = {
        "accept": "*/*",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        if len(response_json["items"]) != 0:
            with open("output/rios/rios.txt", "w") as file:
                for item in response_json["items"]:
                    file.write(f"{item['codigorio']} - {item['Nome_Rio']}\n")
            with open("output/rios/rios.json", "w") as file:
                file.write(response.text)
            with open("output/rios/rios.csv", "w") as file:
                for key in response_json["items"][0].keys():
                    file.write(f"{key},")
                file.write("\n")
                for rio in response_json["items"]:
                    for valor in rio.values():
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

def listar_bacias(token: str):
    url = "https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/HidroBacia/v1"
    headers = {
        "accept": "*/*",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        if len(response_json["items"]) != 0:
            with open("output/bacias/bacias.txt", "w") as file:
                for item in response_json["items"]:
                    file.write(f"{item['codigobacia']} - {item['Nome_Bacia']}\n")
            with open("output/bacias/bacias.json", "w") as file:
                file.write(response.text)
            with open("output/bacias/bacias.csv", "w") as file:
                for key in response_json["items"][0].keys():
                    file.write(f"{key},")
                file.write("\n")
                for bacia in response_json["items"]:
                    for valor in bacia.values():
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

def listar_subbacias(token: str):
    url = "https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/HidroSubBacia/v1"
    headers = {
        "accept": "*/*",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        if len(response_json["items"]) != 0:
            with open("output/sub-bacias/sub-bacias.txt", "w") as file:
                for item in response_json["items"]:
                    file.write(f"{item['codigosubbacia']} - {item['Sub_Bacia_Nome']}\n")
            with open("output/sub-bacias/sub-bacias.json", "w") as file:
                file.write(response.text)
            with open("output/sub-bacias/sub-bacias.csv", "w") as file:
                for key in response_json["items"][0].keys():
                    file.write(f"{key},")
                file.write("\n")
                for sub in response_json["items"]:
                    for valor in sub.values():
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

def menu_aguas(token):
    while True:
        print("=" * 40)
        print("Módulo Aguas")
        print(
            "1 - Listar rios\n"
            "2 - Listar bacias\n"
            "3 - Listar sub-bacias\n"
            "0 - Sair\n"
        )
        opcao = str(input("Digite a opção: "))
        match opcao:
            case "1":
                listar_rios(token)
            case "2":
                listar_bacias(token)
            case "3":
                listar_subbacias(token)
            case "0":
                break
            case _:
                print("Opção inválida, tente novamente.")
                limpar_terminal()
                continue