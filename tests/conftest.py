import pytest


@pytest.fixture(scope='session')
def setup():
    print("SETUP: TODO")

    yield

    print("CLEAN UP TODO")
