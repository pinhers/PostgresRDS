# Flask + AWS RDS Project Setup Guide

## Prerequisites

* Ubuntu server or local machine with internet access
* Python 3.11 installed
* AWS RDS PostgreSQL instance
* Docker and Docker Compose installed

## Step 1: Python Virtual Environment

```
sudo apt update
sudo apt install -y python3-venv python3-pip
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install flask flask-sqlalchemy psycopg2-binary
```

## Step 2: Configuration

Create a configuration file with your RDS credentials. Include host, database name, user, and password, and build the SQLAlchemy URI.

## Step 3: Flask App

* Initialize Flask
* Connect SQLAlchemy to the database using the URI
* Define models for tables (User, Entries, etc.)
* Create routes for `/` and `/submit`
* Use `app.run(host='0.0.0.0', port=5000)` for Docker compatibility

## Step 4: Database Setup

* Connect to PostgreSQL using `psql`:

```
psql -h <RDS_HOST> -U <USER> -d postgres
```

* Create database if missing:

```
CREATE DATABASE flask_db;
```

* Create necessary tables (e.g., entries):

```
CREATE TABLE entries (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Step 5: Initialize Tables via Flask

* Activate virtual environment:

```
source venv/bin/activate
python3
```

* Inside Python shell:

```
from app import db, app
with app.app_context():
    db.create_all()
```

## Step 6: Docker & Docker Compose

* Build and run containers
* Use health checks for Flask service
* Configure Nginx to serve static content and proxy API requests
* Common commands:

```
docker-compose build
docker-compose up -d
docker-compose down --volumes --remove-orphans
docker system prune -a
```

## Step 7: Testing

* Test `/health` endpoint for DB connectivity
* Test `/submit` endpoint via curl or Postman
* Confirm data is inserted into RDS

## Troubleshooting

* 404 errors: check route paths and Nginx proxy
* TemplateNotFound: ensure `templates/` folder exists and contains `index.html`
* DB connection errors: verify `DATABASE_URL` or credentials
* Docker mount errors: verify paths exist on host
