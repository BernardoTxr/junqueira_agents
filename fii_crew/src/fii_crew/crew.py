from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


# Define o Crew para os especialistas de Risco, DRE e CSV
@CrewBase
class FundoImobiliarioCrew:
    """Fundo Imobiliário crew"""

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
            output_file="output/dre_analysis.md",  # O relatório de DRE será salvo aqui
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
