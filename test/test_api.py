import pytest
from app import create_app, db
from config import Config

@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(Config)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def create_user(client):
    def _create_user(username='testuser', password='testpassword', role='user'):
        return client.post('/api/auth/register', json={
            'username': username,
            'password': password,
            'role': role
        })
    return _create_user

@pytest.fixture
def create_admin_user(client):
    def _create_admin_user(username='adminuser', password='adminpassword'):
        return client.post('/api/auth/register', json={
            'username': username,
            'password': password,
            'role': 'admin'
        })
    return _create_admin_user

def test_create_user(client, create_user):
    response = create_user()
    json_data = response.get_json()
    
    assert response.status_code == 201
    assert json_data['success'] is True
    assert json_data['data']['username'] == 'testuser'

def test_get_users(client, create_user):
    create_user()  
    response = client.get('/api/users')
    json_data = response.get_json()

    assert response.status_code == 200
    assert isinstance(json_data['data'], list)
    assert len(json_data['data']) > 0 

def test_get_user(client, create_user):
    create_user()
    response = client.get('/api/users/1')
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data['data']['username'] == 'testuser'

def test_update_user(client, create_user):
    create_user()
    response = client.put('/api/users/1', json={
        'username': 'updateduser',
        'email': 'test@example.com'
    })
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data['data']['username'] == 'updateduser'

def test_delete_user(client, create_user):
    create_user()
    response = client.delete('/api/users/1')

    assert response.status_code == 204

def test_create_item(client, create_admin_user):
    create_admin_user()
    response = client.post('/api/auth/login', json={
        'username': 'adminuser',
        'password': 'adminpassword'
    })
    token = response.get_json()['data']['access_token']

    response = client.post('/api/item', json={
        'name': 'Test Item',
        'price': 10,
        'description': 'A test item'
    }, headers={'Authorization': f'Bearer {token}'})
    
    json_data = response.get_json()

    assert response.status_code == 201
    assert json_data['data']['name'] == 'Test Item'

def test_get_items(client):
    response = client.get('/api/items')
    json_data = response.get_json()

    assert response.status_code == 200
    assert isinstance(json_data['data'], list)

def test_get_item(client):
    response = client.get('/api/items/1')
    json_data = response.get_json()

    assert response.status_code == 200

def test_update_item(client, create_admin_user):
    create_admin_user()
    response = client.post('/api/auth/login', json={
        'username': 'adminuser',
        'password': 'adminpassword'
    })
    token = response.get_json()['data']['access_token']

    item_response = client.post('/api/item', json={
        'name': 'Test Item',
        'price': 10,
        'description': 'A test item'
    }, headers={'Authorization': f'Bearer {token}'})

    item_id = item_response.get_json()['data']['id']

    update_response = client.put(f'/api/items/{item_id}', json={
        'name': 'Updated Test Item',
        'price': 20,
        'description': 'An updated test item'
    }, headers={'Authorization': f'Bearer {token}'})
    
    json_data = update_response.get_json()

    assert update_response.status_code == 200
    assert json_data['data']['name'] == 'Updated Test Item'

def test_delete_item(client, create_admin_user):
    create_admin_user()
    response = client.post('/api/auth/login', json={
        'username': 'adminuser',
        'password': 'adminpassword'
    })
    token = response.get_json()['data']['access_token']

    item_response = client.post('/api/item', json={
        'name': 'Test Item',
        'price': 10,
        'description': 'A test item'
    }, headers={'Authorization': f'Bearer {token}'})

    item_id = item_response.get_json()['data']['id']

    delete_response = client.delete(f'/api/items/{item_id}', headers={'Authorization': f'Bearer {token}'})

    assert delete_response.status_code == 204
