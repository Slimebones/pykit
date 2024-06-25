from pykit.check import check
from pykit.err import ValueErr
from pykit.query import Query


def test_disallow():
    q = Query({"sid": "hello", "$set": {"price": 10}})
    new_q = q.disallow("sid")
    assert q != new_q
    assert new_q["$set"] == q["$set"]
    assert "sid" not in new_q

def test_disallow_upd_operator():
    q = Query({"sid": "hello", "$set": {"price": 10}})
    check.expect(q.disallow, ValueErr, "$set")

def test_disallow_err_mode():
    q = Query({"sid": "hello", "$set": {"price": 10}})
    check.expect(q.disallow, ValueErr, "sid", raise_mode="err")
