from pymongo import MongoClient
from result import UnwrapError

from pykit.check import check
from pykit.err import NotFoundErr, ValueErr
from pykit.query import AggQuery, Query, UpdQuery

def test_updq_create_err():
    check.expect(UpdQuery, ValueErr, {"wow": 1})

def test_aggq_create_err():
    check.expect(AggQuery, ValueErr, {"wow": 1})

def test_get_operator_val():
    q = UpdQuery({
        "$set": {"price": 1.0},
        "$push": {"shop_ids": 15},
        "$unset": {"name": 1}
    })
    assert q.get_operator_val("$push").unwrap() == {"shop_ids": 15}
    check.expect(q.get_operator_val, NotFoundErr, "$pull")
    check.expect(q.get_operator_val, ValueErr, "hello")

def test_get_operator_val_incorrect_query():
    q = UpdQuery({
        "$set": {"price": 1.0}
    })
    q["hello"] = 1
    check.expect(q.get_operator_val, ValueErr, "$set")

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

def test_agg():
    client = MongoClient("localhost", 9006)
    db = client.pykit_test
    client.drop_database(db)

    collection = db.test_agg
    collection.insert_many([
        {
            "name": "pizza",
            "price": 10.0,
        },
        {
            "name": "cola",
            "price": 2.5,
        },
        {
            "name": "donut",
            "price": 3.25,
        },
    ])

    aggq = AggQuery.create(
        {
            "$match": {
                "price": {
                    "$gte": 3.25,
                },
            },
        },
        {
            "$sort": {
                "price": -1,
            },
        },
    )
    cursor = aggq.apply(collection)
    docs = list(cursor)

    assert len(docs) == 2
    assert docs[0]["name"] == "pizza"
    assert docs[1]["name"] == "donut"

    client.drop_database(db)
