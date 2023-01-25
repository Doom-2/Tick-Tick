FROM python:3.10-slim
MAINTAINER "Doom Guy"

WORKDIR /project

EXPOSE 9000

RUN pip install "poetry"

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi --no-root

COPY . .

ENTRYPOINT ["bash", "entrypoint.sh"]

#CMD ["gunicorn", "todolist.wsgi", "-w", "4", "-b", "0.0.0.0:9000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:9000"]
