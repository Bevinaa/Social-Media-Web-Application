#DATA STRUCTURES

class UserGraph:
    def __init__(self):
        self.graph = {}

    def add_user(self, user_id):
        if user_id not in self.graph:
            self.graph[user_id] = {'following': set(), 'followers': set()}

    def add_following(self, user_id, follow_id):
        self.add_user(user_id)
        self.add_user(follow_id)
        self.graph[user_id]['following'].add(follow_id)
        self.graph[follow_id]['followers'].add(user_id)

    def get_suggested_friends(self, user_id):
        if user_id not in self.graph:
            return []
        
        followed_by_user = self.graph[user_id]['following']
        suggested_friends = {}

        for followed_user in followed_by_user:
            for follower in self.graph[followed_user]['followers']:
                if follower != user_id and follower not in followed_by_user:
                    if follower not in suggested_friends:
                        suggested_friends[follower] = 0
                    suggested_friends[follower] += 1

        suggested_friends = sorted(suggested_friends, key=suggested_friends.get, reverse=True)
        return suggested_friends

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
    
    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def delete(self, word):
        def _delete(node, word, depth):
            if depth == len(word):
                if not node.is_end_of_word:
                    return False
                node.is_end_of_word = False
                return len(node.children) == 0

            char = word[depth]
            if char not in node.children:
                return False

            should_delete_child = _delete(node.children[char], word, depth + 1)

            if should_delete_child:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end_of_word

            return False

        _delete(self.root, word, 0)

class SplayTreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None

class SplayTree:
    def __init__(self):
        self.root = None
    
    def _rotate_right(self, x):
        y = x.left
        if y:
            x.left = y.right
            if y.right:
                y.right.parent = x
            y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        if y:
            y.right = x
        x.parent = y

    def _rotate_left(self, x):
        y = x.right
        if y:
            x.right = y.left
            if y.left:
                y.left.parent = x
            y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        if y:
            y.left = x
        x.parent = y

    def _splay(self, x):
        while x.parent:
            if not x.parent.parent:
                if x.parent.left == x:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            elif x.parent.left == x and x.parent.parent.left == x.parent:
                self._rotate_right(x.parent.parent)
                self._rotate_right(x.parent)
            elif x.parent.right == x and x.parent.parent.right == x.parent:
                self._rotate_left(x.parent.parent)
                self._rotate_left(x.parent)
            elif x.parent.left == x and x.parent.parent.right == x.parent:
                self._rotate_right(x.parent)
                self._rotate_left(x.parent)
            else:
                self._rotate_left(x.parent)
                self._rotate_right(x.parent)

    def insert(self, key):
        node = SplayTreeNode(key)
        y = None
        x = self.root

        while x:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if not y:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        self._splay(node)
    
    def search(self, key):
        x = self.root
        while x:
            if key == x.key:
                self._splay(x)
                return x
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        return None

    def delete(self, key):
        node = self.search(key)
        if node:
            if not node.left:
                self._transplant(node, node.right)
            elif not node.right:
                self._transplant(node, node.left)
            else:
                y = self._minimum(node.right)
                if y.parent != node:
                    self._transplant(y, y.right)
                    y.right = node.right
                    y.right.parent = y
                self._transplant(node, y)
                y.left = node.left
                y.left.parent = y
            self._splay(node.parent)

    def _maxattempts(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    def _checkattempts(self, x):
        while x.left:
            x = x.left
        return x

class AVLTreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.height = 1
        self.left = None
        self.right = None

class AVLTree:
    def __init__(self):
        self.root = None
    
    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = max(self._get_height(y.left), self._get_height(y.right)) + 1
        x.height = max(self._get_height(x.left), self._get_height(x.right)) + 1
        return x

    def _left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = max(self._get_height(x.left), self._get_height(x.right)) + 1
        y.height = max(self._get_height(y.left), self._get_height(y.right)) + 1
        return y

    def _insert(self, node, key, value):
        if not node:
            return AVLTreeNode(key, value)
        elif key < node.key:
            node.left = self._insert(node.left, key, value)
        else:
            node.right = self._insert(node.right, key, value)

        node.height = max(self._get_height(node.left), self._get_height(node.right)) + 1
        balance = self._get_balance(node)

        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)
        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)
        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)

    def _inorder_traversal(self, node, result):
        if node:
            self._inorder_traversal(node.left, result)
            result.append((node.key, node.value))
            self._inorder_traversal(node.right, result)

    def inorder_traversal(self):
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _delete(self, node, key):
        if not node:
            return node
        elif key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp
            temp = self._find_min(node.right)
            node.key = temp.key
            node.value = temp.value
            node.right = self._delete(node.right, temp.key)

        if not node:
            return node

        node.height = max(self._get_height(node.left), self._get_height(node.right)) + 1
        balance = self._get_balance(node)

        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def delete(self, key):
        self.root = self._delete(self.root, key)

class Stack:
    def __init__(self):
        self.items = []
    
    def is_empty(self):
        return len(self.items) == 0
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def size(self):
        return len(self.items)

class Queue:
    def __init__(self):
        self.items = []
    
    def is_empty(self):
        return len(self.items) == 0
    
    def enqueue(self, item):
        self.items.insert(0, item)
    
    def dequeue(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def size(self):
        return len(self.items)

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def to_list(self):
        node = self.head
        result = []
        while node:
            result.append(node.data)
            node = node.next
        return result
