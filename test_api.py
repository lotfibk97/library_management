import logging


def test_register_user(client):
    unique_username = "testuser_register"
    response = client.post(
        "/users/",
        json={"username": unique_username, "password": "password123", "role": "USER"},
    )
    assert response.status_code == 200, f"Failed to register user: {response.json()}"
    data = response.json()
    assert "user_id" in data
    assert data["username"] == unique_username
    assert "api_key" in data


def test_login(client):
    unique_username = "testuser_login"
    client.post(
        "/users/",
        json={"username": unique_username, "password": "password123", "role": "USER"},
    )
    response = client.post(
        "/users/login", json={"username": unique_username, "password": "password123"}
    )
    assert response.status_code == 200, f"Failed to login: {response.json()}"
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_create_book(client, test_db):
    unique_librarian = "librarian_create"
    response = client.post(
        "/users/",
        json={
            "username": unique_librarian,
            "password": "password123",
            "role": "LIBRARIAN",
        },
    )
    assert response.status_code == 200, f"Failed to create librarian: {response.json()}"
    data = response.json()
    logging.info(f"Created librarian: {data}")
    api_key = data["api_key"]
    from models.book import Category

    category = Category(name="Fiction")
    test_db.add(category)
    test_db.commit()
    response = client.post(
        "/books/",
        json={
            "title": "Test Book",
            "author": "Author",
            "category_id": category.category_id,
            "isbn": "1234567890",
            "total_copies": 5,
            "available_copies": 5,
        },
        headers={"api-key": api_key},
    )
    assert response.status_code == 200, f"Failed to create book: {response.json()}"
    data = response.json()
    assert "book_id" in data
    assert data["title"] == "Test Book"


def test_update_book(client, test_db):
    unique_librarian = "librarian_update"
    response = client.post(
        "/users/",
        json={
            "username": unique_librarian,
            "password": "password123",
            "role": "LIBRARIAN",
        },
    )
    assert response.status_code == 200, f"Failed to create librarian: {response.json()}"
    data = response.json()
    logging.info(f"Created librarian: {data}")
    api_key = data["api_key"]
    from models.book import Category

    category = Category(name="Fiction")
    test_db.add(category)
    test_db.commit()
    book_response = client.post(
        "/books/",
        json={
            "title": "Test Book",
            "author": "Author",
            "category_id": category.category_id,
            "isbn": "1234567890",
            "total_copies": 5,
            "available_copies": 5,
        },
        headers={"api-key": api_key},
    )
    assert book_response.status_code == 200, (
        f"Failed to create book: {book_response.json()}"
    )
    book_id = book_response.json()["book_id"]
    response = client.put(
        f"/books/{book_id}",
        json={"title": "Updated Book"},
        headers={"api-key": api_key},
    )
    assert response.status_code == 200, f"Failed to update book: {response.json()}"
    assert response.json()["title"] == "Updated Book"


def test_delete_book(client, test_db):
    unique_librarian = "librarian_delete"
    response = client.post(
        "/users/",
        json={
            "username": unique_librarian,
            "password": "password123",
            "role": "LIBRARIAN",
        },
    )
    assert response.status_code == 200, f"Failed to create librarian: {response.json()}"
    data = response.json()
    logging.info(f"Created librarian: {data}")
    api_key = data["api_key"]
    from models.book import Category

    category = Category(name="Fiction")
    test_db.add(category)
    test_db.commit()
    book_response = client.post(
        "/books/",
        json={
            "title": "Test Book",
            "author": "Author",
            "category_id": category.category_id,
            "isbn": "1234567890",
            "total_copies": 5,
            "available_copies": 5,
        },
        headers={"api-key": api_key},
    )
    assert book_response.status_code == 200, (
        f"Failed to create book: {book_response.json()}"
    )
    book_id = book_response.json()["book_id"]
    response = client.delete(f"/books/{book_id}", headers={"api-key": api_key})
    assert response.status_code == 200, f"Failed to delete book: {response.json()}"
    assert response.json()["message"] == "Book deleted"


def test_search_books(client, test_db):
    unique_user = "user_search"
    unique_librarian = "librarian_search"
    response = client.post(
        "/users/",
        json={
            "username": unique_librarian,
            "password": "password123",
            "role": "LIBRARIAN",
        },
    )
    assert response.status_code == 200, f"Failed to create librarian: {response.json()}"
    data = response.json()
    logging.info(f"Created librarian: {data}")
    librarian_api_key = data["api_key"]
    from models.book import Category

    category = Category(name="Fiction")
    test_db.add(category)
    test_db.commit()
    book_response = client.post(
        "/books/",
        json={
            "title": "Test Book",
            "author": "Author",
            "category_id": category.category_id,
            "isbn": "1234567890",
            "total_copies": 5,
            "available_copies": 5,
        },
        headers={"api-key": librarian_api_key},
    )
    assert book_response.status_code == 200, (
        f"Failed to create book: {book_response.json()}"
    )
    response = client.post(
        "/users/",
        json={"username": unique_user, "password": "password123", "role": "USER"},
    )
    assert response.status_code == 200, f"Failed to create user: {response.json()}"
    api_key = response.json()["api_key"]
    response = client.get("/books/?title=Test", headers={"api-key": api_key})
    assert response.status_code == 200, f"Failed to search books: {response.json()}"
    assert len(response.json()) > 0
    assert response.json()[0]["title"] == "Test Book"


def test_borrow_book(client, test_db):
    unique_librarian = "librarian_borrow"
    unique_user = "user_borrow"
    response = client.post(
        "/users/",
        json={
            "username": unique_librarian,
            "password": "password123",
            "role": "LIBRARIAN",
        },
    )
    assert response.status_code == 200, f"Failed to create librarian: {response.json()}"
    data = response.json()
    logging.info(f"Created librarian: {data}")
    librarian_api_key = data["api_key"]
    from models.book import Category

    category = Category(name="Fiction")
    test_db.add(category)
    test_db.commit()
    book_response = client.post(
        "/books/",
        json={
            "title": "Test Book",
            "author": "Author",
            "category_id": category.category_id,
            "isbn": "1234567890",
            "total_copies": 5,
            "available_copies": 5,
        },
        headers={"api-key": librarian_api_key},
    )
    assert book_response.status_code == 200, (
        f"Failed to create book: {book_response.json()}"
    )
    book_id = book_response.json()["book_id"]
    response = client.post(
        "/users/",
        json={"username": unique_user, "password": "password123", "role": "USER"},
    )
    assert response.status_code == 200, f"Failed to create user: {response.json()}"
    user_api_key = response.json()["api_key"]
    user_id = response.json()["user_id"]
    response = client.post(
        "/borrowing/borrow",
        json={"user_id": user_id, "book_id": book_id},
        headers={"api-key": user_api_key},
    )
    assert response.status_code == 200, f"Failed to borrow book: {response.json()}"
    assert "borrow_id" in response.json()


def test_return_book(client, test_db):
    unique_librarian = "librarian_return"
    unique_user = "user_return"
    response = client.post(
        "/users/",
        json={
            "username": unique_librarian,
            "password": "password123",
            "role": "LIBRARIAN",
        },
    )
    assert response.status_code == 200, f"Failed to create librarian: {response.json()}"
    data = response.json()
    logging.info(f"Created librarian: {data}")
    librarian_api_key = data["api_key"]
    from models.book import Category

    category = Category(name="Fiction")
    test_db.add(category)
    test_db.commit()
    book_response = client.post(
        "/books/",
        json={
            "title": "Test Book",
            "author": "Author",
            "category_id": category.category_id,
            "isbn": "1234567890",
            "total_copies": 5,
            "available_copies": 5,
        },
        headers={"api-key": librarian_api_key},
    )
    assert book_response.status_code == 200, (
        f"Failed to create book: {book_response.json()}"
    )
    book_id = book_response.json()["book_id"]
    response = client.post(
        "/users/",
        json={"username": unique_user, "password": "password123", "role": "USER"},
    )
    assert response.status_code == 200, f"Failed to create user: {response.json()}"
    user_api_key = response.json()["api_key"]
    user_id = response.json()["user_id"]
    borrow_response = client.post(
        "/borrowing/borrow",
        json={"user_id": user_id, "book_id": book_id},
        headers={"api-key": user_api_key},
    )
    assert borrow_response.status_code == 200, (
        f"Failed to borrow book: {borrow_response.json()}"
    )
    borrow_id = borrow_response.json()["borrow_id"]
    response = client.post(
        f"/borrowing/return/{borrow_id}",
        json={"return_date": "2023-01-01T00:00:00"},
        headers={"api-key": user_api_key},
    )
    assert response.status_code == 200, f"Failed to return book: {response.json()}"
    assert response.json()["status"] == "RETURNED"  # Updated to uppercase


def test_borrowing_history(client, test_db):
    unique_librarian = "librarian_history"
    unique_user = "user_history"
    response = client.post(
        "/users/",
        json={
            "username": unique_librarian,
            "password": "password123",
            "role": "LIBRARIAN",
        },
    )
    assert response.status_code == 200, f"Failed to create librarian: {response.json()}"
    data = response.json()
    logging.info(f"Created librarian: {data}")
    librarian_api_key = data["api_key"]
    from models.book import Category

    category = Category(name="Fiction")
    test_db.add(category)
    test_db.commit()
    book_response = client.post(
        "/books/",
        json={
            "title": "Test Book",
            "author": "Author",
            "category_id": category.category_id,
            "isbn": "1234567890",
            "total_copies": 5,
            "available_copies": 5,
        },
        headers={"api-key": librarian_api_key},
    )
    assert book_response.status_code == 200, (
        f"Failed to create book: {book_response.json()}"
    )
    book_id = book_response.json()["book_id"]
    response = client.post(
        "/users/",
        json={"username": unique_user, "password": "password123", "role": "USER"},
    )
    assert response.status_code == 200, f"Failed to create user: {response.json()}"
    user_api_key = response.json()["api_key"]
    user_id = response.json()["user_id"]
    borrow_response = client.post(
        "/borrowing/borrow",
        json={"user_id": user_id, "book_id": book_id},
        headers={"api-key": user_api_key},
    )
    assert borrow_response.status_code == 200, (
        f"Failed to borrow book: {borrow_response.json()}"
    )
    response = client.get("/borrowing/history", headers={"api-key": user_api_key})
    assert response.status_code == 200, (
        f"Failed to get borrowing history: {response.json()}"
    )
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
