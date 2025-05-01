from docling.document_converter import DocumentConverter

source = "download1 KNRI11.pdf"  # document per local path or URL
converter = DocumentConverter()
result = converter.convert(source)
markdown_text = result.document.export_to_markdown()

with open("texto_extraido.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write(markdown_text)
