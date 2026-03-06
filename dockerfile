FROM ollama/ollama:latest

# Instala Python + pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# Instala pacotes com flag para ignorar PEP 668
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

# Baixa modelo MUITO leve pro free tier
RUN ollama serve & sleep 15 && ollama pull llama3.2:1b && pkill ollama

EXPOSE 8501

CMD ["sh", "-c", "ollama serve & sleep 5 && streamlit run app.py --server.port 8501 --server.address 0.0.0.0"]
