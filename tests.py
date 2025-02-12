import pytest
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_eval_simple(client):
    response = client.get('/session-id')
    data1 = response.get_json() 
    
    assert response.status_code == 200
    assert 'session_id' in data1
    
    body = {"session_id": data1['session_id'], "user_input": "'test'"}
    response = client.post('/run', json=body)


    assert response.status_code == 200
    json_response = response.get_json()

    root = str(json_response['code_output']['root'])

    assert json_response['code_output']['data'][root]['value'] == 'test'

def test_eval_simple_adding(client):
    response = client.get('/session-id')
    data1 = response.get_json() 
    
    assert response.status_code == 200
    assert 'session_id' in data1
    
    body = {"session_id": data1['session_id'], "user_input": "1 + 1"}
    response = client.post('/run', json=body)


    assert response.status_code == 200
    json_response = response.get_json()

    root = str(json_response['code_output']['root'])

    assert json_response['code_output']['data'][root]['value'] == 2

def test_eval_simple_multiple_sessions(client):
    #Setting the values of a in two sessions

    response1 = client.get('/session-id')
    data1 = response1.get_json() 
    session_id1 = data1['session_id']

    body1 = {"session_id": session_id1, "user_input": "a = 1"}
    client.post('/run', json=body1)


    response2 = client.get('/session-id')
    data2 = response2.get_json() 
    session_id2 = data2['session_id']

    body2 = {"session_id": session_id2, "user_input": "a = 2"}
    client.post('/run', json=body2)

    # checking to make sure they are different
    
    body1 = {"session_id": session_id1, "user_input": "a"}
    response1 = client.post('/run', json=body1)

    body2 = {"session_id": session_id2, "user_input": "a"}
    response2 = client.post('/run', json=body2)


    json_response1 = response1.get_json()
    json_response2 = response2.get_json()

    root1= str(json_response1['code_output']['root'])
    root2= str(json_response2['code_output']['root'])

    value1 = json_response1['code_output']['data'][root1]['value'] 
    value2 = json_response2['code_output']['data'][root2]['value'] 

    assert value1 != value2

def test_nested_object(client):
    response = client.get('/session-id')
    data1 = response.get_json() 
    sessionid = data1['session_id']
    
    body = {"session_id": sessionid, "user_input": "a = {}"}
    response = client.post('/run', json=body)
    

    body = {"session_id": sessionid, "user_input": "b = {}"}
    response = client.post('/run', json=body)


    body = {"session_id": sessionid, "user_input": "a['b'] = b"}
    response = client.post('/run', json=body)

    body = {"session_id": sessionid, "user_input": "b['a'] = a"}
    response = client.post('/run', json=body)


    body = {"session_id": sessionid, "user_input": "a"}
    response = client.post('/run', json=body)
    json_response = response.get_json()

    

    root = str(json_response['code_output']['root'])
    assert str(json_response['code_output']['data'][root]['value']['b']['ref']) == root





