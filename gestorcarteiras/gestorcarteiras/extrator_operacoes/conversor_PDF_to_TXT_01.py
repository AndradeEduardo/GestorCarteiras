import PyPDF2
import re
import pandas as pd
import os
import fitz

def extrair_texto_pdf(caminho_arquivo):
    texto = ""
    with open(caminho_arquivo, 'rb') as arquivo:
        leitor_pdf = PyPDF2.PdfReader(arquivo)
        for pagina in range(len(leitor_pdf.pages)):
            texto_pagina = leitor_pdf.pages[pagina].extract_text()
            if texto_pagina:  # Verifica se conseguiu extrair texto
                texto += texto_pagina
    
    return texto

def extrair_texto_pdf_fitz(caminho_do_arquivo):
    # Abrindo o arquivo PDF
    documento = fitz.open(caminho_do_arquivo)
    
    texto = ''
    # Iterando sobre cada página do PDF
    for pagina in documento:
        # Extraindo o texto da página
        texto += pagina.get_text()
    
    # Fechando o documento
    documento.close()
    
    return texto

def extrair_dados(conteudo_texto):
    
    padrao_para_remover = r"\b(?:ON|PN|PNA|PNB|UNT)\b"
    conteudo_texto = re.sub(padrao_para_remover, "", conteudo_texto)

    print(f"""*****************************************
          {conteudo_texto}
    
""")
    
    
    nr_nota_regex = r"(\d+) Nr\. nota"
    data_pregao_regex = r"(\d{2}/\d{2}/\d{4}) Data pregão"
    nr_nota = re.search(nr_nota_regex, conteudo_texto).group(1)
    data_pregao = re.search(data_pregao_regex, conteudo_texto).group(1)

    # Encontra os negócios realizados e extrai as informações necessárias usando a expressão regular corrigida
    negocios_realizados_regex = r"Negócios realizados(.+?)Resumo dos Negócios"
    negocios_realizados_texto = re.search(negocios_realizados_regex, conteudo_texto, re.DOTALL).group(1)
    #padrao = r"CVISTA\s+([A-Z0-9]+)\s+(ON|PN|)?\s+(\d+)\s+([\d,\.]+)"
    padrao = r"(\d+-BOVESPA)\s+(C|V)VISTA\s+([A-Z|d]{4}\d{1,2}[F]?)\s+(ON|PN|PNA|PNB)?\s*(\d+)\s+(\d+,\d+)\s+(\d+,\d+)\sD"
    padrao = r"(\d+-BOVESPA)\s+(C|V)VISTA\s+([A-Z|0-9]{4}\d{1,2}[F]?)\s+(ON|PN|PNA|PNB)?\s*(\d+)\s+(\d{1,3}(?:\.\d{3})*(?:,\d{2}))\s+(\d{1,3}(?:\.\d{3})*(?:,\d{2}))\s[D|C]"
    padrao_numeros = r"\d{1,3}(?:\.\d{3})*(?:,\d{2})"
    linhas_negocios = re.findall(
        padrao,
        negocios_realizados_texto
    )

    
    # Estrutura para armazenar os dados extraídos
    dados_negocios = []

    for _, operacao, ticker, _, quantidade, preco, _ in linhas_negocios:
        operacao = 'Compra' if operacao == 'C' else 'Venda'
        quantidade = int(quantidade)
        preco = preco.replace(',', '.')
        dados_negocios.append((nr_nota, data_pregao, ticker, operacao, quantidade, preco))

    print(f"{len(dados_negocios)} negociações em {data_pregao}:") 
    print(dados_negocios)
    print(f"*****************************\n\n")

    return dados_negocios
    
# Defina o caminho para o diretório que você deseja listar
caminho_diretorio = "./Notas/BB"

arquivos_pdf = []

    # Listando todos os arquivos e diretórios no caminho especificado
for arquivo in os.listdir(caminho_diretorio):
    # Verificando se o item é um arquivo PDF
    if arquivo.lower().endswith('.pdf'):
        arquivos_pdf.append(arquivo)


# Lista todos os arquivos e diretórios no diretório especificado
# conteudo_diretorio = os.listdir(caminho_diretorio)

# Filtra para obter apenas arquivos, excluindo diretórios
caminhos = [f"{caminho_diretorio}/{arquivo}" for arquivo in arquivos_pdf if os.path.isfile(os.path.join(caminho_diretorio, arquivo))]

# Caminhos dos arquivos PDF
# caminhos = [
#     f"{caminho_diretorio}/XPINC_NOTA_NEGOCIACAO_B3_1_2023.pdf",    
# ]

dados_totais = []
for caminho in caminhos:
    texto_pdf = extrair_texto_pdf(caminho)
    # Separando o nome do arquivo de sua extensão
    nome_base, extensao = caminho.rsplit('.', 1)

    # Alterando a extensão do arquivo para .txt
    nome_arquivo_txt = nome_base + '_PyPDF2' + '.txt'
    with open(f"{nome_arquivo_txt}", 'w') as arquivo:
        # Gravando a string no arquivo
        arquivo.write(texto_pdf)
        print(f"arquivo {nome_arquivo_txt} gravado.")
    # dados = extrair_dados(texto_pdf)
    # dados_totais.extend(dados)

# Cria DataFrame
# df_negocios = pd.DataFrame(dados_totais)

# # Mostra o DataFrame
# print(df_negocios)
