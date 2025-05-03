from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import time
import json
import re

# Carregar os dados a partir dos arquivos JSON
with open("fii_crew/output/risk_analysis.txt", "r", encoding="utf-8") as analise:
    analise_texto = analise.read()

with open("fii_crew/output/dre_analysis.txt", "r", encoding="utf-8") as dre:
    dre_texto = dre.read()

# regex para pegar o conteúdo entre chaves
pattern = r"\{[^{}]*\}"

# Extrair e carregar o JSON do arquivo risk_analysis.txt
match_analise = re.search(pattern, analise_texto)
if match_analise:
    dicionario_json_analise = match_analise.group(0)
    dados_analise = json.loads(dicionario_json_analise)
else:
    raise ValueError("Nenhum dicionário JSON encontrado no texto de análise de risco.")

# Extrair e carregar o JSON do arquivo dre_analysis.txt
match_dre = re.search(pattern, dre_texto)
if match_dre:
    dicionario_json_dre = match_dre.group(0)
    dados_dre = json.loads(dicionario_json_dre)
else:
    raise ValueError("Nenhum dicionário JSON encontrado no texto de análise DRE.")

# Combinar os dois dicionários em um único
dados = {**dados_analise, **dados_dre}

# Adicionar data de análise nos dados
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
