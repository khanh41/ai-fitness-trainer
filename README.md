# AI Fitness Trainer - AIFT
![docker build](https://github.com/khanh41/ai-fitness-trainer/actions/workflows/docker-image.yml/badge.svg)
![codeQL](https://github.com/khanh41/ai-fitness-trainer/actions/workflows/codeql-analysis.yml/badge.svg)

## Installation ⚡️
### Requires
- Python: 3.7~3.8

Install with poetry:
~~~
pip install poetry
poetry install
~~~

## Deployment app ⛄️
Run MongoDB with docker:
~~~
sudo docker pull mongo
sudo docker run --name some-mongo -p 27017:27017 -d mongo
~~~

## Deployment with Docker 🐳
Docker build and run with Dockerfile:
~~~
sudo docker pull mongo
sudo docker run --name some-mongo -p 27017:27017 -d mongo
sudo docker build -t gym-trainer .
sudo docker run -it -d gym-trainer
~~~
Deployment with docker-compose: 
~~~
docker-compose up -d
~~~
- Server backend - docs: http://0.0.0.0:8088/docs
- Api backend: http://0.0.0.0:8088/redoc
- Server frontend: http://0.0.0.0:8088

## Run tests 😋
Tests for this project are defined in the `tests/` folder.
~~~
pytest
~~~

## Run tools 🌍
Auto format: 
~~~
poetry run app/utils/format
~~~

Auto lint: 
~~~
poetry run app/utils/lint
~~~

Auto test: 
~~~
poetry run app/utils/test
~~~

## Tree directory 🌗 
~~~
app
├── api                  - web related stuff.
│   ├── database         - config database.
│   │   ├── models       - definition of error handlers.
│   │   ├── excute       - sql handling, CRUD.
│   │   ├── connect.py   - connect to database.
│   ├── errors           - definition of error handlers.
│   └── routes           - web routes.
│   └── services         - logic that is not just crud related.
│   └── responses        - response for api request corresponding.
├── ml                   - machine learning model and preprocessing.
│   ├── data_loader      - load data or model.
│   ├── preprocessing    - preprocessing data.
│   ├── figures          - draw (ignore).
│   ├── metrics          - metrics for model, etc.
│   ├── base_model       - model machine learning setup
│   ├── trainers         - model machine learning training.
├── core                 - application configuration, startup events, logging.
├── logger               - export log for server process.
├── tests                - test api, code.
├── utils                - tools format, lint, test, etc.
├── resources            - image, audio, csv, etc. (ignore)
├── pyproject.toml       - dependencies and package.
└── main.py              - FastAPI application creation and configuration.
~~~
