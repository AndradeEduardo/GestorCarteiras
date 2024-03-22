from PyPDF2 import PdfReader
import re
import pandas as pd

# Caminho do arquivo PDF
pdf_path = 'NotaCorretagem_BTG_2023-07-23.pdf'

# Inicializando o leitor de PDF
reader = PdfReader(pdf_path)

# Lendo todas as páginas do PDF e concatenando o texto
full_text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

print(full_text)

# Expressões regulares para capturar os dados desejados
pregao_date_regex = re.compile(r"Data pregão\n(\d{2}/\d{2}/\d{4})")
nota_number_regex = re.compile(r"Nr\. nota\n(\d+)")
business_regex = re.compile(r"(C|V)\s+VISTA\s+([\w\d]+)\s+[\w\d.]*\s+[\d.]+\s+([\d.]+)", re.MULTILINE)

# Encontrando a data do pregão e o número da nota
pregao_date = pregao_date_regex.search(full_text).group(1)
nota_number = nota_number_regex.search(full_text).group(1)

# Lista para armazenar os negócios extraídos
negocios_realizados = []

# Encontrando e adicionando os negócios à lista
for match in business_regex.finditer(full_text):
    cv, titulo, preco = match.groups()
    negocio = {
        "C/V": cv,
        "Especificação do título": titulo,
        "Preço": float(preco),
        "Data pregão": pregao_date,
        "Nr. nota": int(nota_number)
    }
    negocios_realizados.append(negocio)

# Convertendo a lista de negócios em um DataFrame
df_negocios = pd.DataFrame(negocios_realizados)

df_negocios
