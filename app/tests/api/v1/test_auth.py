"""
Testing just failure situations
"""
import json
import pytest  # noqa

from app.core.config import settings


# TODO: research why no relations in CI database
def test_fail_login(client):
    test_request_data = {'email': 'no_such_user@example.com', 'password': 'asd'}

    response = client.post(
        url=f'{settings.API_V1}/auth/login',
        data=json.dumps(test_request_data)
    )

    assert response.status_code == 400


def test_fail_register_format(client):
    test_request_data = {'email': 'asd.example.com', 'password': 'asd'}
    response = client.post(
        url=f'{settings.API_V1}/auth/register',
        data=json.dumps(test_request_data)
    )

    assert response.status_code == 422


# TODO: research why no relations in CI database
def test_fail_register_no_such_city(client):
    test_request_data = {
        'first_name': 'string',
        'last_name': 'string',
        'birth_date': '2022-03-28',
        'email': 'user@example.com',
        'city_id': 666,
        'password': 'string'
    }
    response = client.post(
        url=f'{settings.API_V1}/auth/register',
        data=json.dumps(test_request_data)
    )

    assert response.status_code == 404


def test_unauthorized_access(client):
    response = client.get(url=f'{settings.API_V1}/authors')
    assert response.status_code == 403
