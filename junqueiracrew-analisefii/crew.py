from crewai import Agent, Crew, Process, Task
from crewai.llm import LLM
from crewai.project import CrewBase, agent, crew, task, after_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import re
import time
import json
import os
from dotenv import load_dotenv


# Define o Crew para os especialistas de Risco, DRE e CSV
@CrewBase
class FundoImobiliarioCrew:
    @after_kickoff
    def render_pdf(self, input):
        """Função para renderizar o PDF com os dados extraídos"""
        # Carregar os dados a partir dos arquivos JSON
        with open("output/risk_analysis.txt", "r", encoding="utf-8") as analise:
            analise_texto = analise.read()

        with open("output/dre_analysis.txt", "r", encoding="utf-8") as dre:
            dre_texto = dre.read()

        # Regex para pegar o conteúdo entre chaves
        pattern = r"\{[^{}]*\}"

        # Extrair e carregar o JSON do arquivo risk_analysis.txt
        match_analise = re.search(pattern, analise_texto)
        if match_analise:
            dados_analise = json.loads(match_analise.group(0))
        else:
            raise ValueError(
                "Nenhum dicionário JSON encontrado no texto de análise de risco."
            )

        def formatar_como_dinheiro(valor: float) -> str:
            return (
                f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
            )

        def formatar_como_quantidade(valor: float) -> str:
            return f"{int(round(valor)):,}".replace(",", ".")

        # Extrair e carregar o JSON do arquivo dre_analysis.txt
        match_dre = re.search(pattern, dre_texto)
        if match_dre:
            dados_dre = json.loads(match_dre.group(0))
        else:
            raise ValueError(
                "Nenhum dicionário JSON encontrado no texto de análise DRE."
            )

        # Campos monetários
        campos_dinheiro = [
            "receita_total_locacao",
            "receita_outras",
            "despesas_operacionais",
            "despesas_administrativas",
            "resultado_operacional",
            "receitas_financeiras",
            "despesas_financeiras",
            "resultado_financeiro_liquido",
            "lucro_liquido_contabil",
            "resultado_caixa_distribuivel",
            "rendimentos_distribuidos",
        ]

        # Campos de quantidade
        campos_quantidade = [
            "quantidade_cotas",
        ]

        # Formatar os campos de dinheiro
        for campo in campos_dinheiro:
            if campo in dados_dre and isinstance(dados_dre[campo], (int, float)):
                dados_dre[campo] = formatar_como_dinheiro(dados_dre[campo])

        # Formatar os campos de quantidade
        for campo in campos_quantidade:
            if campo in dados_dre and isinstance(dados_dre[campo], (int, float)):
                dados_dre[campo] = formatar_como_quantidade(dados_dre[campo])

        # Formatar rendimento por cota separadamente se for numérico
        if "rendimento_por_cota" in dados_dre and isinstance(
            dados_dre["rendimento_por_cota"], (int, float)
        ):
            dados_dre["rendimento_por_cota"] = formatar_como_dinheiro(
                dados_dre["rendimento_por_cota"]
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

        # Criar diretório de saída se não existir
        output_dir = "output"
        diretorios = os.listdir(".")
        if "output" not in diretorios:
            os.mkdir(output_dir, exist_ok=True)

        pdf_path = f"{output_dir}/relatorio_final.pdf"

        HTML(string=html_content).write_pdf(pdf_path)

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def risk_specialist(self) -> Agent:
        load_dotenv(".env")  # Carrega as variáveis de ambiente do arquivo .env
        return Agent(
            config=self.agents_config["risk_specialist"],  # Usando o YAML configurado
            verbose=True,
            llm=LLM(
                provider="google",
                model="gemini-2.0-flash-001",
                api_key=os.getenv("GEMINI_API_KEY"),
            ),
        )

    @agent
    def dre_specialist(self) -> Agent:
        load_dotenv(".env")  # Carrega as variáveis de ambiente do arquivo .en
        return Agent(
            config=self.agents_config["dre_specialist"],  # Usando o YAML configurado
            verbose=True,
            llm=LLM(
                provider="google",
                model="gemini-2.0-flash-001",
                api_key=os.getenv("GEMINI_API_KEY"),
            ),
        )

    @agent
    def csv_builder(self) -> Agent:
        load_dotenv(".env")  # Carrega as variáveis de ambiente do arquivo .env
        return Agent(
            config=self.agents_config["csv_builder"],  # Usando o YAML configurado
            verbose=True,
            llm=LLM(
                provider="google",
                model="gemini-2.0-flash-001",
                api_key=os.getenv("GEMINI_API_KEY"),
            ),
        )

    @task
    def risk_analysis_task(self) -> Task:
        load_dotenv(".env")  # Carrega as variáveis de ambiente do arquivo .env
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
