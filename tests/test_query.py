from pymongo import MongoClient

from ryz.check import check
from ryz.err import NotFoundErr, ValErr
from ryz.query import AggQuery, Query, UpdQuery


def test_updq_create_err():
    check.expect(UpdQuery, ValErr, {"wow": 1})

def test_aggq_create_err():
    check.expect(AggQuery, ValErr, {"wow": 1})

def test_get_operator_val():
    q = UpdQuery({
        "$set": {"price": 1.0},
        "$push": {"shop_ids": 15},
        "$unset": {"name": 1},
    })
    assert q.get_operator_val("$push").unwrap() == {"shop_ids": 15}
    check.expect(q.get_operator_val, NotFoundErr, "$pull")
    check.expect(q.get_operator_val, ValErr, "hello")

def test_get_operator_val_incorrect_query():
    q = UpdQuery({
        "$set": {"price": 1.0},
    })
    q["hello"] = 1
    check.expect(q.get_operator_val, ValErr, "$set")

def test_disallow():
    q = Query({"sid": "hello", "$set": {"price": 10}})
    new_q = q.disallow("sid")
    assert q != new_q
    assert new_q["$set"] == q["$set"]
    assert "sid" not in new_q

def test_disallow_nested():
    q = Query({"sid": "hello", "$set": {"price": 10}})
    new_q = q.disallow("price")
    assert q != new_q
    assert "sid" in new_q
    assert new_q["$set"] == {}

def test_disallow_upd_operator():
    q = Query({"sid": "hello", "$set": {"price": 10}})
    check.expect(q.disallow, ValErr, "$set")

def test_disallow_err_mode():
    q = Query({"sid": "hello", "$set": {"price": 10}})
    check.expect(q.disallow, ValErr, "sid", raise_mode="err")

def test_agg():
    client = MongoClient("localhost", 9006)
    db = client.ryz_test
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
