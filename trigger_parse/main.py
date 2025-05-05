import requests
import functions_framework


@functions_framework.cloud_event
def trigger_processar_pdf(event):
    import base64

    data = event.data
    filename = data["name"]
    bucket = data["bucket"]

    if not filename.startswith("relatorios_brutos/"):
        return

    requests.post(
        "https://processador-pdf-903386606954.southamerica-east1.run.app",
        json={"bucket": bucket, "filename": filename},
        timeout=3600,  # até 60 minutos de espera
    )
