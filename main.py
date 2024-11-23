import json
import os
import string

from pathlib import Path
from datetime import datetime


def stringinline(line: str) -> str:
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
            stringinline(
                r['author']+r['title']+str(r['year'])) for r in data['books'])
        if stringinline(author+title+str(year)) in data_check:
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


a = input('Введите автора')
t = input('Введите название')

while True:
    y = input('Введите год числом')
    if y.isdigit():
        y = int(y)
        if y <= datetime.now().year:
            break
        else:
            print('год не может быть из будущего')
    else:
        print('Вы ввели не число')

print(add_book(a,t,y))

path = Path('test.json')
data = json.loads(path.read_text(encoding='utf-8'))
for i in data['books']:
    print(i)

id=int(input())
status=input()

new_book_status(id,status)
path = Path('test.json')
data = json.loads(path.read_text(encoding='utf-8'))
for i in data['books']:
    print(i)
