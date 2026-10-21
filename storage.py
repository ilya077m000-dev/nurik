"""Модуль работы с файлами CSV и JSON (импорт/экспорт/генераторы)."""

import csv
import json
import logging
from typing import Generator, List
from models import Book, Reader, LibraryError

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def load_books_from_csv(file_path: str) -> Generator[Book, None, None]:
    """Ленивое чтение книг из CSV с помощью генератора."""
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    yield Book(
                        book_id=int(row['book_id']),
                        title=row['title'].strip(),
                        author=row['author'].strip(),
                        year=int(row['year']),
                        _is_available=row.get('is_available', 'True').lower() == 'true'
                    )
                except (ValueError, KeyError) as err:
                    logging.warning(f"Пропущена некорректная строка в CSV: {row}. Ошибка: {err}")
    except FileNotFoundError:
        logging.error(f"Файл {file_path} не найден.")
        raise LibraryError(f"Файл {file_path} не найден.")


def export_report_to_json(data: List[dict], file_path: str) -> None:
    """Сохранение отчета в JSON."""
    try:
        with open(file_path, mode='w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"Отчет успешно сохранен в {file_path}")
    except IOError as e:
        logging.error(f"Ошибка записи отчета в JSON: {e}")
        raise LibraryError("Не удалось сохранить отчет.")