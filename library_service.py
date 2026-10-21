"""Модуль бизнес-логики: собственный поиск, сортировка и полиморфизм."""

import logging
from typing import List
from models import Book, Loan, Summarizable, LibraryError


class LibraryService:
    def __init__(self):
        self.books: List[Book] = []
        self.loans: List[Loan] = []

    def add_book(self, book: Book) -> None:
        self.books.append(book)

    # --- СОБСТВЕННЫЙ ПОИСК (Линейный поиск O(n)) ---
    def custom_search_by_title(self, title_query: str) -> List[Book]:
        """
        Собственная реализация поиска книги по фрагменту названия.
        Предусловие: title_query — непустая строка.
        Сложность: O(n) по времени, O(k) по памяти (где k — количество найденных совпадений).
        """
        if not title_query or not title_query.strip():
            return []
        
        results: List[Book] = []
        query_lower = title_query.lower().strip()
        
        for book in self.books:
            if query_lower in book.title.lower():
                results.append(book)
                
        return results

    # --- СОБСТВЕННАЯ СОРТИРОВКА (Пузырьковая сортировка / Bubble Sort O(n^2)) ---
    def custom_sort_by_year(self, reverse: bool = False) -> List[Book]:
        """
        Собственная реализация сортировки книг по году издания (Bubble Sort).
        Предусловие: список книг не пуст.
        Сложность: O(n^2) по времени в худшем/среднем случае, O(1) по доп. памяти.
        """
        sorted_books = list(self.books)  # создаем копию
        n = len(sorted_books)
        
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                condition = (sorted_books[j].year < sorted_books[j + 1].year) if reverse else (sorted_books[j].year > sorted_books[j + 1].year)
                if condition:
                    sorted_books[j], sorted_books[j + 1] = sorted_books[j + 1], sorted_books[j]
                    swapped = True
            if not swapped:
                break
                
        return sorted_books

    # --- ДЕМОНСТРАЦИЯ ПОЛИМОРФИЗМА ---
    def print_item_summary(self, item: Summarizable) -> str:
        """Работает с любым объектом, реализующим метод get_summary() (Book, Reader)."""
        return item.get_summary()