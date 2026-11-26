from proyecto_isi.extensions import db
from proyecto_isi.models.User import User


def test_register_creates_user(client, app):
    response = client.post(
        "/register",
        data={"name": "Ada Lovelace", "password": "test-password"},
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")
