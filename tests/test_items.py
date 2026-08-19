def test_create_and_list_item(client):
    r = client.post("/items", json={"name": "widget"})
    assert r.status_code == 201
    assert r.json()["name"] == "widget"

    r = client.get("/items")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_get_missing_item_returns_404(client):
    r = client.get("/items/999")
    assert r.status_code == 404
