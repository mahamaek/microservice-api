from fastapi.testclient import TestClient
from orders.app import app

test_client = TestClient(app=app)


def test_create_order_fails():
    payload = {
        'order': [
            {
                'product': 'coffee'
            }
        ]
    }
    respose = test_client.post('/orders', json=payload)
    assert respose.status_code == 422


def test_create_order_succeeds():
    payload = {
        'order': [
            {
                'product': 'coffee',
                'size': 'big'
            }
        ]
    }
    respose = test_client.post('/orders', json=payload)
    assert respose.status_code == 201
