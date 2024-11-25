import json
import os
import string
import argparse

from pathlib import Path
from datetime import datetime


FILE_NAME: str = 'library.json'
TEXT_FOR_FILTRATION = (
    '''
Введите код для поиска:
1 - по Автору
2 - по Названию книги
3 - по году
'''
)
TEXT_FOR_UPDATING = (
    '''
Введите код статуса:
1 - в наличии
2 - Выдана
'''
)


def string_in_line(line: str) -> str:
    return line.translate(
        str.maketrans('', '', string.punctuation)).replace(' ', '').lower()


def add_book(FILE_NAME, author: str, title: str, year: int) -> list[str]:
    path = Path(FILE_NAME)
    data = json.loads(path.read_text(encoding='utf-8'))
    if not data['books']:
        num = 1
    else:
        data_check = set(
            string_in_line(
                book['author'] + book['title'] + str(
                    book['year'])) for book in data['books'])
        if string_in_line(author + title + str(year)) in data_check:
            return ['книга уже в списке']
        else:
            num = data['books'][-1]['id'] + 1
    book = dict(
        id=num, author=author, title=title, year=year, status='в наличии')
    data['books'].append(book)
    path.write_text(json.dumps(data), encoding='utf-8')
    return ['Книга добавлена']


def new_book_status(FILE_NAME, id: int, status: int):
    if status == 1:
        status_type = 'В наличии'
    else:
        status_type = 'взято'
    with open(FILE_NAME, 'r+') as file:
        data = json.load(file)
        i: int = 0
        while i < len(data['books']) and i <= id:
            if data['books'][i]['id'] == id:
                if data['books'][i]['status'] == status_type:
                    return ['Нечего обновлять']
                data['books'][i]['status'] = status_type
                file.seek(0)
                json.dump(data, file)
                file.truncate()
                return [f'Новый статус {status_type}']
            i += 1
        else:
            return ['Нет такой книги']


def search_book(FILE_NAME, key: int, filter: str) -> list[str]:
    results: list = []
    if key == 1:
        filter_type = 'author'
    elif key == 2:
        filter_type = 'title'
    else:
        filter_type = 'year'
    path = Path(FILE_NAME)
    data = json.loads(path.read_text(encoding='utf-8'))
    for book in data['books']:
        if string_in_line(
                str(book[filter_type])) == string_in_line(filter):
            results.append(book)
    if results:
        return results
    return ['Ничего не найдено']


def del_book(FILE_NAME, id: int) -> list[str]:
    with open(FILE_NAME, 'r+') as file:
        data = json.load(file)
        i: int = 0
        while i < len(data['books']) and i <= id:
            if data['books'][i]['id'] == id:
                to_del = data['books'][i]
                data['books'].remove(to_del)
                file.seek(0)
                json.dump(data, file)
                file.truncate()
                return [f'{to_del} удалена']
            i += 1
        else:
            return ['Такая книга не найдена']


def main(FILE_NAME, args) -> list[str]:
    # Создать файл, если его нет
    if not os.path.exists(FILE_NAME):
        data = dict(books=[])
        with open(FILE_NAME, 'w', encoding='utf-8') as file:
            json.dump(data, file)
    # Аргумент для функции, которая выводит список всех книг
    if args.list:
        path = Path(FILE_NAME)
        data = json.loads(path.read_text(encoding='utf-8'))
        return data['books']
    # Аргумент для функции, которая удаляет книгу
    if args.delete:
        k = 0
        while k < 1:
            id_to_del = input('Введите id для удаления; ')
            if id_to_del.isdigit():
                return del_book(FILE_NAME, int(id_to_del))
            print('Это не число')
    # Аргумент для функции добавления книги
    if args.create:
        author = input('Введите автора: ')
        title = input('Введите название: ')
        k = 0
        while k < 1:
            year = input('Введите год числом: ')
            if year.isdigit():
                year = int(year)
                if year <= datetime.now().year:
                    return add_book(FILE_NAME, author, title, year)
                else:
                    print('год не может быть из будущего')
            else:
                print('Вы ввели не число')
    # Аргумент обновления статуса книги
    if args.update:
        k = 0
        while k < 1:
            status = input(TEXT_FOR_UPDATING)
            if status.isdigit():
                if int(status) in [1, 2]:
                    while k < 1:
                        id_update = input('Введите id для обновления: ')
                        if id_update.isdigit():
                            return new_book_status(
                                FILE_NAME, int(id_update), int(status))
                        print('Это не число')
                else:
                    print('Нет такого кода')
            else:
                print('Вы ввели не число')
    # Аргумент для фильтрации книг
    if args.filter:
        k = 0
        while k < 1:
            type_id = input(TEXT_FOR_FILTRATION)
            if type_id.isdigit():
                if int(type_id) in [1, 2, 3]:
                    filter = input('Ключ фильтра: ')
                    return search_book(FILE_NAME, int(type_id), filter)
                else:
                    print('Нет такого кода')
            else:
                print('Вы ввели не число')


if __name__ == '__main__':
    # Экземпляра класса ArgumentParser
    parser = argparse.ArgumentParser(description='Библиотека')
    # Аргументы командной строки
    parser.add_argument('-c',
                        '--create',
                        action='store_true',
                        help='Добавить книгу')
    parser.add_argument('-d',
                        '--delete',
                        action='store_true',
                        help='Удалить книгу')
    parser.add_argument('-f',
                        '--filter',
                        action='store_true',
                        help='Поиск книг по маске')
    parser.add_argument('-ls',
                        '--list',
                        action='store_true',
                        help='Вывести все книги в библиотеке')
    parser.add_argument('-u',
                        '--update',
                        action='store_true',
                        help='Обновить статус книги')
    # Парсинг аргументов командной строки
    args = parser.parse_args()
    for result in main(FILE_NAME, args):
        print(result)
