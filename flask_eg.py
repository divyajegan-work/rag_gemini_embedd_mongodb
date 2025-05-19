
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)                                #initialization 

client = MongoClient("MONGODB_URI")
db = client["todo_db"]
todos_collection = db["todos"]

def serialize_todo(todo):
    return {
        "id": str(todo["_id"]),
        "task": todo["task"]
    }
@app.route('/')
def home():
    return "Welcome to the Todo API with MongoDB!"

# get 
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = [serialize_todo(todo) for todo in todos_collection.find()]
    return jsonify(todos)
# post 
@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({"error": "Missing 'task' in request"}), 400
    result = todos_collection.insert_one({"task": data['task']})
    todo = todos_collection.find_one({"_id": result.inserted_id})
    return jsonify({"message": "Todo added successfully", "todo": serialize_todo(todo)}), 201
#put
@app.route('/todos/<string:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    if not data or "task" not in data:
        return jsonify({"error": "Missing 'task' in request"}), 400
    result = todos_collection.update_one({"_id": ObjectId(todo_id)}, {"$set": {"task": data['task']}})
    if result.matched_count == 0:
        return jsonify({"error": "Todo not found"}), 404
    todo = todos_collection.find_one({"_id": ObjectId(todo_id)})
    return jsonify({"message": "Todo updated", "todo": serialize_todo(todo)})
#deletee
@app.route('/todos/<string:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    result = todos_collection.find_one_and_delete({"_id": ObjectId(todo_id)})
    if result:
        return jsonify({"message": "Todo deleted", "todo": serialize_todo(result)})
    return jsonify({"error": "Todo not found"}), 404
if __name__ == '__main__':
    app.run(debug=True)
