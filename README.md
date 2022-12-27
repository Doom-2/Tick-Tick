# Tick-Tick
### ToDo List style app
### Tech stack - Python 3.10, Django 4.1.4, Postgres

#### 1. Project start:
   * Install dependencies by running the command `poetry install` in terminal
   * Connect to DB by renaming `.env.example` files located in `./postgres` and project root dirs to `.env` and filling them with your own values
   * Run the following commands in the terminal from project root `./manage.py migrate`, `./manage.py runserver`
   * Backend side will be available on `http://localhost:8000`
&nbsp;
#### 2. Project Creation Steps
2.1 Initial setup, DB connection, Django admin customization
   * Create Python Virtual Environment using Poetry
   * Install `django`, `django-environ` and `psycopg2-binary` packages through Poetry
   * Create Django project `todolist`
   * Create a Git repository `Tick-Tick` on GitHub
   * From here on, commit changes into Git as needed
   * Create .gitignore and fill it out yourself or using the appropriate template
   * Setup configuration file:
     * create `.env` file in project root and fill it with `SECRET_KEY`, `DEBUG` constants according tips in `.env.example` file
     * reformat `settings.py` to use env vars according this https://django-environ.readthedocs.io/en/latest/quickstart.html
     * change ALLOWED_HOSTS to `["*"]`
   * Create new app `core` and register it in `settings.py`
   * Create model `User` in `models.py`, inherit it from `AbstractUser` model and put `AUTH_USER_MODEL = 'core.User'` into `settings.py`
   * Setup connection to Postgres:
     * Add Docker container with Postgres to project via `docker-compose.yaml` in projects root
     * Add to `.env` file `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` constants according tips in `.env.example`
     * Run docker service through `docker compose up -d`
     * Check the connection via any tool you like, e.g. PyCharm Database tools or PGAdmin
   * Add to `.env` file `DATABASE_URL` constant according tips in `.env.example`
   * Reformat `settings.py` to use env vars in `DATABASES` dict according this https://django-environ.readthedocs.io/en/latest/quickstart.html
   * Make migrations for `core` app by running command `./manage.py makemigrations` from the project root
   * Apply all migrations by running command `./manage.py migrate` from the project root
   * Customize Django Admin panel:
     * Make only the following fields displayed: `username`, `email`, `first_name`, `last_name`
     * Add search by the following fields: `email`, `first_name`, `last_name`, `username`
     * Add filters for the following fields: `is_staff`, `is_active`, `is_superuser`
     * Hide `password` field
     * Make fields `last_login`, `date_joined` non-editable

2.2 Deploy
* Create a Git branch 'deploy' and switch to it using command `git switch -c deploy`
* * Add `gunicorn` and `djangorestframework` package through Poetry
* Create Dockerfile for Django api in the project root and make sure it can build.
  * In `CMD` instruction use `gunicorn` instead of `runserver`.
  * In `ENTRYPOINT` instruction include script that contains applying migrations logic
* Create `docker-compose.yaml` file in the project root and fill it using the following instructions:
  * 3 services should be created - `db` for Postgres, `api` for Django app, `frontend` for frontend server nginx
  * An existing image for frontend `doom2/tick-tick-frontend` should be used
  * Use volumes for postgres, api and nginx configuration file.
  * A volume for static should be created as well to store Django static files
  * Api container should depend on db container, while frontend container should depend on api
* Execute command `docker-compose up -d` and make sure that all services are started correctly
* Crete Cloud VPS if you don't have one
* Create DNS name using Freenom service (https://www.freenom.com)
* Delegate the domain to hosting
* Setup your VPS:
  * Install Docker & Compose services
  * Create user `deploy` with admin privileges
  * Allow SSH connection by login and password
* Make CI/CD pipeline using GitHub Actions platform.