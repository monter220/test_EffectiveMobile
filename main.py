import json
import os
import string

from pathlib import Path
from datetime import datetime


def string_in_line(line: str) -> str:
    return line.translate(
        str.maketrans('', '', string.punctuation)).replace(' ', '').lower()


if not os.path.exists('test.json'):
    data = dict(books=[])
    with open('test.json', "w", encoding="utf-8") as file:
        json.dump(data, file)


def add_book(author, title, year):
    path = Path('test.json')
    data = json.loads(path.read_text(encoding='utf-8'))
    if not data['books']:
        num = 1
    else:
        data_check = set(
            string_in_line(
                r['author']+r['title']+str(r['year'])) for r in data['books'])
        if string_in_line(author+title+str(year)) in data_check:
            return 'книга уже в списке'
        else:
            num = data['books'][-1]['id']+1
    book = dict(id=num,author=author,title=title, year=year, status='в наличии')
    data['books'].append(book)
    path.write_text(json.dumps(data), encoding='utf-8')
    return 'Книга добавлена'


def new_book_status(id: int, status: str):
    with open("test.json", "r+") as file:
        data = json.load(file)
        i = 0
        while i < len(data['books']) and i <= id:
            if data['books'][i]['id'] == id:
                data['books'][i]['status'] = status
                file.seek(0)
                json.dump(data, file)
                file.truncate()
                return f'Новый статус {status}'
            i += 1
        else:
            return 'Нет такой книги'


def search_book(key: int, filter: str):
    results = []
    if key == 1:
        filter_type = 'author'
    elif key == 2:
        filter_type = 'title'
    else:
        filter_type = 'year'
    path = Path('test.json')
    data = json.loads(path.read_text(encoding='utf-8'))
    for i in data['books']:
        if str(i[filter_type])==filter:
            results.append(i)
    if results:
        return results
    return ['Ничего не найдено']


def del_book(id: int):
    with open("test.json") as file:
        data = json.load(file)
    i = 0
    while i < len(data['books']) and i <= id:
        print(i)
        print(data['books'][i]['id'])
        print(data['books'][i]['id'] == id)
        if data['books'][i]['id'] == id:
            to_del = data['books'][i]
            print(to_del)
            data['books'].remove(to_del)
            with open('test.json', 'w') as outfile:
                json.dump(data, outfile, indent=4)
            return f'{to_del} удалена'
        i += 1
    else:
        return 'Такая книга не найдена'







# a = input('Введите автора')
# t = input('Введите название')
#
# while True:
#     y = input('Введите год числом')
#     if y.isdigit():
#         y = int(y)
#         if y <= datetime.now().year:
#             break
#         else:
#             print('год не может быть из будущего')
#     else:
#         print('Вы ввели не число')
#
# print(add_book(a,t,y))
#
path = Path('test.json')
data = json.loads(path.read_text(encoding='utf-8'))
for i in data['books']:
    print(i)
#
# id=int(input())
# status=input()
#
# new_book_status(id,status)
# path = Path('test.json')
# data = json.loads(path.read_text(encoding='utf-8'))
# for i in data['books']:
#     print(i)
# k = 0
# while k<1:
#     type_id = input('''
#                  Введите код для поиска:
#                  1 - по Автору
#                  2 - по Названию книги
#                  3 - по году
#                  ''')
#     if type_id.isdigit():
#         if int(type_id) in [1,2,3]:
#             k=2
#         else:
#             print('Нет такого кода')
#     else:
#         print('Вы ввели не число')
#
# filter = input('Ключ фильтра: ')
# for i in search_book(int(type_id),filter):
#     print(i)

id_to_del = input('Введите id для удаления ')
print(del_book(int(id_to_del)))
