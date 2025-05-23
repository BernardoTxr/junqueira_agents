from flask import Flask, request, jsonify
from docling.document_converter import DocumentConverter
from google.cloud import storage
import os

app = Flask(__name__)
storage_client = storage.Client()


@app.route("/processar", methods=["POST"])
def processar_pdf():
    data = request.get_json()
    bucket_name = data["bucket"]
    filename = data["filename"]

    print(f"Received event for file: {filename} in bucket: {bucket_name}")

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)

    local_input_path = f"/tmp/{filename}"
    blob.download_to_filename(local_input_path)

    converter = DocumentConverter()
    result = converter.convert(local_input_path)

    markdown = result.document.export_to_markdown()

    output_filename = f"relatorios_processados/{filename}.md"
    output_blob = bucket.blob(output_filename)

    with open("/tmp/output.md", "w") as f:
        f.write(markdown)

    output_blob.upload_from_filename("/tmp/output.md")

    return jsonify({"status": "success", "output": output_filename})
