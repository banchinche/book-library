# Library API

This project is an example of the library API implementation.

Also, this topic was chosen for course work **"API for library book management"**
and learning how to use FastAPI web-framework with SQLAlchemy (async).

# How to use it

1. Clone repo
```
git clone https://github.com/banchinche/book-library.git
```
2. Run docker-compose services

```
docker-compose up
```

# Tech-stack
- FastAPI
- PostgreSQL
- JWT authentication
- Pgadmin (for development only)


# Diagrams

For course work I have prepared various UML-diagrams, 
you can find them 
[here](https://github.com/banchinche/book-library/tree/master/diagrams).

# Further improvements

- Add user roles for correct edit/delete permissions.
- Improve JWT with adding refresh token (and probably blacklist for revoked tokens).
- Increase test coverage and quality with async tests (pytest-asyncio/httpx).
- Minor fixes (validations, m2m assignments).
