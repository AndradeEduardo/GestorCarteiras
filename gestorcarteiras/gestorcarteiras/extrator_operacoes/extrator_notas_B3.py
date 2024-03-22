import pandas as pd
import io
from correpy.parsers.brokerage_notes.b3_parser.b3_parser import B3Parser
from correpy.parsers.brokerage_notes.b3_parser.nuinvest import NunInvestParser
import correpy
import os

# Defina o caminho para o diretório que você deseja listar
diretorio = "./Notas/BTG"

# Lista todos os arquivos e diretórios no diretório especificado
arquivos = os.listdir(diretorio)

# Filtrando para manter apenas os arquivos PDF
arquivos_pdf = [arquivo for arquivo in arquivos if arquivo.endswith('.pdf')]



# Filtra para obter apenas arquivos, excluindo diretórios
caminhos = [f"{diretorio}/{arquivo}" for arquivo in arquivos_pdf if os.path.isfile(os.path.join(diretorio, arquivo))]

print(caminhos)

conteudo = io.BytesIO()

brokerage_notes = []

for arquivo in caminhos:
    print(f"Lendo o arquivo: {arquivo}")
    with open(arquivo, 'rb') as arquivo:
        conteudo_arq = arquivo.read()
        conteudo.write(conteudo_arq)
        notas = B3Parser(brokerage_note=conteudo, password="password").parse_brokerage_note()
        for nota in notas:
            brokerage_notes.append(nota)

conteudo.seek(0)
        
transacoes = []

print(f"{len(brokerage_notes)} notas de corretagem parseadas")

for nota_corretagem in brokerage_notes:            
    print(f"Nota: {nota_corretagem.reference_id}; Data: {nota_corretagem.reference_date}")
    for transacao in nota_corretagem.transactions:        
        transacoes.append(transacao)
        print(f"{transacao.transaction_type}; {transacao.security.ticker}; {transacao.unit_price}")

print(f"{len(transacoes)} transacões encontradas")

#print(brokerage_notes)

