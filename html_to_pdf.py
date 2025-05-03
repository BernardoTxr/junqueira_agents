from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import time
import json
import re

# Carregar os dados a partir do arquivo JSON
with open("fii_crew/output/risk_analysis.txt", "r", encoding="utf-8") as analise:
    analise_texto = analise.read()

# regex para pegar o conteúdo entre chaves
pattern = r"\{[^{}]*\}"
match = re.search(pattern, analise_texto)
print(match)
if match:
    dicionario_json = match.group(0)
    dados = json.loads(dicionario_json)
else:
    raise ValueError("Nenhum dicionário JSON encontrado no texto.")

# Adicione data de análise nos dados
dados["data_analise"] = time.strftime("%d/%m/%Y")

# Carregar o template HTML
env = Environment(loader=FileSystemLoader("."))
template = env.get_template("template.html")

# Renderizar o template com os dados
html_content = template.render(dados)

# Gerar o PDF com WeasyPrint
pdf = HTML(string=html_content).write_pdf()

# Salvar o PDF gerado
with open("relatorio_fundo_imobiliario.pdf", "wb") as f:
    f.write(pdf)

print("Relatório PDF gerado com sucesso!")
