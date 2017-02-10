from query_phenomizer import query

def test_query_ataxia(ataxia, username, password):
    res = query(username, password, ataxia)
    assert res

def test_query_unicode(username, password):
    res = query(username, password, "HP:0000252")
    assert res
