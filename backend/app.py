from flask import Flask, request, jsonify
import psycopg2
import os


app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname = os.getenv('POSTGRES_DB', 'todo_db'),
        user = os.getenv('POSTGRES_USER', 'todo_user'),
        password = os.getenv('POSTGRES_PASSWORD', 'password'),
        host = os.getenv('POSTGRES_HOST', 'localhost'),
        port = os.getenv('POSTGRES_PORT', '5432')
    )
    return conn

@app.route('/tasks', methods = ["GET"])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, task FROM tasks;")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(tasks)

@app.route('/tasks', methods = ["POST"])
def add_task():
    task = request.json["task"]
    if not task:
        return jsonify({"error":"Task is required"}),400
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (task) VALUES (%s) RETURNING id;", (task,))
    task_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id":task_id, "task": task}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)    


