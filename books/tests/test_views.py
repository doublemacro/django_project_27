import pytest
from django.contrib.auth import get_user_model
from django.test.client import Client
from books.models import Book
User = get_user_model()


def test_is_it_working():
    assert True == 1

# def test_should_fail():
#     assert True == False

def test_even_number():
    number = 10
    assert number % 2 == 0

@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        username="test123",
        password="password123"
    )
    assert user.username == "test123"
    assert user.check_password("password123")


# fixture

@pytest.fixture
def user(db) -> User:
    u = User.objects.create_user(
        username="test123",
        password="password123"
    )
    return u

@pytest.fixture
def logged_in_client(user, client: Client) -> Client:
    # cream un browser simulat, logat, care poate face requesturi HTTP:
    client.login(
        username="test123",
        password="password123"
    )

    return client

@pytest.fixture
def book(db):
    user = User.objects.create_user(
        username="useruser",
        password="password123"
    )
    b = Book.objects.create(title="testbook", author="Rowling", user=user)
    return b



def test_list_all_books(logged_in_client):
    # making a HTTP GET request:
    response = logged_in_client.get("/")

    assert response.status_code == 200


def test_does_book_exist(logged_in_client, book):
    # making a HTTP GET request:
    response = logged_in_client.get("/")

    assert response.status_code == 200
    assert "testbook" in str(response.content)


def test_user_book_count(user):
    book1 = Book.objects.create(title="book 1", author="author 1", user=user)
    book2 = Book.objects.create(title="book 2", author="author 2", user=user)
    # conceptual, ce trebuie sa facem aici?
    # trebuie sa ne uitam in baza de date, si sa numaram cartile, care apartin user-ului.
    books = list(Book.objects.filter(user_id=user.pk))
    assert len(books) == 2


def test_user_book_count_html(user):
    book1 = Book.objects.create(title="book 1", author="author 1", user=user)
    book2 = Book.objects.create(title="book 2", author="author 2", user=user)
    book2 = Book.objects.create(title="book 3", author="author 3", user=user)

    # conceptual, ce trebuie sa facem aici?
    # trebuie sa ne uitam in baza de date, si sa numaram cartile, care apartin user-ului.
    books = list(Book.objects.filter(user_id=user.pk))
    assert len(books) == 2
