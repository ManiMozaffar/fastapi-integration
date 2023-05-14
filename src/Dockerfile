FROM python:3.11.3


WORKDIR /src

EXPOSE 8000

COPY . .

RUN pip install poetry
RUN poetry install

CMD ["make", "deploy"]
