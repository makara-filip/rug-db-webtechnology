# DB-driven web-technology: Assignment 2

This document contains both theoretical and practical assignment
submission. 

Author: Filip Makara, S6163696, m.filip.2@student.rug.nl

The GitHub repository can be found at:
[https://github.com/makara-filip/rug-db-webtechnology/tree/main/assignment-2](https://github.com/makara-filip/rug-db-webtechnology/tree/main/assignment-2)




```python
# execute "flask shell" in your terminal
>>> user = User(username="filip")
>>> user.set_password("password")
>>> db.session.add(user)
>>> db.session.commit()
>>> ^D
```
