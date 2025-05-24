import hashlib

class AVLNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None
    
    def _height(self, node):
        return node.height if node else 0
    
    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))
    
    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right) if node else 0
    
    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        
        x.right = y
        y.left = T2
        
        self._update_height(y)
        self._update_height(x)
        
        return x
    
    def _rotate_left(self, x):
        y = x.right
        T2 = y.left
        
        y.left = x
        x.right = T2
        
        self._update_height(x)
        self._update_height(y)
        
        return y
    
    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)
    
    def _insert(self, node, key, value):
        if not node:
            return AVLNode(key, value)
        
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value
            return node
        
        self._update_height(node)
        return self._rebalance(node)
    
    def _rebalance(self, node):
        balance = self._balance_factor(node)
        
        if balance > 1:
            if self._balance_factor(node.left) >= 0:
                return self._rotate_right(node)
            else:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)
        
        if balance < -1:
            if self._balance_factor(node.right) <= 0:
                return self._rotate_left(node)
            else:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)
        
        return node
    
    def search(self, key):
        return self._search(self.root, key)
    
    def _search(self, node, key):
        if not node:
            return None
        if key == node.key:
            return node.value
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)
    
    def delete(self, key):
        self.root = self._delete(self.root, key)
    
    def _delete(self, node, key):
        if not node:
            return node
        
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                temp = self._min_value_node(node.right)
                node.key = temp.key
                node.value = temp.value
                node.right = self._delete(node.right, temp.key)
        
        self._update_height(node)
        return self._rebalance(node)
    
    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current
    
    def display(self):
        self._inorder(self.root)
        print()
    
    def _inorder(self, node):
        if node:
            self._inorder(node.left)
            print(f"{node.key}: {node.value}", end=" | ")
            self._inorder(node.right)

class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [AVLTree() for _ in range(size)]
    
    def _hash(self, key):
        return int(hashlib.sha256(key.encode()).hexdigest(), 16) % self.size
    
    def insert(self, key, value):
        index = self._hash(key)
        self.table[index].insert(key, value)
        print(f"Добавлено: [{key}: {value}] в Cell {index + 1}")
    
    def search(self, key):
        index = self._hash(key)
        result = self.table[index].search(key)
        print(f"Поиск '{key}' в Cell {index + 1}: {'найден' if result else 'не найден'}")
        if result:
            print(f"Значение: {result}")  # Явный вывод значения при успешном поиске
        return result
    
    def delete(self, key):
        index = self._hash(key)
        if self.table[index].search(key):
            self.table[index].delete(key)
            print(f"Удалено: {key} из Cell {index + 1}")
        else:
            print(f"Ключ '{key}' не найден")
    
    def display(self):
        print("\nТекущее состояние хеш-таблицы:")
        for i, tree in enumerate(self.table):
            print(f"Cell {i + 1}: ", end="")
            tree.display()
        print()

def interactive_menu():
    print("\nМеню управления хеш-таблицей:")
    print("1. Добавить элемент")
    print("2. Найти элемент")
    print("3. Удалить элемент")
    print("4. Показать всю таблицу")
    print("5. Изменить размер таблицы")
    print("6. Выход")

def main():
    while True:
        try:
            size = int(input("Введите начальный размер хеш-таблицы: ") or 10)
            break
        except ValueError:
            print("Некорректный ввод размера, попробуйте снова")
    ht = HashTable(size)
    
    while True:
        interactive_menu()
        choice = input("Выберите действие (1-6): ")
        
        if choice == "1":
            key = input("Введите ключ: ")
            value = input("Введите значение: ")
            ht.insert(key, value)
        
        elif choice == "2":
            key = input("Введите ключ для поиска: ")
            result = ht.search(key)
            if result:
                print(f"Значение: {result}")
        
        elif choice == "3":
            key = input("Введите ключ для удаления: ")
            ht.delete(key)
        
        elif choice == "4":
            ht.display()
        
        elif choice == "5":
            try:
                new_size = int(input("Введите новый размер таблицы: "))
                ht = HashTable(new_size)
                print(f"Таблица изменена на размер {new_size}")
            except ValueError:
                print("Некорректный размер таблицы, попробуйте снова")
        
        elif choice == "6":
            print("Выход из программы")
            break
        
        else:
            print("Неверный ввод, попробуйте снова")

if __name__ == "__main__":
    main()