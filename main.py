from src.auth.token import auth, check_token
from src.services.estacao import menu_estacoes
from src.services.corpos_agua import menu_aguas
from src.utils.utils import limpar_terminal

def main():
    token = auth()
    while True:
        limpar_terminal()
        token = check_token(token)
        print("=" * 40)
        print("Módulos")
        print(
            "1 - Estações\n"
            "2 - Aguas\n"
            "0 - Sair\n"
        )
        opcao = str(input("Digite a opção: "))
        match opcao:
            case "1":
                menu_estacoes(token)
            case "2":
                menu_aguas(token)
            case "0":
                break
            case _:
                print("Opção inválida, tente novamente.")
                continue


if __name__ == '__main__':
    main()


