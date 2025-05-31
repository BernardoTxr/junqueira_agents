from fastapi import FastAPI, UploadFile, File
from typing import List
from fastapi.responses import JSONResponse

import pdfplumber
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()


@app.get("/health")
def health():
    return "OK", 200


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/processar")
async def processar_pdf(files: List[UploadFile] = File(...)) -> JSONResponse:
    textos = []
    for file in files:
        filename = file.filename.lower()

        # Salvar o arquivo
        input_path = os.path.join("./uploads", filename)
        os.makedirs("./uploads", exist_ok=True)

        contents = await file.read()

        with open(input_path, "wb") as f:
            f.write(contents)

        with pdfplumber.open(input_path) as pdf:
            texto = ""
            for page in pdf.pages:
                texto += (
                    page.extract_text() or ""
                ) + "\n"  # Garante que não quebre se a página não tiver texto

        textos.append(texto)

    # Possibilidade de chamar outra api
    return JSONResponse(
        content={
            "message": textos,
            "filenames": [file.filename for file in files],
            "status": "success",
        },
        status_code=200,
    )


import os

port = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
