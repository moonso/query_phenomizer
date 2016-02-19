import os

import pytest

@pytest.fixture(scope="function")
def ataxia(request):
    """Return hpo term for ataxia"""
    return "HP:0002497"

@pytest.fixture(scope="function")
def username(request):
    """Return the username form environmental variable USERNAME"""
    return os.environ['USERNAME']

@pytest.fixture(scope="function")
def password(request):
    """Return the password form environmental variable PASSWORD"""
    return os.environ['PASSWORD']

