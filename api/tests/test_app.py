import os
import json
import pytest

from fastapi.testclient import TestClient

from app import app
from api.utils.json_data_models import DummyRequest, DummyResponse

client = TestClient(app)

# Set API Key Authentication Related Variables
API_KEY_HEADER_KEY_NAME = "x-api-key"
API_KEY_ENVIRONMENT_VARIABLE_NAME = "API_TOKEN"
RIGHT_API_KEY = os.getenv(API_KEY_ENVIRONMENT_VARIABLE_NAME)
WRONG_API_KEY = "wrong-api-key"

# Load Data for Test Cases
path_to_test_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./test_data.json")

test_data = {}
with open(path_to_test_data, 'r') as f:
    test_data = json.load(f)


# API Token Behaviour Tests with GET Endpoint
def test_get_endpoint_without_api_token():
    response = client.get(
        "/dummy/"
    )

    assert response.status_code == 403
    assert response.text == "No API Token Provided"


def test_get_endpoint_with_wrong_api_token():
    response = client.get(
        "/dummy/",
        headers={API_KEY_HEADER_KEY_NAME: WRONG_API_KEY}
    )

    assert response.status_code == 403
    assert response.text == "Wrong API Token"


def test_get_endpoint():
    response = client.get(
        "/dummy/",
        headers={API_KEY_HEADER_KEY_NAME: RIGHT_API_KEY}
    )

    assert response.status_code == 200


# Valid Request Tests
@pytest.mark.parametrize('valid_request_body', test_data['valid_requests'])
def test_valid_requests(valid_request_body):
    request_body = valid_request_body

    response = client.post(
        "/dummy/",
        headers={API_KEY_HEADER_KEY_NAME: RIGHT_API_KEY, "Content-Type": "application/json"},
        json=request_body
    )

    assert response.status_code == 200
    assert len(response.json()['response_values']) == request_body['num_responses']


# Invalid Request Tests
@pytest.mark.parametrize('invalid_request_body', test_data['invalid_requests'].values())
def test_invalid_requests(invalid_request_body):
    request_body = invalid_request_body

    response = client.post(
        "/dummy/",
        headers={API_KEY_HEADER_KEY_NAME: RIGHT_API_KEY, "Content-Type": "application/json"},
        json=request_body
    )

    assert response.status_code == 422
