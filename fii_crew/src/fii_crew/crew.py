from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from docling.document_converter import DocumentConverter
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import re
import time
import json

source = "download1 KNRI11.pdf"  # document per local path or URL


# Define o Crew para os especialistas de Risco, DRE e CSV
@CrewBase
class FundoImobiliarioCrew:

    @before_kickoff
    def parse_pdf(self, source: str):
        """Função para fazer o parse do PDF e extrair os dados necessários"""
        converter = DocumentConverter()
        result = converter.convert(source)
        markdown_text = result.document.export_to_markdown()

        with open("texto_extraido.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(markdown_text)

    @after_kickoff
    def render_pdf(self):
        """Função para renderizar o PDF com os dados extraídos"""
        # Carregar os dados a partir dos arquivos JSON
        with open("output/risk_analysis.txt", "r", encoding="utf-8") as analise:
            analise_texto = analise.read()

        with open("output/dre_analysis.txt", "r", encoding="utf-8") as dre:
            dre_texto = dre.read()

        # regex para pegar o conteúdo entre chaves
        pattern = r"\{[^{}]*\}"

        # Extrair e carregar o JSON do arquivo risk_analysis.txt
        match_analise = re.search(pattern, analise_texto)
        if match_analise:
            dicionario_json_analise = match_analise.group(0)
            dados_analise = json.loads(dicionario_json_analise)
        else:
            raise ValueError(
                "Nenhum dicionário JSON encontrado no texto de análise de risco."
            )

        # Extrair e carregar o JSON do arquivo dre_analysis.txt
        match_dre = re.search(pattern, dre_texto)
        if match_dre:
            dicionario_json_dre = match_dre.group(0)
            dados_dre = json.loads(dicionario_json_dre)
        else:
            raise ValueError(
                "Nenhum dicionário JSON encontrado no texto de análise DRE."
            )

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
        with open("output/relatorio_fundo_imobiliario.pdf", "wb") as f:
            f.write(pdf)

        print("Relatório PDF gerado com sucesso!")

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def risk_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["risk_specialist"],  # Usando o YAML configurado
            verbose=True,
        )

    @agent
    def dre_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["dre_specialist"],  # Usando o YAML configurado
            verbose=True,
        )

    @agent
    def csv_builder(self) -> Agent:
        return Agent(
            config=self.agents_config["csv_builder"],  # Usando o YAML configurado
            verbose=True,
        )

    @task
    def risk_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config[
                "risk_analysis_task"
            ],  # Configuração da task de análise de risco
            output_file="output/risk_analysis.txt",  # O relatório de riscos será salvo aqui
        )

    @task
    def dre_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config[
                "dre_analysis_task"
            ],  # Configuração da task de análise de DRE
            output_file="output/dre_analysis.txt",  # O relatório de DRE será salvo aqui
        )

    @task
    def csv_structuring_task(self) -> Task:
        return Task(
            config=self.tasks_config[
                "csv_structuring_task"
            ],  # Configuração da task de geração de CSV
            output_file="output/data_report.csv",  # O arquivo CSV gerado será salvo aqui
        )

    @crew
    def crew(self) -> Crew:
        """Cria o Crew para os agentes e tasks definidos"""
        return Crew(
            agents=self.agents,  # Agentes definidos com a função @agent
            tasks=self.tasks,  # Tasks definidas com a função @task
            process=Process.sequential,  # O processo será sequencial
            verbose=True,
        )
