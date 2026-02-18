# utils/python/lc_utils.py
import sys
import json
import pprint
from typing import List, Optional, Dict, Set, Tuple, Any

# --- LeetCode Structures ---

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        vals = []
        curr = self
        while curr:
            vals.append(curr.val)
            curr = curr.next
        return f"ListNode{vals}"

    @staticmethod
    def from_list(lst: List[int]) -> Optional['ListNode']:
        if not lst:
            return None
        head = ListNode(lst[0])
        current = head
        for val in lst[1:]:
            current.next = ListNode(val)
            current = current.next
        return head

    def to_list(self) -> List[int]:
        lst = []
        current = self
        while current:
            lst.append(current.val)
            current = current.next
        return lst

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"

    # Simple level-order constructor from list [1, 2, 3, null, null, 4, 5]
    @staticmethod
    def from_list(lst: List[Optional[int]]) -> Optional['TreeNode']:
        if not lst:
            return None

        nodes = [TreeNode(val) if val is not None else None for val in lst]
        root = nodes[0]
        queue = [root]
        idx = 1

        while queue and idx < len(nodes):
            node = queue.pop(0)
            if node:
                if idx < len(nodes):
                    node.left = nodes[idx]
                    if nodes[idx]: queue.append(nodes[idx])
                    idx += 1
                if idx < len(nodes):
                    node.right = nodes[idx]
                    if nodes[idx]: queue.append(nodes[idx])
                    idx += 1
        return root

# --- Debug Helper ---
def debug(*args, **kwargs):
    """Prints debug info to stderr."""
    sys.stderr.write("\033[34m[DEBUG] ")
    print(*args, file=sys.stderr, **kwargs)
    sys.stderr.write("\033[0m")

# --- Parse Helper ---
def parse(s: str):
    """Tries to parse string as JSON (list/dict/prim), else returns raw string."""
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return s.strip()

# --- Read Helper ---
def read_input() -> str:
    """Reads a line from stdin."""
    try:
        line = sys.stdin.readline()
        return line.strip()
    except EOFError:
        return ""
