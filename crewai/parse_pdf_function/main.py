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

    print(f"Downloading {filename} from bucket {bucket_name}...")

    local_input_path = f"/tmp/{filename}"
    blob.download_to_filename(local_input_path)

    print(f"Downloaded {filename} to {local_input_path}")

    converter = DocumentConverter()
    result = converter.convert(local_input_path)

    print(f"Conversion done")

    markdown = result.document.export_to_markdown()

    print(f"Markdown conversion done")

    # trocando para o outro bucket
    bucket_name = "relatorios-processados"
    bucket = storage_client.bucket(bucket_name)

    output_filename = f"{filename}"
    output_blob = bucket.blob(output_filename)

    print(f"Uploading {output_filename} to bucket {bucket_name}...")

    with open("/tmp/output.md", "w") as f:
        f.write(markdown)

    print(f"Markdown written to /tmp/output.md")

    output_blob.upload_from_filename("/tmp/output.md")

    print(f"Uploaded {output_filename} to bucket {bucket_name}")

    return jsonify({"status": "success", "output": output_filename})
