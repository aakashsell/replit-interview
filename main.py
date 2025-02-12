from flask import Flask, request, jsonify
from helpers import *
import sqlite3
import json


app = Flask(__name__)




sessions = {}
sessions['last_id'] = 0

# database stuff not fully working

def create_session_data(session_id):
    con = sqlite3.connect("./session.db")
    cur = con.cursor()

    cur.execute("""
        INSERT INTO session_data (session_id, global_vars, local_vars)
        VALUES (?, ?, ?)
        """, (session_id, json.dumps({}), json.dumps({})))
     
    con.commit()

    con.close()
    
def check_session_id(session_id):
    con = sqlite3.connect("./session.db")
    cur = con.cursor()

    cur.execute("select global_vars, local_vars from session_data where session_id = ?", (session_id,))
    session = cur.fetchone()
    if session == None:
        return False
    
    sessions[session_id] = {}
    return True

    con.close()
    

def get_session_data(session_id = None):
    con = sqlite3.connect("./session.db")
    cur = con.cursor()

    cur.execute("select global_vars, local_vars from session_data where session_id = ?", (session_id,))
    session = cur.fetchone()
    
    
    sessions[session_id]['global'] = json.loads(session[0])
    sessions[session_id]['local'] = json.loads(session[1])

    con.close()
    


def update_vars(session_id, global_vars, local_vars):
    con = sqlite3.connect("./session.db")
    cur = con.cursor()

    cur.execute("""
            UPDATE session_data 
            SET global_vars = ?, local_vars = ?
            WHERE session_id = ?
        """, (json.dumps(global_vars), json.dumps(local_vars), session_id))
    
    con.commit()
    
    con.close()


 # Main api, this is the good stuff!   


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

    #check_session_id(session_id)

    if sessions.get(session_id, 0) == 0:
        return jsonify({'message': 'invalid session id recieved'}), 400
    
    session = sessions.get(session_id)

    try:
        #print(get_session_data(session_id))
        pass
    except Exception:
        print("not able to save session data")

    global_vars = session['global']
    local_vars = session['local']

    if data.get('user_input', 0) == 0:
        return jsonify({'message': 'no code sent'}), 400
    
    code = data.get('user_input')

    output = execute_code(code, {}, local_vars)

    if output.get('error', 0) == 0:
        try:
            update_vars(session_id, global_vars, local_vars)
        except Exception:
            print("cannot update vars")
        return jsonify({'code_output': output}), 200  
    else:
        return jsonify({'message': f"error - {output['error']}"}), 400



if __name__ == '__main__':

    app.run(debug=True)