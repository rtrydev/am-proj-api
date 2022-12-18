FROM python:3.10-slim-bullseye
EXPOSE 80
EXPOSE 443

WORKDIR /app
COPY . .

RUN apt update
RUN apt install -y cmake build-essential libssl-dev uuid-dev cmake libcurl4-openssl-dev pkg-config python3-dev
RUN pip install pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --system

ENTRYPOINT python -u server.py
