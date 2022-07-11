<h1 align="center"> FastAPI Postgres App</h1>

---
# 📖About
A simple API using Python with FastAPI freamework, SQLAlchemy,
PostgresSQL Database and set up with Docker. This API is similiar to a library, you can
signup and login, add authors and papers, make all CRUD actions for both. Beside you search for
specific terms, authors or papers.

---
# 🚀Features
- [Python](https://www.python.org/)
- [JWT](https://jwt.io/introduction)
- [Docker](https://www.docker.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PostgresSQL](https://www.postgresql.org/)
---

# ⚡Getting Started

### Docker install:
- [Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

### Postgres install:
    sudo apt update
	apt install postgresql postgresql-contrib

### Database configuration usgin pycharm IDE:
- go to Database -> new 
- select the Data Source **postgres**
- give the name of your choice
- put the Host as: **localhost** and the port as: **5432**
- put the user as: **postgres** and the password as: **root**
- keep url and authentication
- test the connection
<hr/>

- right click on the created Data Source
- select new -> Daatabase
- put the name of **lib**
- once created, right click on lib
- select new -> schema 
- put the name of **public**
- in the pycharm terminal run **python create_db.py** to create the tables in the database


### Run with Docker:
    docker build . -t my-second-api
    docker run --network="host" my-second-api

---

# 🚩Done

Ok, now you should see in the browser that the API is running
on http://0.0.0.0:8000/. To see all endpoints and more information
you can go to /docs

# Using Insomnia 
[Install Insomnia](https://docs.insomnia.rest/insomnia/install)
You can download [this file](https://mega.nz/file/YpJExDaY#QHQG373fMcM9727mijEeW-lFga-gjF4Q84UZexClY8s) and import in your insomnia. Contains all endpoints and
methods already setup to test requests and responses