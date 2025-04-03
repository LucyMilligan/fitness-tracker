# fitness_tracker

The aim of this project is to create a simple fitness tracker application that can take a users activity data as an input (e.g. a run), display activity data back to the user and give some visual insights into the users fitness. 

It is a work in progress, with the backend and API the initial focus. This document will get updated as the project progresses and becomes more user friendly.

## Prerequisites

Postgres - this can be downloaded from https://www.postgresql.org/download/

## Backend Setup

Create a virtual environment and install the requirements

```pip install -r requirements.txt```

## To run the application

### If database does not exist:

Create a .env file in the root of the directory, with the following content, updating the username and password with your postgress username and password:

```DB_URL="postgresql://<username: str>:<password: str>@localhost:5432/fitness_tracker"```

Create the database by running the following in the terminal:

```psql -f create.sql```

### To run the application:

```uvicorn main:app --reload --port <port: int>```

To test the requests, use the browser and localhost:<port: int>/docs
