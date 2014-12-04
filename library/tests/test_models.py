import pytest

from django.db import IntegrityError

from ..models import Book, BookSpecimen
from .factories import BookFactory

pytestmark = pytest.mark.django_db


def test_deleting_book_sould_delete_specimen_too(specimen):
    assert BookSpecimen.objects.all()
    assert Book.objects.all()
    specimen.book.delete()
    assert not BookSpecimen.objects.all()
    assert not Book.objects.all()


def test_deleting_specimen_sould_not_delete_book(specimen):
    assert BookSpecimen.objects.all()
    assert Book.objects.all()
    specimen.delete()
    assert not BookSpecimen.objects.all()
    assert Book.objects.all()


def test_it_should_be_possible_to_have_more_than_one_isbn_null_value():
    assert len(Book.objects.filter(isbn__isnull=True)) == 0
    BookFactory(isbn=None)
    BookFactory(isbn=None)
    assert len(Book.objects.filter(isbn__isnull=True)) == 2


def test_it_should__not_be_possible_to_have_twice_the_same_isbn():
    assert len(Book.objects.filter(isbn__isnull=True)) == 0
    BookFactory(isbn='123456')
    with pytest.raises(IntegrityError):
        BookFactory(isbn='123456')
    # FIXME Raises TransactionManagementError if do the following assert
    # assert len(Book.objects.filter(isbn__isnull=True)) == 1
