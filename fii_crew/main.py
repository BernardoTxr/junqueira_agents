from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)


@app.route("/processar", methods=["POST"])
def processar():
    data = request.get_json()
    bucket = data["bucket"]
    filename = data["filename"]

    try:
        # Executa o crewai com seu script principal (pode ser um .py ou pyproject)
        result = subprocess.run(
            ["crewai", "run"], capture_output=True, text=True, check=True
        )
        return jsonify({"status": "success", "output": result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "error": e.stderr}), 500
