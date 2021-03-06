# Flawful Forum

## About

This is a Django-based project work for the Helsinki Open University MOOC course [Cyber Security Base 2020](https://cybersecuritybase.mooc.fi/).

The project consists of a simple message forum **that contains several intentional security flaws** in order to demonstrate the [OWASP Top 10 Web Application Security Risks](https://owasp.org/www-project-top-ten/).

## Instructions

First, clone the project with `git clone https://github.com/joonaspartanen/flawful_forum`.

Then, navigate to the `flawful_forum/` directory and run the following commands:

```
python3 manage.py migrate
python3 manage.py runserver
```

The application can now be accessed on port 8000.

On startup, the application creates two users for test purposes (one with admin rights):

| Username   | Password    |
| ---------- | ----------- |
| superadmin | verysecret  |
| testuser   | quitesecret |
