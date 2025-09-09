from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine, text
import os

# Create Flask app
app = Flask(__name__)

# Database connection using DATABASE_URL from environment
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

engine = create_engine(DATABASE_URL, echo=True, future=True)

@app.get("/")
def index():
    """Serve the main HTML page."""
    return render_template("index.html")

@app.get("/health")
def health():
    """Healthcheck endpoint for Docker or monitoring."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"ok": True}
    except Exception as e:
        # Print error so it shows in `docker compose logs`
        print("Healthcheck DB connection failed:", str(e))
        return {"ok": False, "error": str(e)}, 500

@app.post("/api/submit")
def submit():
    """
    Receives form data (from index.html) or JSON (if used in future),
    then inserts into AWS RDS entries table.
    """
    # Try JSON first, fallback to form data
    data = request.get_json() or request.form.to_dict()

    # Validate required fields
    required_fields = ["name", "email", "message"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing input"}), 400

    try:
        with engine.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO entries (name, email, message) "
                    "VALUES (:name, :email, :message)"
                ),
                data
            )
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        # Print error so you see insert failures too
        print("Insert failed:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Flask listens on all interfaces for Docker
    app.run(host="0.0.0.0", port=5000)
