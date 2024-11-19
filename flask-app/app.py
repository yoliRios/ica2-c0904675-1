from flask import Flask, jsonify
import psycopg2
import redis
import os

db_host = os.getenv("PGDB_HOST")
db_user = os.getenv("PGDB_USER")
db_password = os.getenv("PGDB_PASSWORD")
db_name = os.getenv("PGDB_NAME")
redis_host = os.getenv("REDIS_HOST")

app = Flask(__name__)

# Connect to Redis
cache = redis.Redis(host=redis_host, port=6379)

# Connect to PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(host=db_host,
                            database=db_name,
                            user=db_user,
                            password=db_password)
    return conn

@app.route('/')
def hello():
    return "Hello, Docker Multi-Container!"

@app.route('/users')
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(users)

@app.route('/cache')
def cache_example():
    if cache.get('key'):
        return f"Cache Hit: {cache.get('key')}"
    else:
        cache.set('key', 'Hello from Redis Cache!')
        return "Cache Miss: Key Set"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
