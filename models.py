"""Модуль моделей данных электронной библиотеки."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Protocol

class Summarizable(Protocol):
    """Протокол для демонстрации полиморфизма."""
    def get_summary(self) -> str:
        ...


class LibraryError(Exception):
    """Базовое исключение предметной области библиотеки."""
    pass


@dataclass
class Book:
    """Модель книги."""
    book_id: int
    title: str
    author: str
    year: int
    _is_available: bool = True

    @property
    def is_available(self) -> bool:   #позволяет получать статус книги 
      return self._is_available

    @is_available.setter
    def is_available(self, status: bool) -> None:
        if not isinstance(status, bool):
            raise LibraryError("Статус доступности должен быть булевым значением.")
        self._is_available = status

    def get_summary(self) -> str:
        """Реализация метода протокола Summarizable."""
        status = "Доступна" if self._is_available else "Выдана"
        return f"Книга [{self.book_id}]: '{self.title}' — {self.author} ({self.year}) [{status}]"


@dataclass
class Reader:
    """Модель читателя."""
    reader_id: int
    name: str
    email: str

    def get_summary(self) -> str:
        """Реализация метода протокола Summarizable."""
        return f"Читатель [{self.reader_id}]: {self.name} ({self.email})"


class Loan:
    """Модель выдачи книги (Композиция Book и Reader)."""
    def __init__(self, loan_id: int, book: Book, reader: Reader, issue_date: str):
        if book.is_available is False:
            raise LibraryError(f"Книга '{book.title}' уже выдана другому читателю.")
        
        self.loan_id = loan_id
        self.book = book        # Композиция
        self.reader = reader    # Композиция
        self.issue_date = issue_date
        self.book.is_available = False

    def return_book(self) -> None:
        """Возврат книги в библиотеку."""
        self.book.is_available = True

    def to_dict(self) -> dict:
        return {
            "loan_id": self.loan_id,
            "book_title": self.book.title,
            "reader_name": self.reader.name,
            "issue_date": self.issue_date
        }   
