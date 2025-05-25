from flask import Flask, request, jsonify
import subprocess
import os
from google.cloud import storage
from pathlib import Path

app = Flask(__name__)
storage_client = storage.Client()


@app.route("/health")
def health():
    return "OK", 200


@app.route("/processar", methods=["POST"])
def processar():
    data = request.get_json()
    bucket = data["bucket"]
    filename = data["filename"]

    print(f"Received event for file: {filename} in bucket: {bucket}")

    bucket = storage_client.bucket(bucket)
    blob = bucket.blob(filename)

    blob.download_to_filename("texto_extraido.txt")

    result = subprocess.run(
        ["crewai", "install"], capture_output=True, text=True, check=True
    )
    result = subprocess.run(
        ["crewai", "run"], capture_output=True, text=True, check=True
    )

    filename = filename.replace(".txt", ".pdf")

    bucket = storage_client.bucket("relatorios-finais")
    new_blob = bucket.blob(filename)

    # Create an output directory in your working directory
    output_dir = Path("output")  # Relative path
    output_dir.mkdir(exist_ok=True, parents=True)

    # Now use this path for your PDF
    pdf_path = output_dir / "relatorio_final.pdf"

    new_blob.upload_from_filename(pdf_path)
    return jsonify({"status": "success", "output": result.stdout})
