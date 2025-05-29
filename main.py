from src.auth.token import auth, check_token
from src.services.estacao import menu_estacoes

if __name__ == '__main__':
    token = auth()
    while True:
        token = check_token(token)
        print("=" * 40)
        print("Módulos")
        print(
            "1 - Estações\n"
            "2 - Rios\n"
            "0 - Sair\n"
        )
        opcao = str(input("Digite a opção: "))
        match opcao:
            case "1":
                menu_estacoes(token)
            case "0":
                break
            case _:
                print("Opção inválida, tente novamente.")
                continue


