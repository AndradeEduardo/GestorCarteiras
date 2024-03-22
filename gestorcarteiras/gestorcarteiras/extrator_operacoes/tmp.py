import os

# Defina o caminho para o diretório que você deseja listar
caminho_diretorio = "./Notas/BB"

# Lista todos os arquivos e diretórios no diretório especificado
conteudo_diretorio = os.listdir(caminho_diretorio)

# Filtra para obter apenas arquivos, excluindo diretórios
arquivos = [f"{caminho_diretorio}{arquivo}" for arquivo in conteudo_diretorio if os.path.isfile(os.path.join(caminho_diretorio, arquivo))]

print("Arquivos no diretório:", arquivos)
