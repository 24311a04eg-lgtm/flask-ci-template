def test_get_posts(client):
    response = client.get('/api/posts')
    assert response.status_code == 200
    assert 'posts' in response.json


def test_create_post_authenticated(client):
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    login = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    token = login.json['access_token']

    response = client.post(
        '/api/posts',
        json={'title': 'Test Post', 'content': 'Test content'},
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    )

    assert response.status_code == 201
    assert response.json['title'] == 'Test Post'
    assert 'id' in response.json


def test_create_post_unauthenticated(client):
    response = client.post('/api/posts',
                           json={'title': 'Test', 'content': 'Test'})
    assert response.status_code == 401


def test_get_single_post(client):
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    login = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    token = login.json['access_token']

    created = client.post(
        '/api/posts',
        json={'title': 'Test', 'content': 'Content'},
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    )
    assert created.status_code == 201
    post_id = created.json['id']

    response = client.get(f'/api/posts/{post_id}')
    assert response.status_code == 200
    assert response.json['title'] == 'Test'
