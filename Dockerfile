    # Use uma imagem base oficial do Python
    FROM python:3.9-alpine

    # Atualize a lista de pacotes e instale dependências necessárias
    RUN apt-get update && \
        apt-get install -y postgresql postgresql-contrib gcc libpq-dev && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/*

    # Crie e ative um ambiente virtual Python
    RUN python -m venv --copies /opt/venv
    ENV PATH="/opt/venv/bin:$PATH"

    # Copie o arquivo de requisitos e instale dependências Python
    COPY requirements.txt .
    RUN pip install --upgrade pip && pip install -r requirements.txt

    # Copie o código da aplicação para o contêiner
    COPY . /app

    # Defina o diretório de trabalho
    WORKDIR /app

    # Comando para iniciar a aplicação
    CMD ["python", "main.py"]
