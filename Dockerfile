FROM python:3.11

# install nodejs with npm
RUN apt-get update && apt-get install -y nodejs npm

RUN pip install --no-cache-dir --upgrade poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry install

COPY . /app/

ENV PYTHONPATH=/app

CMD ["poetry", "run", "pytest"]
