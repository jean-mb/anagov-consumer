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