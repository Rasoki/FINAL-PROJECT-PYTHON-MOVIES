import json
import config

connex_app = config.connex_app
connex_app.add_api('swagger.yml')
connex_app = connex_app.app

client = connex_app.test_client()

#test read all directors
def test_directors_read_all():
    url = 'api/directors?limit=10'

    response = client.get(url)
    data = json.loads(response.get_data())
    assert isinstance(data, list) is True
    assert response.status_code == 200

#test read all movies
def test_movies_read_all():
    url = 'api/movies?limit=10'

    response = client.get(url)
    data = json.loads(response.get_data())
    assert isinstance(data, list) is True
    assert response.status_code == 200

#test create directors
def test_director_create():
    url = 'api/directors'
    mock_request_headers = {
        'Content-Type': 'application/json'
    }

    mock_request_data = {
        "department": "Directing",
        "gender": 2,
        "name": "Maman",
        "uid": 9000
    }

    response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
    data = json.loads(response.get_data())
    assert isinstance(data, dict) is True
    assert response.status_code == 201