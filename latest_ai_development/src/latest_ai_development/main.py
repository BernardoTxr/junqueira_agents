#!/usr/bin/env python
# src/latest_ai_development/main.py
import sys
from latest_ai_development.crew import FundoImobiliarioCrew


def run():
    """
    Run the crew.
    """
    # carregue o relatório texto_extraido.txt
    with open("texto_extraido.txt", "r", encoding="utf-8") as arquivo:
        texto = arquivo.read()
    inputs = {"relatorio": texto}
    FundoImobiliarioCrew().crew().kickoff(inputs=inputs)
