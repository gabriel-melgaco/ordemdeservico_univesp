FROM python:3.12-slim

# Evita input interativo
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instala dependências
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia o projeto
COPY . .

# Expõe a porta usada pelo gunicorn
EXPOSE 8000

# Comando para iniciar
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
