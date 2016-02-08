import pytest

@pytest.fixture(scope="function")
def ataxia(request):
    """Return hpo term for ataxia"""
    return "HP:0002497"