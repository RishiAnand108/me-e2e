import uuid


VALID_PASSWORD = "SecurePass123!"
INVALID_PASSWORD = "WrongPass123!"


def generate_email():
    return f"test_{uuid.uuid4().hex[:8]}@example.com"


# ---------------------------
# REGISTER INTEGRATION TESTS
# ---------------------------

def test_register_missing_all_fields(client):
    response = client.register(None, None, None, None)
    assert response.status_code in (400, 422)


def test_register_missing_email(client):
    response = client.register(
        first_name="John",
        last_name="Doe",
        email=None,
        password=VALID_PASSWORD
    )
    assert response.status_code in (400, 422)


def test_register_with_valid_data(client):
    email = generate_email()
    response = client.register(
        first_name="John",
        last_name="Doe",
        email=email,
        password=VALID_PASSWORD
    )
    assert response.status_code in (200, 201, 409)


# ---------------------------
# LOGIN INTEGRATION TESTS
# ---------------------------

def test_login_with_invalid_email_and_password(client):
    response = client.login(
        email="fake@example.com",
        password=INVALID_PASSWORD
    )
    assert response.status_code in (401, 404)


def test_login_with_invalid_email_valid_password(client):
    response = client.login(
        email="notexist@example.com",
        password=VALID_PASSWORD
    )
    assert response.status_code in (401, 404)


def test_login_with_valid_email_invalid_password(client):
    email = generate_email()

    client.register(
        first_name="Test",
        last_name="User",
        email=email,
        password=VALID_PASSWORD
    )

    response = client.login(
        email=email,
        password=INVALID_PASSWORD
    )
    assert response.status_code == 401


def test_login_with_valid_email_and_password(client):
    email = generate_email()

    client.register(
        first_name="Test",
        last_name="User",
        email=email,
        password=VALID_PASSWORD
    )

    response = client.login(
        email=email,
        password=VALID_PASSWORD
    )

    assert response.status_code == 200
    assert "token" in response.text.lower()
