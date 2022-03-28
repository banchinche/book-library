"""
Testing just failure situations
"""
import json
import pytest

from app.core.config import settings
from app.crud.city import city


def test_get_cities(client, monkeypatch):

    async def mock_get_all(*args, **kwargs):
        return list()

    monkeypatch.setattr(city, 'get_multi', mock_get_all)
    response = client.get(f'{settings.API_V1}/cities')

    assert response.status_code == 200
    assert response.json() == list()
