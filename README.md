# Tick-Tick
### ToDo List style app
### Tech stack - Python 3.10, Django 4.1.4, Postgres 15.0-alpine, Docker Compose

#### 1. Project start:
   * Make sure Docker Compose is installed on your local machine
   * Clone repo with `git clone https://github.com/Doom-2/Tick-Tick.git`
   * Rename `.env.example` to `.env` and edit it with your own values. See footnote for more <sup>*</sup>
   * Run the following command from the project root `docker compose up --build -d` to run this app
   * Client side (frontend) will be available on `http://localhost`, server side (backend) on `http://localhost:9000`

---
<sup>*</sup>
To set up user authentication via OAuth 2.0 and API VK make the following steps:
1. Create VK app on https://dev.vk.com with `Website` as platform, `http://127.0.0.1` as Website address, `127.0.0.1` as Base domain.
2. Set the value of `SOCIAL_AUTH_VK_OAUTH2_KEY` to the value of `App ID` \
and `SOCIAL_AUTH_VK_OAUTH2_SECRET` to the value of `Secure key` from Settings tab of your VK app.
---
&nbsp;
#### 2. Project Creation Steps
2.1 Initial setup, DB connection, Django admin customization
* Create Python Virtual Environment using Poetry
* Install `django`, `django-environ` and `psycopg2-binary` packages. \
  Hereinafter use `Poetry` tool to install python dependencies.
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
* Add `gunicorn` and `djangorestframework` package
* Create Dockerfile for Django api in the project root and make sure it can build:
  * In `CMD` instruction use `gunicorn` instead of `runserver`
  * In `ENTRYPOINT` instruction include script that contains applying migrations logic
* Create `docker-compose.yaml` file in the project root and fill it using the following instructions:
  * 3 services should be created - `db` for Postgres, `api` for Django app, `frontend` for frontend server nginx
  * An existing image for frontend `doom2/tick-tick-frontend` should be used
  * Use volumes for postgres, api and nginx configuration file
  * A volume for static should be created as well to store Django static files
  * Api container should depend on db container, while frontend container should depend on api
* Execute command `docker-compose up --build -d` and make sure that all services are started correctly
* Crete Cloud VPS if you don't have one
* Create DNS name using Freenom service (https://www.freenom.com)
* Delegate the domain to hosting
* Setup your VPS:
  * Install Docker & Compose services
  * Create user `deploy` with admin privileges
  * Allow SSH connection by login and password
* Make CI/CD pipeline using GitHub Actions platform
* Install the `pre-commit` package and use it for code inspection with popular hooks as \
 `end-of-file-fixer`, `trailing-whitespace`, `double-quote-string-fixer`, `flake8`, etc.

2.3 Auth
* Add CRUD for User Model:
  * Create custom User Manager
  * Use Django authentication system from `django.contrib.auth` standard library. \
  Check `username/password` with `authenticate()` method and return a user instance if it is correct with `login()` method, which are presented in this lib.
  * Add serializers and endpoints for Register, Login, UserProfile, ChangePassword <sup>*</sup>
---
<sup>*</sup>
Tips:
1. Inherit `LoginSerializer` from `Serializer` class instead of `ModelSerializer` class \
   in order to prevent an automatic attempt to create an object, even if it exists in the database.
2. Inherit `UserProfile` endpoint from `RetrieveUpdateDestroyAPIView`, for logging user out \
   redefine `delete()` method, where call `logout()` method from `django.contrib.auth` library.
---
* Set up user authentication via VK or any other social network using Python Social Auth mechanism for Django projects:
  * Main configuration: https://python-social-auth.readthedocs.io/en/latest/configuration/django.html
  * Backend support for VK: https://python-social-auth.readthedocs.io/en/latest/backends/vk.html
* Add URLs entries to `ursl.py` of `core` app as following rules:
  * `core/signup` for register endpoint
  * `core/login` for login endpoint
  * `core/profile` for user profile endpoint
  * `core/update_password` for password update endpoint
* Add URLs entry `path('oauth/', include('social_django.urls', namespace='social'))` to `urls.py` of `todolist` app for social authentication
* Update frontend image to `doom2/tick-tick-frontend:v2.0` in `docker-compose.yaml` locally and remotely
* Install `drf_yasg` package to generate Swagger/OpenAPI 2.0 specification from your Django Rest Framework API
* Test all endpoints via Postman API platform or Swagger tool
