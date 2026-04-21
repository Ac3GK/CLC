class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(root, value):
    if root is None:
        return TreeNode(value)
    if value < root.value:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)
    return root

def find_min(node):
    current = node
    while current.left is not None:
        current = current.left
    return current.value

def find_max(node):
    current = node
    while current.right is not None:
        current = current.right
    return current.value

def get_stats_from_list(data_list):
    if not data_list:
        return None, None
    
    root = None
    for val in data_list:
        root = insert(root, val)
    
    return find_min(root), find_max(root)
