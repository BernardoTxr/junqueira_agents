#!/usr/bin/env python
# src/latest_ai_development/main.py
import sys
from fii_crew.crew import FundoImobiliarioCrew


def run():
    """
    Run the crew.
    """
    # carregue o relatório texto_extraido.txt
    with open("texto_extraido.txt", "r", encoding="utf-8") as arquivo:
        texto = arquivo.read()
    FundoImobiliarioCrew().crew().kickoff(inputs={"relatorio": texto})
