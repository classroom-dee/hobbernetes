from flask import Flask, request, jsonify
from flask_cors import CORS

app   = Flask(__name__)
CORS(app) # all routes

todos = ["todo1", "todo2", "todo3", "todo4", "todo5", "todo6"]

@app.route("/todos", methods=["GET", "POST"])
def handle_todos():
    if request.method == "GET":
        return jsonify(todos)
    
    # for POST req
    item = (request.get_json() or {}).get("item")
    if item:
        todos.append(item)
    return jsonify(todos), 201

if __name__ == "__main__":
    app.run(port=8061, host='0.0.0.0', debug=True)