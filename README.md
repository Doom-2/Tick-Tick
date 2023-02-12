<a name="readme-top"></a>
# Tick-Tick <img src="/tick-tick-app-logo.png" width="5%" style="position:relative; top:5px;"/>
### ToDo List style app
#### [tick-tick.ml](http://tick-tick.ml)


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About the project</a>
      <ul>
        <li><a href="#techstack">TechStack</a></li>
        <li><a href="#features">Features</a></li>
      </ul>
    </li>
    <li>
      <a href="#project-start">Project start</a>
    </li>
    <li>
      <a href="#step-by-step-project-creation">Step-by-step project creation</a>
      <ul>
        <li><a href="#1-initial-setup-db-connection-django-admin">Initial setup, db connection, django-admin</a></li>
        <li><a href="#2-deploy">Deploy</a></li>
        <li><a href="#3-authentication">Authentication</a></li>
        <li><a href="#4-the-main-interface">The main interface</a></li>
        <li><a href="#5-data-sharing">Data sharing</a></li>
        <li><a href="#6-telegram-bot">Telegram bot</a></li>
        <li><a href="#7-testing">Testing</a></li>
        <li><a href="#8-final">Final</a></li>
      </ul>
    </li>
    <li><a href="#feedback">Feedback</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

This app will help you get your business in order.
* define goals
* sort them by categories
* organize priorities
* track deadlines
* share data

### TechStack

[![Python][Python.js]][Python-url] &nbsp;&nbsp;
[![Django][Django.js]][Django-url] &nbsp;&nbsp;
[![Postgres][Postgres.js]][Postgres-url] &nbsp;&nbsp;
[![AngularJS][AngularJS.js]][AngularJS-url] &nbsp;&nbsp;
[![Docker][Docker.js]][Docker-url]

[Django-url]: https://www.djangoproject.com/
[Django.js]: https://img.shields.io/badge/Django-darkgreen?style=for-the-badge&logo=django&logoColor=white

[Python-url]: https://www.python.org/
[Python.js]: https://img.shields.io/badge/Python-174394?style=for-the-badge&logo=python&logoColor=white

[Postgres-url]: https://www.postgresql.org/
[Postgres.js]: https://img.shields.io/badge/Postgres-737fff?style=for-the-badge&logo=postgresql&logoColor=white

[AngularJS-url]: https://angularjs.org/
[AngularJS.js]: https://img.shields.io/badge/Angular-ff261e?style=for-the-badge&logo=angularjs&logoColor=white

[Docker-url]: https://www.docker.com/
[Docker.js]: https://img.shields.io/badge/Docker-4870ff?style=for-the-badge&logo=docker&logoColor=white


### Features

* Data access permissions
* OAuth2 authorization via VK
* Collaborative goal management
* Search, sorting and filtering data
* Docker and CI/CD-pipeline usage
* Telegram user binding functionality

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- PROJECT START -->
## Project Start
   * Make sure Docker Compose is installed on your local machine
   * Clone repo with `git clone https://github.com/Doom-2/Tick-Tick.git`
   * Rename `.env.example` to `.env` and edit it with your own values
   * Run the following command from the project root `docker compose up --build -d` to run this app
   * Client side (frontend) will be available on `http://localhost`, server side (backend) on `http://localhost:9000`

> To set up user authentication via OAuth 2.0 and API VK make the following steps:
> 1. Create VK app on https://dev.vk.com with `Website` as platform, `http://127.0.0.1` as Website address, `127.0.0.1` as Base domain.
> 2. Set the value of `SOCIAL_AUTH_VK_OAUTH2_KEY` to the value of `App ID` and\
   `SOCIAL_AUTH_VK_OAUTH2_SECRET` to the value of `Secure key` from Settings tab of your VK app.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- STEP-BY-STEP PROJECT CREATION -->
## Step-by-step Project Creation
###### 1. Initial setup, db connection, django-admin

* Create Python Virtual Environment using Poetry
* Install `django`, `django-environ` and `psycopg2-binary` packages. \
  Hereinafter use `Poetry` tool to install python dependencies
* Create Django project `todolist`
* Create a Git repository `Tick-Tick` on GitHub
* From here on, commit changes into Git and push them to remote repository as needed
* Create `.gitignore` file and fill it out yourself or using the appropriate template
* Create `.env` file in project root and fill it with `SECRET_KEY`, `DEBUG` constants according tips in `.env.example` file
* Setup configuration file `settings.py`:
  * reformat it to use ENV vars according this https://django-environ.readthedocs.io/en/latest/quickstart.html
  * change ALLOWED_HOSTS to `["*"]`
* Create new app `core` and register it in `settings.py`
* Add model `User` in `models.py`, inherit it from `AbstractUser` model and put `AUTH_USER_MODEL = 'core.User'` into `settings.py`
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

<p align="right">(<a href="#readme-top">back to top</a>)</p>

###### 2. Deploy
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
* Make CI/CD pipeline using GitHub Actions platform and `action.yaml` file
* Install the `pre-commit` package and use it for code inspection with popular hooks as \
 `end-of-file-fixer`, `trailing-whitespace`, `double-quote-string-fixer`, `flake8`, etc.
* Make Pull Request in feature `deploy`, discuss and check its functionality with Team Lead, \
  then make the necessary changes and merge with the `master` branch

<p align="right">(<a href="#readme-top">back to top</a>)</p>

###### 3. Authentication
* Create a Git branch `auth` and switch to it
* Add CRUD for User Model:
  * Create custom User Manager
  * Use Django authentication system from `django.contrib.auth` standard library \
  Check `username/password` with `authenticate()` method and return a user instance if it is correct with `login()` method, which are presented in this lib
  * Add serializers and endpoints for Register, Login, UserProfile, ChangePassword

> Inherit `LoginSerializer` from `Serializer` class instead of `ModelSerializer` class \
in order to prevent an automatic attempt to create an object, even if it exists in the database.
>
> Inherit `UserProfile` endpoint from `RetrieveUpdateDestroyAPIView`, for logging user out \
  redefine `delete()` method, where call `logout()` method from `django.contrib.auth` library.

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
* Make Pull Request in current feature `auth`, discuss and check its functionality with Team Lead, \
  then make the necessary changes and merge with the `master` branch
* Apply changes on your remote server

<p align="right">(<a href="#readme-top">back to top</a>)</p>

###### 4. The main interface
* Create a Git branch `goals` and switch to it
* Create new app `goals` and register it in `settings.py`
* Add the following models using ORM: `GoalCategory`, `Goal`, `GoalComment`. Hereafter get models specification from [Swagger](http://skypro.oscarbot.ru/swagger/)
* Implement CRUD for these models using DRF APIViews and Serializers
* Add an existing models to Django admin site
* Install `django-filter` package to filter down a queryset based on a model’s fields
* Add `LimitOffsetPagination` to separate web content into discrete pages
* Add `OrderingFilter` and `SearchFilter` to realize the ordering and search functionality
* Apply changes on your remote server

<p align="right">(<a href="#readme-top">back to top</a>)</p>

###### 5. Data sharing
* Create new models `Board` and `BoardParticipant` in `goals` app
* Add `board` field to `GoalCategory` model as ForeignKey
* If you already have entries in db, take into account `board` field cannot be null, \
  because each category must refer to the board, so do the following trick:
  * temporary mark this field as nullable
  * make migrations
  * create an empty migration `python manage.py makemigrations goals —empty -n create_new_objects` \
    and write code in it as shown in `/goals/mogrations/0003_create_new_objects.py`
  * delete `null=True` option of the field `board`
  * make migrations again, on warning choose option 2 (Ignore for now)
  * apply migrations
* Implement CRUD for these models using DRF APIViews and Serializers
* Append an existing models to Django admin site
* Supplement new entity with pagination and ordering functionality
* Redefine QuerySets for existing views `GoalCategory`, `Goal`, `GoalComment`
  considering functionality of the `Board` model
* Add category filtering by board
* Use new version of frontend from here `doom2/tick-tick-frontend:v4.1`
* Apply changes on your remote server

<p align="right">(<a href="#readme-top">back to top</a>)</p>

###### 6. Telegram bot
* Register new telegram bot with BotFather inside Telegram Mobile App
* Practice receiving notifications from Telegram using [long polling](https://core.telegram.org/bots/api#getupdates). \
  Send any message to your newly created bot, then perform the following request in browser address line:
  * `https://api.telegram.org/bot<token>/getUpdates`
  * `https://api.telegram.org/bot<token>/sendMessage?chat_id=85364161&text=hello` \
    where `<token>` is personal token of your bot and `chat_id` is field that came in the `Update` object (1st request)
* Create a Git branch `bot` and switch to it
* Create new app `bot` and register it in `settings.py`
* Add model `Bot`  to `bot` app
* Create python package `tg` inside `bot` folder and make file `bot/tg/dc.py`
* Describe JSON schema of `Message`, `Update`, `Chat`, `MessageFrom`, `GetUpdatesResponse` and `SendMessageResponse`objects using `data classes`
* Create `/bot/tg/client.py` and write `TgClient` class that implements the logic of requests to the Telegram API
* Create custom management command `runbot` and implement simple logic for echo bot responses
* Realise HTTP-method PATCH method on `/bot/verify` to initialize a telegram user as an authorized user in your app
* Implement in a file `runbot.py` bot interaction logic displayed in `/Swagger/tg_bot_logic.pdf`
* Add `bot` section to `docker-compose.yaml`<sup>*</sup> and `build / push` steps to `action.yaml`
  * Use multi-stage build in `Dockerfile` to be able to execute `runbot` command after starting Django or Gunicorn server
  * Set the network for the bot service explicitly and attach it to Postgres service
* Change image with current version of frontend on `doom2/tick-tick-frontend:v5.1`
* Apply changes on your remote server with CI/CD

<p align="right">(<a href="#readme-top">back to top</a>)</p>

###### 7. Testing
* Install pytest-django package
* Cover project with the following tests:
  * User `login`,  `profile`, `signup`, `update-password` logic
  * CRUD functions for `Board`, `GoalCategory`, `Goal`, `GoalComment` models

<p align="right">(<a href="#readme-top">back to top</a>)</p>

###### 8. Final
* Document your code according to PEP8 conversations
* Add type annotations wherever possible
* Make sure that your project meets the following criteria:
  * All application methods are completely identical to the reference swagger
  * Board and Board Participant (owner, writer, reader) functionality works correct
  * User can only see the information from boards he is participant in
  * CRUD functions for GoalCategory, Goal, Comment models work correct
  * Implemented the following functionality:
    * registration
    * login / logout
    * profile obtaining / updating
    * password change
    * OAuth2 authorization via VK
  * CI/CD pipeline is configured:
    *  `docker-compose.yaml` contains 4 section: `db`, `api`, `frontend`, `bot` that interact with each other properly
    * `.github/actions/action.yaml` describes build and deploy jobs
    * each job performs correct and has green status in GitHub `Actions` section
  * Sensitive data is placed in `.env` which is encoded for third parties
  * Telegram account is linked to the app user account
  * Implemented the functionality to view the user's active goals and create new ones



<!-- Feedback -->
## Feedback

###### Executive programmer: <span style="color:black">Peter Khramov:</span> [phramov945@gmail.com](mailto:phramov945@gmail.com)
###### Design brief author: <span style="color:black">SkyPro online university:</span> [skypro-support@skyeng.ru](mailto:skypro-support@skyeng.ru)


<!-- License -->
## License
Distributed under the MIT License. See LICENSE.txt for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
