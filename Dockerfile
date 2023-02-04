FROM python:3.10-slim as base-image
MAINTAINER "Doom Guy"

WORKDIR /project

EXPOSE 9000

RUN pip install "poetry"

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi --no-root

COPY . .

ENTRYPOINT ["bash", "entrypoint.sh"]


FROM base-image as api-image

CMD ["gunicorn", "todolist.wsgi", "-w", "4", "-b", "0.0.0.0:9000"]


FROM base-image as bot-image

CMD ["python", "manage.py", "runbot"]
