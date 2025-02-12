import pytest
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_eval_simple_adding(client):
    # Simulate a GET request to the "/" route
    response = client.get('/session-id')
    data1 = response.get_json() 
    
    # Assert the response status code
    assert response.status_code == 200
    assert 'session_id' in data1
    
    body = {"session_id": data1['session_id'], "user_input": "1 + 1"}
    response = client.post('/run', json=body)


    assert response.status_code == 200
    json_response = response.get_json()

    print(json_response)
    root = str(json_response['code_output']['root'])

    assert json_response['code_output']['data'][root]['value'] == 2

def test_eval_simple_multiple_sessions(client):
    # Simulate a GET request to the "/" route
    response = client.get('/session-id')
    data1 = response.get_json() 
    
    # Assert the response status code
    assert response.status_code == 200
    assert 'session_id' in data1
    
    body = {"session_id": data1['session_id'], "user_input": "1 + 1"}
    response = client.post('/run', json=body)


    assert response.status_code == 200
    json_response = response.get_json()

    print(json_response)
    root = str(json_response['code_output']['root'])

    assert json_response['code_output']['data'][root]['value'] == 2



