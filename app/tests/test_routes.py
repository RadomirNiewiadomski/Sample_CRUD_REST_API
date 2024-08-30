from fastapi.testclient import TestClient


def test_create_parent(client: TestClient):
    response = client.post(
        "/parents/",
        json={
            "name": "Parent 1",
            "age": 40,
            "email": "user@example.com",
            "address": "Poland",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Parent 1"
    assert data["age"] == 40
    assert "id" in data


def test_create_child(client: TestClient):
    parent_response = client.post(
        "/parents/",
        json={
            "name": "Parent 2",
            "age": 35,
            "email": "user2@example.com",
            "address": "Germany",
        },
    )
    parent_id = parent_response.json()["id"]
    response = client.post(
        "/children/",
        json={"name": "Child 1", "age": 10, "hobby": "Drawing", "parent_id": parent_id},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Child 1"
    assert data["age"] == 10
    assert "id" in data


def test_read_parents(client: TestClient):
    response = client.get("/parents/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_read_children(client: TestClient):
    response = client.get("/children/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_read_specific_parent(client: TestClient):
    parent_response = client.post(
        "/parents/",
        json={
            "name": "Parent 3",
            "age": 50,
            "email": "user3@example.com",
            "address": "UK",
        },
    )
    parent_id = parent_response.json()["id"]
    response = client.get(f"/parents/{parent_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == parent_id
    assert data["name"] == "Parent 3"


def test_read_specific_child(client: TestClient):
    parent_response = client.post(
        "/parents/",
        json={
            "name": "Parent for Child 1",
            "age": 35,
            "email": "parent_for_child1@example.com",
            "address": "Canada",
        },
    )
    parent_id = parent_response.json()["id"]
    child_response = client.post(
        "/children/",
        json={"name": "Child 1", "age": 10, "hobby": "Drawing", "parent_id": parent_id},
    )
    child_id = child_response.json()["id"]

    response = client.get(f"/children/{child_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == child_id
    assert data["name"] == "Child 1"


def test_update_parent(client: TestClient):
    parent_response = client.post(
        "/parents/",
        json={
            "name": "Parent 4",
            "age": 45,
            "email": "user4@example.com",
            "address": "France",
        },
    )
    parent_id = parent_response.json()["id"]
    response = client.put(
        f"/parents/{parent_id}",
        json={
            "name": "Updated Parent 4",
            "age": 46,
            "email": "updated_user4@example.com",
            "address": "Updated France",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == parent_id
    assert data["name"] == "Updated Parent 4"


def test_update_child(client: TestClient):
    parent_response = client.post(
        "/parents/",
        json={
            "name": "Parent for Child 2",
            "age": 40,
            "email": "parent_for_child2@example.com",
            "address": "Australia",
        },
    )
    parent_id = parent_response.json()["id"]
    child_response = client.post(
        "/children/",
        json={"name": "Child 2", "age": 12, "hobby": "Reading", "parent_id": parent_id},
    )
    child_id = child_response.json()["id"]

    response = client.put(
        f"/children/{child_id}",
        json={
            "name": "Updated Child 2",
            "age": 13,
            "hobby": "Writing",
            "parent_id": parent_id,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == child_id
    assert data["name"] == "Updated Child 2"


def test_delete_parent(client: TestClient):
    parent_response = client.post(
        "/parents/",
        json={
            "name": "Parent 5",
            "age": 55,
            "email": "user5@example.com",
            "address": "Spain",
        },
    )
    parent_id = parent_response.json()["id"]
    response = client.delete(f"/parents/{parent_id}")
    assert response.status_code == 200
    data = response.json()
    assert data == {"detail": f"Parent with ID {parent_id} deleted successfully"}

    # Verify the parent has been deleted
    parent_check_response = client.get(f"/parents/{parent_id}")
    assert parent_check_response.status_code == 404


def test_delete_child(client: TestClient):
    parent_response = client.post(
        "/parents/",
        json={
            "name": "Parent for Child 3",
            "age": 38,
            "email": "parent_for_child3@example.com",
            "address": "Brazil",
        },
    )
    parent_id = parent_response.json()["id"]
    child_response = client.post(
        "/children/",
        json={"name": "Child 3", "age": 15, "hobby": "Gaming", "parent_id": parent_id},
    )
    child_id = child_response.json()["id"]

    response = client.delete(f"/children/{child_id}")
    assert response.status_code == 200
    data = response.json()
    assert data == {"detail": f"Child with ID {child_id} deleted successfully"}

    # Verify the child has been deleted
    child_check_response = client.get(f"/children/{child_id}")
    assert child_check_response.status_code == 404


def test_create_parent_invalid_data(client: TestClient):
    response = client.post(
        "/parents/",
        json={"name": "", "age": 40, "email": "not-an-email", "address": ""},
    )
    assert response.status_code == 422  # Unprocessable Entity (validation error)


def test_create_child_with_invalid_data(client: TestClient):
    parent_response = client.post(
        "/parents/",
        json={
            "name": "Parent for Invalid Child",
            "age": 45,
            "email": "parent_for_invalid_child@example.com",
            "address": "Japan",
        },
    )
    parent_id = parent_response.json()["id"]

    response = client.post(
        "/children/",
        json={"name": "", "age": "not-an-age", "hobby": "", "parent_id": parent_id},
    )
    assert response.status_code == 422  # Unprocessable Entity (validation error)


def test_update_nonexistent_parent(client: TestClient):
    response = client.put(
        "/parents/999999",
        json={
            "name": "Nonexistent Parent",
            "age": 40,
            "email": "nonexistent@example.com",
            "address": "Nowhere",
        },
    )
    assert response.status_code == 404


def test_update_nonexistent_child(client: TestClient):
    response = client.put(
        "/children/999999",
        json={
            "name": "Nonexistent Child",
            "age": 10,
            "hobby": "Playing",
            "parent_id": 1,
        },
    )
    assert response.status_code == 404


def test_delete_parent_with_children(client: TestClient):
    parent_response = client.post(
        "/parents/",
        json={
            "name": "Parent with Child",
            "age": 35,
            "email": "parentwithchild@example.com",
            "address": "Italy",
        },
    )
    assert parent_response.status_code == 201
    parent_id = parent_response.json()["id"]

    child_response = client.post(
        "/children/",
        json={
            "name": "Child of Parent",
            "age": 8,
            "hobby": "Soccer",
            "parent_id": parent_id,
        },
    )
    assert child_response.status_code == 201
    child_id = child_response.json()["id"]

    response = client.delete(f"/parents/{parent_id}")
    assert response.status_code == 200
    data = response.json()
    assert data == {"detail": f"Parent with ID {parent_id} deleted successfully"}

    # Step 4: Verify the parent has been deleted
    parent_check_response = client.get(f"/parents/{parent_id}")
    assert parent_check_response.status_code == 404

    # Step 5: Verify the child has also been deleted
    child_check_response = client.get(f"/children/{child_id}")
    assert child_check_response.status_code == 404


def test_delete_nonexistent_parent(client: TestClient):
    response = client.delete("/parents/999999")
    assert response.status_code == 404


def test_delete_nonexistent_child(client: TestClient):
    response = client.delete("/children/999999")
    assert response.status_code == 404
