# fitness_tracker

A simple web-based fitness/activity tracker application with a graphical user interface. The app allows users input activity data (e.g. a run), track their activities and give some visual insights into the users fitness.

The aim of this project is to build upon the cli-fitness-tracker application, adding a graphical user interface and additional features. Alongside developing the backend using Python, FastAPI, SQLAlchemy and a PostgreSQL database, I have learnt and developed frontend skills including Next.js (React framework), Javascript, HTML, TailwindCSS and Chart.js.

Note: It is a work in progress. This document will get updated as the project progresses and becomes more user friendly.


## Prerequisites

Postgres - this can be downloaded from https://www.postgresql.org/download/


## Initial Setup

Clone the repo: 

```git clone https://github.com/LucyMilligan/fitness-tracker.git```


## Backend 

### Setup

Change directory into the backend directory:

```cd backend```

Create a virtual environment and install the requirements:

```pip install -r requirements.txt```

Create a .env file in the root of the backend directory with the following content, updating the username and password with your postgress username and password:

```DB_URL="postgresql://<username: str>:<password: str>@localhost:5432/fitness_tracker"```

Create the database by running the following in the terminal:

```psql -f database/create_db.sql```

Run the API (changing the port number if necessary):

```uvicorn main:app --reload --port 8080```

Seed the database:

```python seed_db.py```

Note: Prior to seeding the database, the above two steps must be executed. These create the database and tables needed to add data to the database.

### Run tests

To run the backend tests:

```pytest -vvvrP```

### Run API

To run the API, run the following from the backend directory (port 8080 can be replaced with another if necessary):

```uvicorn main:app --reload --port 8080```

Open [http://localhost:8080/docs](http://localhost:8080/docs) with your browser to manually test the API endpoints.


## Frontend

Change directory into the frontend/fitness-tracker directory:

```cd frontend/fitness-tracker```

Run the application on the development server:

```npm run dev```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.


## Further Improvements / TODO

Additional features to be implemented:
- visualise page - create the plots based on data from API's
- add additional pages to update or delete users / activities (API's exist but need the frontend)
- use docker?
- add to a website domain
- add user logins