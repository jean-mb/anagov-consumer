import os
import subprocess

def limpar_terminal():
    os.system('clear')

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