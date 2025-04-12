# Simple Django Blog

This is a simple blog application built with Django. It allows users to register, log in, view blog posts, and add
comments. The blog also includes tagging functionality and a rich-text editor for creating content.

You can visit it: [Simple Django Blog](https://testdev122333.pythonanywhere.com/)

## Features

- Blog post creation with rich text support via django-tinymce

- Tagging system using django-taggit

- User registration and login using username and password

- Logged-in users can comment on blog posts

- Email notifications sent when:

    - A new user registers

    - A comment is added to a post

## Tech Stack

- `Django` (Python web framework)

- `django-taggit` – For tag management

- `django-tinymce` – Rich text editor for blog posts

- Built-in Django authentication

## Installation

1. Clone the repo
2. Go to repo dir
3. Create virtual env:

```shell
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

4. Add configuration:

```shell
cd blog/blog
cp .env.example .env
```

Than add values for variables:

- **SECRET_KEY**: Django project secret key
- **DEBUG**: If it's debug version (True or False)
- **EMAIL_HOST**: email host provider domain
- **EMAIL_PORT**: email port
- **EMAIL_HOST_USER**: host user's email
- **EMAIL_HOST_PASSWORD**: host user's password
- **EMAIL_USE_TLS**: use TLS connection (True or False)
- **DEFAULT_FROM_MAIL**: define from what email messages will be sent by default
- **ALLOWED_HOSTS**: a list of allowed hosts. Enter allowed domain names separated by comma.

5. Install required packages:

```shell
pip install -r requirements.txt
```

6. Run db migrations:

```shell
python manage.py migrate
```

7. Create superuser:

```shell
python manage.py createsuperuser
```

8. Run server:

```shell
python manage.py runserver
```
