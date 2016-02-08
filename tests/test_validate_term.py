from query_phenomizer import validate_term

def test_validate_ataxia(ataxia):
    assert validate_term(ataxia) == True