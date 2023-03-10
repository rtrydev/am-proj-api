FROM python:3.10-slim-bullseye
EXPOSE 80

WORKDIR /app
RUN apt update
RUN apt install -y cmake build-essential libssl-dev uuid-dev cmake libcurl4-openssl-dev pkg-config python3-dev
RUN pip install pipenv

COPY ./Pipfile .
COPY ./Pipfile.lock .

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --system

COPY . .

ENTRYPOINT alembic upgrade head && python -u server.py
