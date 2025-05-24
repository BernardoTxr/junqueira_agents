import functions_framework
import requests
import base64
import json


@functions_framework.cloud_event
def trigger_cloud_run(cloud_event):
    data = cloud_event.data

    bucket = data["bucket"]
    name = data["name"]

    print(f"Received event for file: {name} in bucket: {bucket}")

    payload = {"bucket": bucket, "filename": name}

    response = requests.post(
        "https://crewai-service-903386606954.us-central1.run.app/processar",
        json=payload,
    )

    if response.ok:
        print("Relatório enviado com sucesso.")
    else:
        print("Erro ao enviar para o container:", response.text)
        response.raise_for_status()
