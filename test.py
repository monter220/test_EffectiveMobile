import unittest
import json
import os

from library import add_book, new_book_status, search_book, del_book, main


class TestLibrary(unittest.TestCase):
    FILE_NAME = 'test_library.json'

    def setUp(self):
        self.data = {'books': []}
        with open(self.FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump(self.data, f)

    def tearDown(self):
        if os.path.exists(self.FILE_NAME):
            os.remove(self.FILE_NAME)

    def test_add_book(self):
        result = add_book(self.FILE_NAME, 'Автор', 'Название', 2020)
        self.assertEqual(result, ['Книга добавлена'])

        result = add_book(self.FILE_NAME, 'Автор', 'Название', 2020)
        self.assertEqual(result, ['книга уже в списке'])

    def test_new_book_status(self):
        add_book(self.FILE_NAME, 'Автор', 'Название', 2020)

        result = new_book_status(self.FILE_NAME, 1, 'взято')
        self.assertEqual(result, ['Новый статус взято'])

        result = new_book_status(self.FILE_NAME, 999, 'взято')
        self.assertEqual(result, ['Нет такой книги'])

    def test_search_book(self):
        add_book(self.FILE_NAME, 'Автор', 'Название', 2020)

        result = search_book(self.FILE_NAME, 1, 'Автор')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Название')

        result = search_book(self.FILE_NAME, 1, 'Неизвестный автор')
        self.assertEqual(result, ['Ничего не найдено'])

    def test_del_book(self):
        add_book(self.FILE_NAME, 'Автор', 'Название', 2020)

        result = del_book(self.FILE_NAME, 1)
        self.assertEqual(result, [
            "{'id': 1, 'author': 'Автор', 'title': 'Название', 'year': 2020, 'status': 'в наличии'} удалена"])

        result = del_book(self.FILE_NAME, 999)
        self.assertEqual(result, ['Такая книга не найдена'])

    def test_main_list(self):
        add_book(self.FILE_NAME, 'Автор', 'Название', 2020)
        args = type('', (), {})()
        args.list = True
        result = main(self.FILE_NAME, args)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Название')


if __name__ == '__main__':
    unittest.main()
