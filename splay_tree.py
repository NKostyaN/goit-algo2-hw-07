class SplayNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class SplayTree:
    def __init__(self):
        self.root = None

    def _right(self, node):
        left = node.left
        node.left = left.right
        left.right = node
        return left

    def _left(self, node):
        right = node.right
        node.right = right.left
        right.left = node
        return right

    def _splay(self, node, key):
        if not node or node.key == key:
            return node

        if key < node.key:
            if not node.left:
                return node
            if key < node.left.key:
                node.left.left = self._splay(node.left.left, key)
                node = self._right(node)
            elif key > node.left.key:
                node.left.right = self._splay(node.left.right, key)
                if node.left.right:
                    node.left = self._left(node.left)
            return self._right(node) if node.left else node
        else:
            if not node.right:
                return node
            if key > node.right.key:
                node.right.right = self._splay(node.right.right, key)
                node = self._left(node)
            elif key < node.right.key:
                node.right.left = self._splay(node.right.left, key)
                if node.right.left:
                    node.right = self._right(node.right)
            return self._left(node) if node.right else node

    def search(self, key):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None

    def insert(self, key, value):
        if not self.root:
            self.root = SplayNode(key, value)
            return

        self.root = self._splay(self.root, key)
        if self.root.key == key:
            self.root.value = value
        elif key < self.root.key:
            new_node = SplayNode(key, value)
            new_node.left = self.root.left
            new_node.right = self.root
            self.root.left = None
            self.root = new_node
        else:
            new_node = SplayNode(key, value)
            new_node.right = self.root.right
            new_node.left = self.root
            self.root.right = None
            self.root = new_node
