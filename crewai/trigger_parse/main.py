import requests
import functions_framework


@functions_framework.cloud_event
def trigger_processar_pdf(event):
    import base64

    data = event.data
    filename = data["name"]
    bucket = data["bucket"]

    print(f"Received event for file: {filename} in bucket: {bucket}")

    if not filename.startswith("relatorios_brutos/"):
        return

    requests.post(
        "https://junqueira-agents-903386606954.us-central1.run.app",
        json={"bucket": bucket, "filename": filename},
        timeout=3600,  # até 60 minutos de espera
    )
