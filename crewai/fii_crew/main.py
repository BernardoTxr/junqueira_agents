from flask import Flask, request, jsonify
import subprocess
import os
from google.cloud import storage

app = Flask(__name__)
storage_client = storage.Client()


@app.route("/processar", methods=["POST"])
def processar():
    data = request.get_json()
    bucket = data["bucket"]
    filename = data["filename"]

    print(f"Received event for file: {filename} in bucket: {bucket}")

    bucket = storage_client.bucket(bucket)
    blob = bucket.blob(filename)

    blob.download_to_filename("texto_extraido.txt")

    # Executa o crewai com seu script principal (pode ser um .py ou pyproject)
    result = subprocess.run(
        ["crewai", "run"], capture_output=True, text=True, check=True
    )

    filename = filename.replace(".txt", ".pdf")

    bucket = storage_client.bucket("relatorios-finais")
    new_blob = bucket.blob(filename)
    new_blob.upload_from_filename("/output/relatorio_final.pdf")
    return jsonify({"status": "success", "output": result.stdout})
