import unittest
import json
import os
import sys
from io import StringIO
from main import AVLTree, HashTable, main  # Импортируйте ваши классы и функцию main

class TestAVLTree(unittest.TestCase):
    def setUp(self):
        self.tree = AVLTree()

    def test_insert_and_search(self):
        self.tree.insert("key1", "value1")
        self.assertEqual(self.tree.search("key1"), "value1")
        self.assertIsNone(self.tree.search("key2"))

    def test_delete(self):
        self.tree.insert("key1", "value1")
        self.tree.delete("key1")
        self.assertIsNone(self.tree.search("key1"))

    def test_rebalance(self):
        for i in range(10):
            self.tree.insert(str(i), f"value{i}")
        self.assertEqual(self.tree.root.key, "3")  # Проверяем, что корень сбалансирован

    def test_delete_nonexistent(self):
        self.tree.delete("nonexistent")
        self.assertIsNone(self.tree.search("nonexistent"))

    def test_insert_overwrite(self):
        self.tree.insert("key1", "value1")
        self.tree.insert("key1", "value2")  # Обновляем значение
        self.assertEqual(self.tree.search("key1"), "value2")

class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.ht = HashTable(size=5)

    def test_insert_and_search(self):
        self.ht.insert("key1", "value1")
        self.assertEqual(self.ht.search("key1"), "value1")
        self.assertIsNone(self.ht.search("key2"))

    def test_delete(self):
        self.ht.insert("key1", "value1")
        self.ht.delete("key1")
        self.assertIsNone(self.ht.search("key1"))

    def test_save_and_load(self):
        self.ht.insert("key1", "value1")
        filename = 'test_hash_table.json'
        self.ht.save_to_file(filename)

        new_ht = HashTable(size=5)
        new_ht.load_from_file(filename)
        self.assertEqual(new_ht.search("key1"), "value1")
        
        # Удаляем файл после теста
        os.remove(filename)

    def test_load_nonexistent_file(self):
        new_ht = HashTable(size=5)
        result = new_ht.load_from_file('nonexistent.json')
        self.assertFalse(result)

    def test_change_size(self):
        self.ht.insert("key1", "value1")
        self.ht.insert("key2", "value2")
        
        new_ht = HashTable(size=10)
        for key, value in self.ht.get_all_items():
            new_ht.insert(key, value)
        
        self.assertEqual(new_ht.search("key1"), "value1")
        self.assertEqual(new_ht.search("key2"), "value2")

    def test_display_empty_table(self):
        self.ht.display()  # Проверяем, что метод не вызывает ошибок при отображении пустой таблицы

class TestMainFunction(unittest.TestCase):
    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output  # Перенаправляем стандартный вывод

    def tearDown(self):
        sys.stdout = sys.__stdout__  # Возвращаем стандартный вывод

    def test_main_insertion_and_display(self):
        inputs = ['10', '1', 'key1', 'value1', '4', '8']
        sys.stdin = StringIO('\n'.join(inputs))  # Перенаправляем стандартный ввод
        main()  # Запускаем функцию main
        output = self.held_output.getvalue()
        self.assertIn("Добавлено: [key1: value1] в Cell", output)

    def test_main_search_existing_key(self):
        inputs = ['10', '1', 'key1', 'value1', '2', 'key1', '4', '8']
        sys.stdin = StringIO('\n'.join(inputs))  # Перенаправляем стандартный ввод
        main()  # Запускаем функцию main
        output = self.held_output.getvalue()
        self.assertIn("Значение: value1", output)

    def test_main_search_nonexistent_key(self):
        inputs = ['10', '2', 'key2', '4', '8']
        sys.stdin = StringIO('\n'.join(inputs))  # Перенаправляем стандартный ввод
        main()  # Запускаем функцию main
        output = self.held_output.getvalue()
        self.assertIn("не найден", output)

    def test_main_delete_existing_key(self):
        inputs = ['10', '1', 'key1', 'value1', '3', 'key1', '4', '8']
        sys.stdin = StringIO('\n'.join(inputs))  # Перенаправляем стандартный ввод
        main()  # Запускаем функцию main
        output = self.held_output.getvalue()
        self.assertIn("Удалено: key1 из Cell", output)

    def test_main_delete_nonexistent_key(self):
        inputs = ['10', '3', 'key2', '4', '8']
        sys.stdin = StringIO('\n'.join(inputs))  # Перенаправляем стандартный ввод
        main()  # Запускаем функцию main
        output = self.held_output.getvalue()
        self.assertIn("Ключ 'key2' не найден", output)

    def test_main_change_size(self):
        inputs = ['10', '5', '20', '4', '8']
        sys.stdin = StringIO('\n'.join(inputs))  # Перенаправляем стандартный ввод
        main()  # Запускаем функцию main
        output = self.held_output.getvalue()
        self.assertIn("Таблица изменена на размер 20", output)

    def test_main_save_to_file(self):
        inputs = ['10', '6', 'test_file.json', '4', '8']
        sys.stdin = StringIO('\n'.join(inputs))  # Перенаправляем стандартный ввод
        main()  # Запускаем функцию main
        output = self.held_output.getvalue()
        self.assertIn("Хеш-таблица сохранена в файл 'test_file.json'", output)
        os.remove('test_file.json')  # Удаляем временный файл

    def test_main_load_nonexistent_file(self):
        inputs = ['10', '7', 'nonexistent.json', '8']
        sys.stdin = StringIO('\n'.join(inputs))  # Перенаправляем стандартный ввод
        main()  # Запускаем функцию main
        output = self.held_output.getvalue()
        self.assertIn("Файл 'nonexistent.json' не существует", output)

    def test_main_exit(self):
        inputs = ['10', '8']
        sys.stdin = StringIO('\n'.join(inputs))  # Перенаправляем стандартный ввод
        main()  # Запускаем функцию main
        output = self.held_output.getvalue()
        self.assertIn("Выход из программы", output)

if __name__ == '__main__':
    unittest.main()