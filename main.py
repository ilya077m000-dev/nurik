"""Главный модуль запуска консольного приложения."""

import os
from models import Book, Reader, Loan, LibraryError
from storage import load_books_from_csv, export_report_to_json
from library_service import LibraryService


def main():
    service = LibraryService()
    
    # Загрузка данных из CSV (если файл существует)
    csv_file = "data/books.csv"
    if os.path.exists(csv_file):
        print("Загрузка книг из CSV...")
        for book in load_books_from_csv(csv_file):
            service.add_book(book)
    else:
        # Тестовые данные по умолчанию
        service.add_book(Book(1, "Преступление и наказание", "Ф. Достоевский", 1866))
        service.add_book(Book(2, "Мастер и Маргарита", "М. Булгаков", 1967))
        service.add_book(Book(3, "Война и мир", "Л. Толстой", 1869))

    while True:
        print("\n=== ЭЛЕКТРОННАЯ БИБЛИОТЕКА ===")
        print("1. Показать все книги")
        print("2. Искать книгу по название (Собственный поиск)")
        print("3. Отсортировать книги по году издания (Собственная сортировка)")
        print("4. Проверить полиморфизм (Книга / Читатель)")
        print("5. Экспортировать отчет в JSON")
        print("0. Выход")
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            if not service.books:
                print("Коллекция книг пуста.")
            for b in service.books:
                print(b.get_summary())
                
        elif choice == "2":
            query = input("Введите название или его часть для поиска: ")
            results = service.custom_search_by_title(query)
            print(f"\nНайдено совпадений: {len(results)}")
            for b in results:
                print(b.get_summary())
                
        elif choice == "3":
            sorted_books = service.custom_sort_by_year()
            print("\nКниги, отсортированные по году издания (от старых к новым):")
            for b in sorted_books:
                print(f"{b.year} г. — {b.title} ({b.author})")
                
        elif choice == "4":
            book = Book(99, "Чистый код", "Р. Мартин", 2008)
            reader = Reader(1, "Иван Иванов", "ivan@example.com")
            print("\n[Полиморфизм через общий метод get_summary()]:")
            print(service.print_item_summary(book))
            print(service.print_item_summary(reader))
            
        elif choice == "5":
            report_data = [b.__dict__ for b in service.books]
            os.makedirs("data", exist_ok=True)
            try:
                export_report_to_json(report_data, "data/report.json")
                print("Отчет 'data/report.json' успешно сформирован.")
            except LibraryError as e:
                print(f"Ошибка при формировании отчета: {e}")
                
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()