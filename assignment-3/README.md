# DB-driven web-technology: Assignment 3

This document contains both theoretical and practical assignment
submission.

Author: Filip Makara, S6163696, `m.filip.2@student.rug.nl`

The GitHub repository can be found at:
[https://github.com/makara-filip/rug-db-webtechnology/tree/main/assignment-3](https://github.com/makara-filip/rug-db-webtechnology/tree/main/assignment-3)

## Practical part: API with authentication

Following [The Flask Mega-Tutorial by Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis),
as recommended from the assignment, I implemented the API
for users and movies; and token authentication on top of it
(see git history).

Additional packages were installed:

- `flask-httpauth` for token-based HTTP authentication,
- `Flask-Migrate` for database migrations (see bellow).

### Database migration

During database migrations, I needed to add `auth_token` and `auth_token_expiration`
columns to the database. For that, I used the
[Flask-Migrate developer documentation](https://flask-migrate.readthedocs.io/en/latest/)
to complete the migrations. After configuring the package
and running `flask db init`, `flask db migrate -m "User Auth Tokens"`,
I manually explicitly named the `auth_token` unique constraint, as
"Alembic [Flask-Migrate dependency] is currently unable to detect
[...] anonymously named constraints".
Finally, I ran `flask db upgrade` to finalize the migration.

Another migration was needed for adding `Movie.genre` field:

```bash
flask db migrate -m "Movie genre field"
# now check the scripts
flask db upgrade
```

### API demonstration

For the following requests and responses, I include only relevant
HTTP headers (omitting cache- or connection-related ones, even the required ones,
such as HOST).

Accessing any token-protected API endpoint (everything except
creating new user) responds with 401 Unauthorized:

```bash
curl -v http://127.0.0.1:5000/api/movies
```

```
> GET /api/movies HTTP/1.1
>
< HTTP/1.1 401 UNAUTHORIZED
< Content-Type: application/json
< Content-Length: 30
< WWW-Authenticate: Bearer realm="Authentication Required"
<
{
  "error": "Unauthorized"
}
```

Obtaining token with correct credentials:

```bash
curl -v --user filip:password http://127.0.0.1:5000/api/tokens -X POST
```

```
* Server auth using Basic with user 'filip'
> POST /api/tokens HTTP/1.1
> Authorization: Basic ZmlsaXA6cGFzc3dvcmQ=
>
< HTTP/1.1 200 OK
< Content-Type: application/json
< Content-Length: 50
<
{
  "token": "0093a9a10c4dd46ed0f306bd71bd4fbe"
}
```

After using the token, accessing the list of movies (paginated):

```bash
curl -v -H "Authorization: Bearer 0093a9a10c4dd46ed0f306bd71bd4fbe" "http://127.0.0.1:5000/api/movies?page=2&page_size=3"
```

```
> GET /api/movies?page=2&page_size=3 HTTP/1.1
> Authorization: Bearer 0093a9a10c4dd46ed0f306bd71bd4fbe
> 
* Request completely sent off
< HTTP/1.1 200 OK
< Content-Type: application/json
< Content-Length: 420
< 
{
  "data": [
    {
      "awards": 1,
      "id": 4,
      "name": "Dunkirk",
      "year": 2017
    },
    {
      "awards": 9,
      "id": 5,
      "name": "Test",
      "year": 2024
    }
  ],
  "links": {
    "next": null,
    "prev": "/api/movies?page=1&page_size=3",
    "self": "/api/movies?page=2&page_size=3"
  },
  "meta": {
    "page": 2,
    "page_size": 3,
    "total_items": 5,
    "total_pages": 2
  }
}
```

Editing movie details (specifically, setting the number of awards for Dunkirk to 300, from original 1 award):
```bash
curl -v -H "Authorization: Bearer 0093a9a10c4dd46ed0f306bd71bd4fbe" -H "Content-Type: application/json" "http://127.0.0.1:5000/api/movies/4" -X PUT --data '{"awards":"300"}'
```

```
> PUT /api/movies/4 HTTP/1.1
> User-Agent: curl/8.7.1
> Accept: */*
> Authorization: Bearer 0093a9a10c4dd46ed0f306bd71bd4fbe
> Content-Type: application/json
> Content-Length: 16
> 
< HTTP/1.1 200 OK
< Content-Type: application/json
< Content-Length: 68
< Location: /api/movies/4
< 
{
  "awards": 300,
  "id": 4,
  "name": "Dunkirk",
  "year": 2017
}
```

Demonstrating the change is saved to the database:
![Database table of movies after the Dunkirk award modification](./images/movies.png)

## Theoretical part: traffic prediction API design

To be continued...