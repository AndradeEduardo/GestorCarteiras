import re
import pandas as pd

# Carrega o conteúdo do arquivo de texto
caminho_arquivo = 'conteudo_pdf_NC_BTG.txt'
with open(caminho_arquivo, 'r') as arquivo:
    conteudo_texto = arquivo.read()

# Encontra o número da nota e a data do pregão
# nr_nota_regex = r"(\d+) Nr\. nota"
# data_pregao_regex = r"(\d{2}/\d{2}/\d{4}) Data pregão"
# nr_nota = re.search(nr_nota_regex, conteudo_texto).group(1)
# data_pregao = re.search(data_pregao_regex, conteudo_texto).group(1)

# # # Usa expressões regulares para encontrar as linhas individuais dos negócios realizados
# # linhas_negocios = re.findall(
# #     r"\d+-BOVESPA (C|V)VISTA\s+([A-Z]{4}\d{1,2}[F]?)\s+(ON|PN)?\s*(\d+)\s+(\d+,\d+)\s+(\d+,\d+)",
# #     conteudo_texto
# # )

# # print(linhas_negocios)

# # # Estrutura para armazenar os dados extraídos
# # dados_negocios = []

# # for operacao, ticker, _, quantidade, preco, _ in linhas_negocios:
# #     operacao = 'Compra' if operacao == 'C' else 'Venda'
# #     quantidade = int(quantidade)
# #     preco = float(preco.replace(',', '.'))
# #     dados_negocios.append((nr_nota, data_pregao, ticker, operacao, quantidade, preco))

# # # Cria um DataFrame com as novas informações extraídas
# # df_negocios_atualizado = pd.DataFrame(
# #     dados_negocios,
# #     columns=['Nr. Nota', 'Data', 'Ticker', 'Operação', 'Quantidade', 'Preço']
# # )


# # print(df_negocios_atualizado)

# # Encontra os negócios realizados e extrai as informações necessárias
# negocios_realizados_regex = r"Negócios realizados(.+?)Resumo dos Negócios"
# negocios_realizados_texto = re.search(negocios_realizados_regex, conteudo_texto, re.DOTALL).group(1)
# linhas_negocios = re.findall(
#     r"\d+-BOVESPA (C|V)VISTA\s+([A-Z]{4}\d{1,2}[F]?)\s+(ON|PN)?\s*(\d+)\s+(\d+,\d+)\s+(\d+,\d+)",
#     negocios_realizados_texto
# )

# # Estrutura para armazenar os dados extraídos
# dados_negocios = []

# for operacao, ticker, _, quantidade, preco, _ in linhas_negocios:
#     operacao = 'Compra' if operacao == 'C' else 'Venda'  # Correção aqui
#     quantidade = int(quantidade)
#     preco = float(preco.replace(',', '.'))
#     dados_negocios.append((nr_nota, data_pregao, ticker, operacao, quantidade, preco))

# # Cria um DataFrame com as novas informações extraídas
# df_negocios_atualizado = pd.DataFrame(
#     dados_negocios,
#     columns=['Nr. Nota', 'Data', 'Ticker', 'Operação', 'Quantidade', 'Preço']
# )

# print(df_negocios_atualizado)
    
# Encontra o número da nota e a data do pregão
nr_nota_regex = r"(\d+) Nr\. nota"
data_pregao_regex = r"(\d{2}/\d{2}/\d{4}) Data pregão"
nr_nota = re.search(nr_nota_regex, conteudo_texto).group(1)
data_pregao = re.search(data_pregao_regex, conteudo_texto).group(1)

# Encontra os negócios realizados e extrai as informações necessárias usando a expressão regular corrigida
negocios_realizados_regex = r"Negócios realizados(.+?)Resumo dos Negócios"
negocios_realizados_texto = re.search(negocios_realizados_regex, conteudo_texto, re.DOTALL).group(1)
linhas_negocios = re.findall(
    r"(\d+-BOVESPA)\s+(C|V)VISTA\s+([A-Z]{4}\d{1,2}[F]?)\s+(ON|PN)?\s*(\d+)\s+(\d+,\d+)\s+(\d+,\d+)",
    negocios_realizados_texto
)

print(linhas_negocios)

# Estrutura para armazenar os dados extraídos
dados_negocios = []

for _, operacao, ticker, _, quantidade, preco, _ in linhas_negocios:
    operacao = 'Compra' if operacao == 'C' else 'Venda'
    quantidade = int(quantidade)
    preco = preco.replace(',', '.')
    dados_negocios.append((nr_nota, data_pregao, ticker, operacao, quantidade, preco))


# Cria um DataFrame com as novas informações extraídas
df_negocios_atualizado = pd.DataFrame(
    dados_negocios,
    columns=['Nr. Nota', 'Data', 'Ticker', 'Operação', 'Quantidade', 'Preço']
)

print(df_negocios_atualizado)