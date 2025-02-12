from flask import Flask, request, jsonify
from helpers import *

app = Flask(__name__)


sessions = {}
sessions['last_id'] = 0

@app.route('/session-id', methods=['GET'])
def create_session():
    session_id = sessions['last_id'] + 1
    sessions['last_id'] = session_id
    return jsonify({"session_id": session_id})

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data received'}), 400
    
    return jsonify({'message': 'Data received', 'data': data}), 200


@app.route('/test', methods=['POST'])
def test():
    print(eval("a + 1"))
    return jsonify({"value": eval("a + 1")})


if __name__ == '__main__':
    app.run(debug=True)