import unittest
import io
import sys
from main import HashTable, AVLTree, main

class TestAVLTree(unittest.TestCase):

    def setUp(self):
        self.avl_tree = AVLTree()

    def test_insert_and_search(self):
        self.avl_tree.insert("key1", "value1")
        self.avl_tree.insert("key2", "value2")
        self.avl_tree.insert("key3", "value3")

        self.assertEqual(self.avl_tree.search("key1"), "value1")
        self.assertEqual(self.avl_tree.search("key2"), "value2")
        self.assertEqual(self.avl_tree.search("key3"), "value3")
        self.assertIsNone(self.avl_tree.search("key4"))

    def test_delete_node_with_two_children(self):
        self.avl_tree.insert("key2", "value2")
        self.avl_tree.insert("key1", "value1")
        self.avl_tree.insert("key3", "value3")
        self.avl_tree.insert("key4", "value4")

        self.avl_tree.delete("key2")  # key2 has two children
        self.assertIsNone(self.avl_tree.search("key2"))
        self.assertEqual(self.avl_tree.search("key1"), "value1")
        self.assertEqual(self.avl_tree.search("key3"), "value3")
        self.assertEqual(self.avl_tree.search("key4"), "value4")

    def test_search_empty_tree(self):
        self.assertIsNone(self.avl_tree.search("key1"))  # Searching in an empty tree

    def test_balance_after_multiple_operations(self):
        keys = ["key1", "key2", "key3", "key4", "key5"]
        for key in keys:
            self.avl_tree.insert(key, f"value_{key}")
        
        self.avl_tree.delete("key3")  # Remove a middle node
        self.assertEqual(self.avl_tree.search("key1"), "value_key1")

class TestHashTable(unittest.TestCase):

    def setUp(self):
        self.hash_table = HashTable(size=5)  # Smaller size for easier testing

    def test_insert_and_search(self):
        self.hash_table.insert("key1", "value1")
        self.hash_table.insert("key2", "value2")

        self.assertEqual(self.hash_table.search("key1"), "value1")
        self.assertEqual(self.hash_table.search("key2"), "value2")
        self.assertIsNone(self.hash_table.search("key3"))

    def test_collision_handling(self):
        self.hash_table.insert("key1", "value1")
        self.hash_table.insert("key2", "value2")  # Assuming they collide

        self.assertEqual(self.hash_table.search("key1"), "value1")
        self.assertEqual(self.hash_table.search("key2"), "value2")

    def test_resize_table(self):
        for i in range(10):  # Insert more elements than initial size
            self.hash_table.insert(f"key{i}", f"value{i}")

        # Check if it runs without error (simple display check)
        self.hash_table.display()

    def test_delete_nonexistent_key(self):
        self.hash_table.insert("key1", "value1")
        self.hash_table.delete("key2")  # Attempt to delete a non-existent key
        self.assertIsNone(self.hash_table.search("key2"))

class TestInteractiveMenu(unittest.TestCase):

    def test_interactive_menu(self):
        # Prepare the input
        user_input = "10\n1\nkey1\nvalue1\n2\nkey1\n3\nkey1\n4\n5\n10\n6\n"
        sys.stdin = io.StringIO(user_input)  # Redirect stdin

        # Redirect stdout to capture print statements
        captured_output = io.StringIO()
        sys.stdout = captured_output

        main()  # Run the main menu

        # Restore stdout and stdin
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

        # Get the output as a single string
        output = captured_output.getvalue()

        # Check the printed outputs
        self.assertIn("Значение: value1", output)
        self.assertIn("Таблица изменена на размер 10", output)
        self.assertIn("Выход из программы", output)

    def test_interactive_menu_invalid_input(self):
        # Prepare the input
        user_input = "10\n7\n1\nkey1\nvalue1\n2\nkey1\n6\n"
        sys.stdin = io.StringIO(user_input)  # Redirect stdin

        # Redirect stdout to capture print statements
        captured_output = io.StringIO()
        sys.stdout = captured_output

        main()  # Run the main menu

        # Restore stdout and stdin
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

        # Check for error message
        output = captured_output.getvalue()  # Get the full output

        # Check for the error message
        self.assertIn("Неверный ввод, попробуйте снова", output)

        # Check that the menu is shown again
        self.assertIn("Меню управления хеш-таблицей:", output)

if __name__ == "__main__":
    unittest.main()