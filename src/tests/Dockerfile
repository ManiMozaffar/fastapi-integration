FROM python:3.11.3


WORKDIR /src

COPY ../. .

RUN pip install poetry
RUN poetry install

CMD ["make", "test"]
