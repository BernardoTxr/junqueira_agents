from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from crew import FundoImobiliarioCrew
import base64
import pandas as pd
import logging
import sys
import os
import csv

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    logger.info("Health check endpoint accessed")
    return "OK", 200


@app.post("/processar")
async def processar(payload: Request):
    try:
        logger.info("Iniciando processamento...")

        json_request = await payload.json()
        logger.debug(f"Payload recebido: {json_request}")

        textos = json_request.get("message", [])
        filenames = json_request.get("filenames", [])
        logger.info(f"Processando {len(textos)} textos e {len(filenames)} arquivos")

        arquivos_base64 = {}
        for filename, texto in zip(filenames, textos):
            # Executa o crew
            logger.debug("Iniciando FundoImobiliarioCrew...")
            FundoImobiliarioCrew().crew().kickoff(inputs={"relatorio": texto})
            logger.info("Crew executado com sucesso")

            # Processa CSVs
            try:
                df1 = pd.read_csv("output/data_report.csv")
                df2 = pd.read_csv("output/data_report_final.csv")
                df_final = pd.concat([df1, df2], ignore_index=True)
                df_final.to_csv("output/data_report_final.csv", index=False)
                logger.debug("CSVs mesclados com sucesso")
            except Exception as e:
                logger.error(f"Erro ao mesclar CSVs: {str(e)}")
                raise

            try:
                with open("output/relatorio_final.pdf", "rb") as f:
                    encoded = base64.b64encode(f.read()).decode("utf-8")
                    arquivos_base64[filename] = encoded
                logger.debug(f"Arquivo {filename} codificado com sucesso")
            except FileNotFoundError:
                logger.error(f"Arquivo relatorio_final.pdf não encontrado!")
                raise

        try:
            with open(f"output/data_report_final.csv", "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
                arquivos_base64["comparacao_fiis.csv"] = encoded
            logger.debug(f"Arquivo data_report_final.csv codificado com sucesso")
        except FileNotFoundError:
            logger.error(f"Arquivo data_report_final.csv não encontrado!")
            raise

        with open(
            "output/data_report_final.csv", mode="r", newline="", encoding="utf-8"
        ) as f:
            reader = csv.reader(f)
            cabecalho = next(reader)  # Lê apenas a primeira linha

        # Reescreve o arquivo apenas com o cabeçalho
        with open(
            "output/data_report_final.csv", mode="w", newline="", encoding="utf-8"
        ) as f:
            writer = csv.writer(f)
            writer.writerow(cabecalho)

        logger.info("Processamento concluído com sucesso")
        return JSONResponse(content=arquivos_base64, status_code=200)

    except Exception as e:
        logger.critical(f"Erro crítico no processamento: {str(e)}", exc_info=True)
        return JSONResponse(content={"error": str(e)}, status_code=500)
