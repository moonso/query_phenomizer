from query_phenomizer import validate_term

def test_validate_ataxia(ataxia, username, password):
    assert validate_term(username, password, ataxia) == True