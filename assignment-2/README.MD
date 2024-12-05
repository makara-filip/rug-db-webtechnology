# DB-driven web-technology: Assignment 2

This document contains both theoretical and practical assignment
submission.

Author: Filip Makara, S6163696, m.filip.2@student.rug.nl

The GitHub repository can be found at:
[https://github.com/makara-filip/rug-db-webtechnology/tree/main/assignment-2](https://github.com/makara-filip/rug-db-webtechnology/tree/main/assignment-2)

## Practical part: movie database with authentication

As the assignment stated, I used `flask_wtf` for server form
validation and rendering; `flask_login` for authentication-related logic,
extending the user model and enforcing authenticated state on movie-related
routes: they are protected with the `flask_login.login_required` decorator.

After I created the login and logout functionality, I created and saved
a new user using the interactive Flask shell:

```python
# execute "flask shell" in your terminal
>>> user = User(username="filip")
>>> user.set_password("password")
>>> db.session.add(user)
>>> db.session.commit()
```

After that, I implemented the registration form and route.
For simplicity, user email field is omitted from the form.


## Theoretical part: website inspection

I have chosen `brightspace.rug.nl` website for inspection because of variety
of authentication-related requests, mini-applications and components inside.
When visiting `GET https://brightspace.rug.nl/`, a `302 Found` response is
sent with a redirection (`Location` HTTP header) to `/d2l/login`.
After a few redirects, the browser requested `https://brightspace.rug.nl/d2l/home` with `200 OK` response.

Some of the widgets inside Brightspace requested additional data
after page load - mostly in JSON format or a HTML sub-document.
I noticed widget requests for timetable, grades, faculty tools...

Ukrant widget `POST`-ed `https://ukrant.nl/wp-json/wordpress-popular-posts/v2/views/178173`, but received `403 Forbidden` JSON response with
a short payload containing some `rest_cookie_invalid_nonce` information.

The cookie notice in the website is not provided, but after some searching,
I found the Privacy statement Student Portal, Brightspace & EDU Support
at [https://edusupport.rug.nl/1981939790/Faculty+Admin/General+Information/Privacy/Privacy+statement+Student+Portal%2C+Brightspace+%26+EDU+Support](https://edusupport.rug.nl/1981939790/Faculty+Admin/General+Information/Privacy/Privacy+statement+Student+Portal%2C+Brightspace+%26+EDU+Support).
The portals are using functional and technical cookies for session storage
and language preferences. Additionally, Google Analytics cookies are included
with various widgets. Other cookies cannot be controlled, for example
YouTube or Vimeo components.
