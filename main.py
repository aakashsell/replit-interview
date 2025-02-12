from flask import Flask, request, jsonify
from helpers import *

app = Flask(__name__)


sessions = {}

@app.route('/session-id', methods=['GET'])
def create_session():
    session_id = sessions['last_id'] + 1
    sessions['last_id'] = session_id
    sessions[session_id] = {'global': {}, 'local': {}}
    sessions[session_id]['global'] = {}
    sessions[session_id]['local'] = {}

    return jsonify({"session_id": session_id})

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json() 

    if not data:
        return jsonify({'error': 'No JSON data received'}), 400
    
    if data.get('session_id', 0) == 0:
        return jsonify({'message': 'no session id recieved'}), 400
    
    session_id = data['session_id']

    if sessions.get(session_id, 0) == 0:
        return jsonify({'message': 'invalid session id'}), 400
    
    session = sessions.get(session_id)

    global_vars = session['global']
    local_vars = session['local']

    if data.get('user_input', 0) == 0:
        return jsonify({'message': 'no code sent'}), 400
    
    code = data.get('user_input')
    print(code)

    output = execute_code(code, global_vars, local_vars)

    if not output:
        return jsonify({'code_output': output}), 200  

    return jsonify({'message': 'Code did not run properly'}), 400



if __name__ == '__main__':

    sessions['last_id'] = 0
    app.run(debug=True)