import pytest
from proyecto_isi import create_app


@pytest.fixture
def app():
    app = create_app()

    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
    )

    return app


@pytest.fixture
def client(app):
    return app.test_client()


