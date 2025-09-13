import pytest
from dotenv import find_dotenv, load_dotenv


@pytest.fixture(autouse=True, scope='session')
def setup():
    load_dotenv(find_dotenv(), override=False)

    yield
