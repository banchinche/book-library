"""
Testing City GET-POST
"""
import json
import pytest  # noqa

from app.core.config import settings
from app.crud.city import city


def test_get_cities(client, monkeypatch):

    async def mock_get_all(*args, **kwargs):
        return list()

    monkeypatch.setattr(city, 'get_multi', mock_get_all)
    response = client.get(f'{settings.API_V1}/cities/')

    assert response.status_code == 200
    assert response.json() == list()


def test_create_city(client, monkeypatch):
    request_data = {'name': 'London'}
    response_data = {'id': 1, 'name': 'London'}

    async def mock_create_city(*arg, **kwargs):
        instance = request_data.copy()
        instance['id'] = 1  # noqa
        return instance

    monkeypatch.setattr(city, 'create', mock_create_city)

    response = client.post(url=f'{settings.API_V1}/cities/', data=json.dumps(request_data))

    assert response.status_code == 200
    assert response.json() == response_data
