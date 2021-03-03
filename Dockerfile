FROM python:3.9-slim-buster

ENV FLASK_APP "remote-wol.py"
ENV FLASK_ENV "production"

WORKDIR /usr/src/app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["flask", "run", "--host=0.0.0.0"]
