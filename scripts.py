import subprocess
def run(STRING):
    comando = STRING.split()

    # Executar o comando do Scrapy
    resultado = subprocess.run(comando, capture_output=True, text=True)