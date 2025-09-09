# Flask + AWS RDS (PostgreSQL) Project

This project demonstrates how to build a **Flask application** connected to an **AWS RDS PostgreSQL** database, containerize it with **Docker Compose**, and manage schema/tables.

---

## 🚀 Setup

### 1. Install Python and dependencies

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Upgrade pip and install dependencies:

```bash
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip
pip install flask flask-sqlalchemy psycopg2-binary
```

---

### 2. Configuration (`config.py`)

```python
import os

DB_HOST = "flask-db.cnuocu8suj74.eu-west-1.rds.amazonaws.com"
DB_NAME = "flask-db"
DB_USER = "ITadmin"
DB_PASS = "yourpassword"

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
```

---

### 3. Flask Application (`app.py`)

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

# Example model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

@app.route('/')
def index():
    return "Flask App Connected to AWS RDS PostgreSQL!"

if __name__ == '__main__':
    app.run(debug=True)
```

Run locally:

```bash
source venv/bin/activate
python app.py
```

---

### 4. AWS RDS Setup

Connect to RDS:

```bash
psql -h flask-db.cnuocu8suj74.eu-west-1.rds.amazonaws.com -U ITadmin -d postgres
```

If DB doesn’t exist:

```sql
CREATE DATABASE flask_db;
```

List databases:

```sql
SELECT datname FROM pg_database;
```

---

### 5. Creating Tables

From Python shell:

```bash
cd /home/ubuntu/PostgresRDS
source venv/bin/activate
python3
```

```python
from app import db, app
with app.app_context():
    db.create_all()
```

Manual SQL table:

```sql
\c flask_db

CREATE TABLE entries (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO entries (name, email, message)
VALUES ('Afonso', 'afonso@example.com', 'Hello from AWS RDS!');

SELECT * FROM entries;
```

---

### 6. Docker & Docker Compose

Install:

```bash
apt install docker-compose
```

Stop and clean containers:

```bash
docker-compose down --volumes --remove-orphans
docker system prune -a   # ⚠ deletes all unused images/containers
```

---

### 7. Healthcheck

Inside Docker or host:

```bash
curl http://localhost:5000/health
```

Expected output:

```json
{"ok": true}
```

---

## 🔧 Troubleshooting

* **404 on `/submit`** → Check that your frontend form calls `/api/submit`, not `/submit`.
* **Database connection error** → Ensure AWS RDS security group allows inbound `5432` from your EC2/server.
* **Broken venv** → Recreate it with:

  ```bash
  rm -rf venv
  python3 -m venv venv
  source venv/bin/activate
  ```
* **Docker issues** → Run `docker-compose logs` to debug.

---

## ✅ Next Steps

* Add HTML templates under `templates/`
* Create an API endpoint for `/api/submit`
* Use Docker to deploy Flask + Nginx in production
* Automate DB migrations with **Flask-Migrate**
