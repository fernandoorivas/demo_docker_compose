import os
from time import sleep
from flask import Flask, jsonify, request
import psycopg2
import redis

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")

def wait_for_db(max_retries=20):
    for _ in range(max_retries):
        try:
            conn = psycopg2.connect(DATABASE_URL)
            conn.close()
            return True
        except Exception:
            sleep(1)
    raise RuntimeError("DB no respondió, está muerta!")

def init_users_table():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.get("/")
def home():
    return jsonify({
        "message": "¡Hola desde Flask en Docker Compose!",
        "services": {
            "/health": "Verifica la salud de la aplicación",
            "/visits": "Cuenta las visitas usando Redis",
            "/users (GET)": "Lista usuarios desde Postgres",
            "/users (POST)": "Crea un usuario en Postgres"
        }
    })


@app.get("/health")
def health():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        now = cur.fetchone()[0]
        cur.close()

        # Verificar conexión a Redis
        r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
        pong = r.ping()

        return jsonify({
            "status": "ok",
            "db_time": str(now),
            "redis_ping": pong
        })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500
    

@app.get("/visits")
def visits():
    try:
        r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
        count = r.incr("visits")
        return jsonify({
            "visits":int(count)
        })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500
    
@app.post("/users")
def create_user():
    try:
        data = request.get_json() or {}
        name = data.get("name")
        email = data.get("email")

        if not name or not email:
            return jsonify({"status": "error", "message": "name y email son obligatorios"}), 400

        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email) VALUES (%s, %s);", (name, email))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "ok", "message": "Usuario creado"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.get("/users")
def get_users():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM users ORDER BY id;")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        users = []
        for r in rows:
            users.append({"id": r[0], "name": r[1], "email": r[2]})

        return jsonify({"count": len(users), "users": users})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    wait_for_db()
    init_users_table()
    app.run(host="0.0.0.0", port=8000)