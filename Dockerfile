FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN python3.9 -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

LABEL org.opencontainers.image.source=https://github.com/abdulahad1015/DB_Project

ENTRYPOINT ["bash", "-c", "python run.py"]
