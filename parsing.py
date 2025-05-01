import io
import pdfplumber
from google.cloud import storage


def extrair_texto_pdf(event, context):
    """
    Função acionada por um evento do Cloud Storage.
    Extrai o texto de um PDF e o salva em um novo arquivo de texto.

    Parâmetros:
      event: dict, dados do evento do Cloud Storage
      context: metadata do evento
    """
    bucket_name = event["bucket"]
    file_name = event["name"]

    print(f"Processando arquivo: gs://{bucket_name}/{file_name}")

    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Baixar o PDF como bytes
    pdf_bytes = blob.download_as_bytes()

    # Inicializar a extração de texto
    texto_extraido = ""
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                texto_extraido += page_text + "\n"

    # Define o nome do arquivo de saída, mantendo a estrutura do bucket
    output_file_name = f"processed/{file_name}.txt"
    output_blob = bucket.blob(output_file_name)
    output_blob.upload_from_string(texto_extraido, content_type="text/plain")

    print(f"Texto extraído salvo em: gs://{bucket_name}/{output_file_name}")


extrair_texto_pdf(
    {"bucket": "seu-bucket", "name": "caminho/para/seu/arquivo.pdf"}, None
)
