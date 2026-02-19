import random
import heapq
from collections import defaultdict
import uuid

# Binary Search Tree Node
class BSTNode:
    def __init__(self, price, id):
        self.price = price
        self.id = id
        self.left = None
        self.right = None

# Binary Search Tree for price-sorted stock IDs
class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, price, id):
        if not self.root:
            self.root = BSTNode(price, id)
            return
        current = self.root
        while True:
            if price < current.price or (price == current.price and id < current.id):
                if current.left is None:
                    current.left = BSTNode(price, id)
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = BSTNode(price, id)
                    break
                current = current.right

    def delete(self, price, id):
        def find_min(node):
            while node.left:
                node = node.left
            return node

        def delete_node(node, price, id):
            if not node:
                return None
            if price < node.price or (price == node.price and id < node.id):
                node.left = delete_node(node.left, price, id)
            elif price > node.price or (price == node.price and id > node.id):
                node.right = delete_node(node.right, price, id)
            else:
                # Node to delete found
                if not node.left:
                    return node.right
                if not node.right:
                    return node.left
                # Node has two children
                successor = find_min(node.right)
                node.price = successor.price
                node.id = successor.id
                node.right = delete_node(node.right, successor.price, successor.id)
            return node

        self.root = delete_node(self.root, price, id)

    def range_query(self, p1, p2):
        result = []
        def inorder(node, p1, p2):
            if not node:
                return
            if node.price > p1 or (node.price == p1 and node.id >= 0):
                inorder(node.left, p1, p2)
            if p1 <= node.price <= p2:
                result.append(node.id)
            if node.price < p2 or (node.price == p2 and node.id <= float('inf')):
                inorder(node.right, p1, p2)
        inorder(self.root, p1, p2)
        return result

class StockTracker:
    def __init__(self):
        self.stocks = {}  # Hash table: ID -> (price, volume)
        self.price_sorted = BinarySearchTree()  # BST of (price, ID)
        self.price_to_ids = defaultdict(set)  # Price -> set of IDs
        self.volume_heap = []  # Max heap: (-volume, ID, uuid)
        self.id_to_uuid = {}  # ID -> uuid for heap uniqueness

    def insert_new_stock(self, x, p):
        if x in self.stocks:
            return
        self.stocks[x] = [p, 0]
        self.price_sorted.insert(p, x)
        self.price_to_ids[p].add(x)
        unique_id = str(uuid.uuid4())
        self.id_to_uuid[x] = unique_id
        heapq.heappush(self.volume_heap, (0, x, unique_id))

    def update_price(self, x, p):
        if x not in self.stocks:
            return
        old_price, volume = self.stocks[x]
        self.stocks[x][0] = p
        self.price_to_ids[old_price].discard(x)
        if not self.price_to_ids[old_price]:
            del self.price_to_ids[old_price]
        self.price_sorted.delete(old_price, x)
        self.price_sorted.insert(p, x)
        self.price_to_ids[p].add(x)

    def increase_volume(self, x, vinc):
        if x not in self.stocks:
            return
        self.stocks[x][1] += vinc
        new_volume = self.stocks[x][1]
        unique_id = str(uuid.uuid4())
        self.id_to_uuid[x] = unique_id
        heapq.heappush(self.volume_heap, (-new_volume, x, unique_id))

    def lookup_by_id(self, x):
        if x not in self.stocks:
            return None
        return self.stocks[x]

    def price_range(self, p1, p2):
        return self.price_sorted.range_query(p1, p2)

    def max_vol(self):
        while self.volume_heap:
            neg_vol, x, uuid = self.volume_heap[0]
            if x not in self.stocks or self.id_to_uuid.get(x) != uuid:
                heapq.heappop(self.volume_heap)
                continue
            return -neg_vol, x
        return 0, None
