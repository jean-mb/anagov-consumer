import subprocess

def limpar_terminal():
    subprocess.run(['clear'])
    

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

def criar_diretorios():
    import os

    directories = [
        "output",
        "html",
        "output/municipios",
        "output/estados",
        "output/rios",
        "output/bacias",
        "output/sub-bacias",
        "output/estacoes"
    ]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Diretório {directory} criado.")
        else:
            print(f"Diretório {directory} já existe.")