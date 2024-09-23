from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Predefined data
groups = [
    {"id": 1, "groupName": "Group 1", "members": [1, 2, 3]},
    {"id": 2, "groupName": "Group 2", "members": [4, 5]},
]

students = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
    {"id": 4, "name": "David"},
    {"id": 5, "name": "Eve"},
]

@app.route('/api/groups', methods=['GET'])
def get_groups():
    return jsonify(groups)

@app.route('/api/students', methods=['GET'])
def get_students():
    return jsonify(students)

@app.route('/api/groups', methods=['POST'])
def create_group():
    group_data = request.json
    group_name = group_data.get("groupName")
    group_members = group_data.get("members")
    
    if not group_name or not group_members:
        abort(400, "Group name and members are required")

    new_group_id = max([group["id"] for group in groups]) + 1
    new_group = {"id": new_group_id, "groupName": group_name, "members": group_members}
    groups.append(new_group)

    return jsonify(new_group), 201

@app.route('/api/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    global groups
    group = next((g for g in groups if g["id"] == group_id), None)
    if group is None:
        abort(404, "Group not found")
    
    groups = [g for g in groups if g["id"] != group_id]
    return '', 204

@app.route('/api/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    group = next((g for g in groups if g["id"] == group_id), None)
    if group is None:
        abort(404, "Group not found")
    
    group_details = {
        "id": group["id"],
        "groupName": group["groupName"],
        "members": [student for student in students if student["id"] in group["members"]]
    }
    return jsonify(group_details)

if __name__ == '__main__':
    app.run(port=3902, debug=True)
