from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    text = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    status = db.Column(db.Boolean, default=False)


@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/items', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    todos_list = [
        {'id': todo.id, 'text': todo.text, 'status': int(todo.status), 'desc': todo.description} for todo in todos]
    return jsonify({"items": todos_list})


@app.route('/items', methods=['POST'])
def create_todo():
    print(request)
    new_todo = request.get_json()
    text = new_todo.get('text')
    status = new_todo.get('status', False)
    description = new_todo.get('desc', '')

    todo = Todo(
        id=str(uuid.uuid4()),
        text=text, 
        description=description, 
        status=status
    )
    db.session.add(todo)
    db.session.commit()

    return jsonify({'id': todo.id, 'text': text, 'desc': description, 'status': int(status)}), 201

@app.route('/items/<string:todo_id>', methods=['PUT'])
def update_todo_text(todo_id):
    todo = request.get_json()
    text = todo.get('text')
    desc = todo.get('desc')

    db.session.query(Todo).filter_by(id=todo_id).update({'text': text, 'description': desc})
    db.session.commit()

    updated_todo = Todo.query.get(todo_id)
    return jsonify({'id': updated_todo.id, 'text': updated_todo.text, 'desc': updated_todo.description, 'status': int(updated_todo.status)})

@app.route('/items/<string:todo_id>/status', methods=['PUT'])
def update_todo_status(todo_id):
    todo = request.get_json()
    status = todo.get('status')

    db.session.query(Todo).filter_by(id=todo_id).update({'status': status})
    db.session.commit()

    updated_todo = Todo.query.get(todo_id)
    return jsonify({'id': updated_todo.id, 'text': updated_todo.text, 'desc': updated_todo.description, 'status': int(updated_todo.status)})

# get todo by id
@app.route('/items/<string:todo_id>', methods=['GET'])
def get_todo_by_id(todo_id):
    todo = Todo.query.get(todo_id)
    return jsonify({'id': todo.id, 'text': todo.text, 'desc': todo.description, 'status': int(todo.status)})


# delete todo by id
@app.route('/items/<string:todo_id>', methods=['DELETE'])
def delete_todo_by_id(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'id': todo.id, 'text': todo.text, 'desc': todo.description, 'status': int(todo.status)})

if __name__ == '__main__':
    app.run(debug=True)
