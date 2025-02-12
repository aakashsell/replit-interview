from flask import Flask, request, jsonify
from helpers import *


app = Flask(__name__)




sessions = {}
sessions['last_id'] = 0


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
        return jsonify({'message': 'No session id recieved'}), 400
    
    session_id = data['session_id']

    if sessions.get(session_id, 0) == 0:
        return jsonify({'message': 'invalid session id recieved'}), 400
    
    session = sessions.get(session_id)

    global_vars = session['global']
    local_vars = session['local']

    if data.get('user_input', 0) == 0:
        return jsonify({'message': 'no code sent'}), 400
    
    code = data.get('user_input')

    output = execute_code(code, global_vars, local_vars)

    if output.get('error', 0) == 0:
        return jsonify({'code_output': output}), 200  
    else:
        return jsonify({'message': f"error - {output['error']}"}), 400



if __name__ == '__main__':

    app.run(debug=True)