FROM python:3.10-slim

# Dependências do sistema
RUN apt-get update && \
    apt-get install -y gcc libpq-dev \
    libcairo2 libcairo2-dev libpangocairo-1.0-0 \
    && apt clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# Instala crewai + dependências
RUN pip install --upgrade pip \
    && pip install crewai flask gunicorn \
    && crewai install

ENV VIRTUAL_ENV="/app/.venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

EXPOSE 8080

# Executa a API Flask via Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]
