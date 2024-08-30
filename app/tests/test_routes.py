import json

from fastapi.testclient import TestClient

from app.routes import redis_client


def test_create_parent(client: TestClient):
    """
    Test creating a new parent.
    """
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
    """
    Test creating a new child.
    """
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
    """
    Test retrieving a list of parents.
    """
    response = client.get("/parents/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_read_children(client: TestClient):
    """
    Test retrieving a list of children.
    """
    response = client.get("/children/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_read_specific_parent(client: TestClient):
    """
    Test retrieving a specific parent by ID.
    """
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
    """
    Test retrieving a specific child by ID.
    """
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
    """
    Test updating an existing parent.
    """
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
    """
    Test updating an existing child.
    """
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
    """
    Test deleting an existing parent.
    """
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
    """
    Test deleting an existing child.
    """
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
    """
    Test creating a parent with invalid data.
    """
    response = client.post(
        "/parents/",
        json={"name": "", "age": 40, "email": "not-an-email", "address": ""},
    )
    assert response.status_code == 422  # Unprocessable Entity (validation error)


def test_create_child_with_invalid_data(client: TestClient):
    """
    Test creating a child with invalid data.
    """
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
    """
    Test updating a nonexistent parent.
    """
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
    """
    Test updating a nonexistent child.
    """
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
    """
    Test deleting a parent with associated children. Verifies that the API returns a 200 status code
    and that both the parent and the associated children are deleted.
    """
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
    """
    Test deleting a nonexistent parent.
    """
    response = client.delete("/parents/999999")
    assert response.status_code == 404


def test_delete_nonexistent_child(client: TestClient):
    """
    Test deleting a nonexistent child.
    """
    response = client.delete("/children/999999")
    assert response.status_code == 404


def test_redis_connection(client: TestClient):
    """
    Test Redis connection and basic operations. Verifies that keys can be set,
    retrieved, and deleted from Redis.
    """
    # Define a key-value pair
    test_key = "test_key"
    test_value = "test_value"

    # Set the value in Redis
    redis_client.set(test_key, test_value)

    # Retrieve the value from Redis
    value = redis_client.get(test_key)
    assert value is not None, "Redis did not return a value"
    assert value.decode("utf-8") == test_value, "Redis returned an incorrect value"

    # Delete the key from Redis
    redis_client.delete(test_key)

    # Check if the key has been deleted
    value = redis_client.get(test_key)
    assert value is None, "Redis key was not deleted"


def test_get_parents_stores_in_redis(client: TestClient):
    """
    Test that the list of parents is stored in Redis after a GET request.
    Verifies that the cache is initially empty and is populated after the request.
    """
    # Clear Redis before the test
    redis_client.flushdb()

    # Create a parent
    client.post(
        "/parents/",
        json={
            "name": "Parent Redis Test",
            "age": 40,
            "email": "redis_test@example.com",
            "address": "Testland",
        },
    )

    # Check Redis before GET request
    cached_parents_before = redis_client.get("parents:0:100")
    assert (
        cached_parents_before is None
    ), "Redis cache should be empty before the GET request"

    # Get the list of parents (this should store the result in Redis)
    response = client.get("/parents/")
    assert response.status_code == 200

    # Check Redis after GET request
    cached_parents_after = redis_client.get("parents:0:100")
    assert (
        cached_parents_after is not None
    ), "Redis cache should store the parents list after the GET request"

    # Deserialize the data from Redis and check if it matches the response
    cached_parents = json.loads(cached_parents_after.decode("utf-8"))
    response_data = response.json()
    assert (
        cached_parents == response_data
    ), "Cached data in Redis should match the response data"

    # Clean up by flushing Redis
    redis_client.flushdb()


def test_delete_parent_invalidates_cache(client: TestClient):
    """
    Test that deleting a parent invalidates the cached list of parents in Redis.
    Verifies that the cache is cleared after a parent is deleted.
    """
    # Step 1: Ensure Redis is clear
    redis_client.flushdb()

    # Step 2: Create a parent to populate the cache
    parent_response = client.post(
        "/parents/",
        json={
            "name": "Parent 6",
            "age": 45,
            "email": "user6@example.com",
            "address": "Italy",
        },
    )
    parent_id = parent_response.json()["id"]
    assert parent_response.status_code == 201

    # Step 3: Access the parents to store them in the cache
    response = client.get("/parents/")
    assert response.status_code == 200

    # Step 4: Verify that the cache is populated
    cached_parents_before = redis_client.get("parents:0:100")
    assert (
        cached_parents_before is not None
    ), "Redis cache should store the parents list"

    # Step 5: Delete the parent, which should invalidate the cache
    delete_response = client.delete(f"/parents/{parent_id}")
    assert delete_response.status_code == 200

    # Step 6: Check if the cache has been invalidated
    cached_parents_after = redis_client.get("parents:0:100")
    assert (
        cached_parents_after is None
    ), "Redis cache should be invalidated after deleting a parent"

    # Clean up by flushing Redis
    redis_client.flushdb()
