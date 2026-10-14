
from flask import Flask, request, redirect, render_template_string
import json
import os

app = Flask(__name__)

FILE = "tasks.json"


def load_tasks():
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False)


@app.route("/", methods=["GET", "POST"])
def home():
    tasks = load_tasks()

    if request.method == "POST":
        name = request.form.get("task", "").strip()

        if name:
            tasks.append({
                "name": name,
                "done": False
            })
            save_tasks(tasks)

        return redirect("/")

    page = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport"
              content="width=device-width, initial-scale=1">
        <title>My To-Do List</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f3f5f2;
                padding: 25px 15px;
                color: #28382d;
            }

            .container {
                max-width: 450px;
                margin: auto;
                background: white;
                padding: 22px;
                border-radius: 18px;
            }

            h1 {
                text-align: center;
            }

            input {
                width: 65%;
                padding: 12px;
                border: 1px solid #ccc;
                border-radius: 8px;
                box-sizing: border-box;
            }

            button {
                padding: 12px;
                border: none;
                border-radius: 8px;
                background: #54785d;
                color: white;
            }

            .task {
                background: #f3f5f2;
                padding: 12px;
                margin-top: 12px;
                border-radius: 10px;
                overflow-wrap: anywhere;
            }

            .done {
                text-decoration: line-through;
                color: gray;
            }

            form {
                display: inline;
            }

            .delete {
                background: #b45b5b;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h1>My To-Do List</h1>
            <p>One thing at a time.</p>

            <form method="POST">
                <input name="task"
                       placeholder="Enter your task..."
                       required>
                <button type="submit">Add</button>
            </form>

            <h3>My Tasks ({{ tasks|length }})</h3>

            {% for task in tasks %}
                <div class="task">
                    <span class="{{ 'done' if task.done else '' }}">
                        {{ task.name }}
                    </span>

                    <br><br>

                    <form method="POST"
                          action="/done/{{ loop.index0 }}">
                        <button type="submit">
                            {{ 'Undo' if task.done else 'Done' }}
                        </button>
                    </form>

                    <form method="POST"
                          action="/delete/{{ loop.index0 }}">
                        <button class="delete" type="submit">
                            Delete
                        </button>
                    </form>
                </div>
            {% else %}
                <p>No tasks yet. Add your first task!</p>
            {% endfor %}
        </div>
    </body>
    </html>
    """

    return render_template_string(page, tasks=tasks)


@app.route("/done/<int:number>", methods=["POST"])
def complete(number):
    tasks = load_tasks()

    if 0 <= number < len(tasks):
        tasks[number]["done"] = not tasks[number]["done"]
        save_tasks(tasks)

    return redirect("/")


@app.route("/delete/<int:number>", methods=["POST"])
def delete(number):
    tasks = load_tasks()

    if 0 <= number < len(tasks):
        tasks.pop(number)
        save_tasks(tasks)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
