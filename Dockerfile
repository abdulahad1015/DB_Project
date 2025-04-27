FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN python3.9 -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

COPY wait-for-mysql.sh /usr/local/bin/wait-for-mysql.sh

RUN chmod +x /usr/local/bin/wait-for-mysql.sh

LABEL org.opencontainers.image.source=https://github.com/abdulahad1015/DB_Project

ENTRYPOINT ["bash", "-c", "/usr/local/bin/wait-for-mysql.sh && python run.py"]
