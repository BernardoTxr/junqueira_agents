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

    bucket = storage_client.bucket(bucket)
    blob = bucket.blob(filename)

    blob.download_to_filename("texto_extraido.txt")

    try:
        # Executa o crewai com seu script principal (pode ser um .py ou pyproject)
        result = subprocess.run(
            ["crewai", "run"], capture_output=True, text=True, check=True
        )
        new_filename = f"relatorio_final_{filename}"
        new_blob = bucket.blob(new_filename)
        new_blob.upload_from_filename("/tmp/output.pdf")
        return jsonify({"status": "success", "output": result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "error": e.stderr}), 500
