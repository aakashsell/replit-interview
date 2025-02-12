from flask import Flask, request, jsonify
from helpers import *
import sqlite3


app = Flask(__name__)




sessions = {}
sessions['last_id'] = 0

def get_session_data(session_id):
    con = sqlite3.connect("./session.db")
    cur = con.cursor()

    
    tmp = cur.execute("select count(*) from session_data where session_id = ?", (session_id,))
    session = cur.fetchone()

    if not session[0]:
        cur.execute("insert into session_data values(?,?,?)", (session_id,{},{},))
    
    

def update_vars(session_id, global_vars, local_vars):



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
    print(data)

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