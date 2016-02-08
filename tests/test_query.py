from query_phenomizer import query

def test_query_ataxia(ataxia):
    res = query([ataxia])
    assert res

def test_query_unicode():
    res = query(["HP:0000252"])
    assert res
