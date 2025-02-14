import hashlib
import bisect
import re

class ConsistentHash:
    """
    Implements consistent hashing with variable node weights.
    """
    interleave_count = 10  # Number of virtual nodes per real node
    hasher = None  # Custom hash function (if needed)

    def __init__(self, objects=None):
        """
        Initialize the consistent hash ring.
        :param objects: A dictionary {node: weight}, list of nodes, or single node string.
        """
        self.keys = []  # Sorted hash ring keys
        self.key_node = {}  # Mapping of hash ring keys to nodes
        self.nodes = []  # List of nodes
        self.index = 0  # Number of nodes in the ring
        self.weights = {}  # Weights of each node

        self.add_nodes(objects)

    def _ingest_objects(self, objects):
        """
        Ingest nodes into the consistent hashing ring.
        :param objects: Can be a dictionary (nodes with weights), list, or string (single node).
        """
        if isinstance(objects, dict):
            self.nodes.extend(objects.keys())
            self.weights.update(objects)
        elif isinstance(objects, list):
            self.nodes.extend(objects)
        elif isinstance(objects, str):
            self.nodes.append(objects)
        elif objects is not None:
            raise TypeError("Nodes must be a dict, list, or string.")

    def add_nodes(self, nodes):
        """
        Adds nodes to the hash ring and updates the hash space.
        :param nodes: A dictionary {node: weight}, list of nodes, or single node string.
        """
        self._ingest_objects(nodes)
        self._generate_ring(start=self.index)
        self.index = self.get_nodes_count()
        self.keys.sort()

    def _generate_ring(self, start=0):
        """
        Generates the hash ring from the given starting index.
        :param start: Index to start generating the ring from (default is 0).
        """
        for node in self.nodes[start:]:
            for key in self._node_keys(node):
                self.key_node[key] = node
                self.keys.append(key)

    def remove_nodes(self, nodes):
        """
        Removes nodes from the hash ring.
        :param nodes: List of nodes to remove.
        """
        if not isinstance(nodes, list):
            raise TypeError("Nodes must be a list.")

        for node in nodes:
            if node not in self.nodes:
                continue
            for key in self._node_keys(node):
                self.keys.remove(key)
                del self.key_node[key]
            self.nodes.remove(node)
            if node in self.weights:
                del self.weights[node]
            self.index -= 1

    def _node_keys(self, node):
        """
        Generates hash keys for a given node based on its weight.
        :param node: The node to generate keys for.
        :return: Generator yielding hash keys.
        """
        weight = self.weights.get(node, 1)
        factor = self.interleave_count * weight

        for j in range(int(factor)):
            b_key = self._hash_digest(f"{node}-{j}")
            for i in range(4):
                yield self._hash_val(b_key, lambda x: x + i * 4)

    def get_node(self, string_key):
        """
        Finds the appropriate node for the given key.
        :param string_key: The key to hash and find a node for.
        :return: The corresponding node.
        """
        pos = self.get_node_pos(string_key)
        return None if pos is None else self.key_node[self.keys[pos]]

    def get_node_pos(self, string_key):
        """
        Finds the position of the node responsible for a given key.
        :param string_key: The key to find the position for.
        :return: Position in the sorted ring or None if empty.
        """
        if not self.key_node:
            return None
        key = self.gen_key(string_key)
        pos = bisect.bisect(self.keys, key)
        return 0 if pos == len(self.keys) else pos

    def get_all_nodes(self):
        """
        Returns a sorted list of all nodes in the hash ring.
        """
        return sorted(self.nodes, key=lambda node: list(map(int, re.split(r'\W', node))))

    def get_nodes_count(self):
        """
        Returns the number of nodes in the hash ring.
        """
        return len(self.nodes)

    def gen_key(self, key):
        """
        Generates a hash key for a given string.
        :param key: The string key to hash.
        :return: A numerical hash value.
        """
        return self._hash_val(self._hash_digest(key), lambda x: x)

    def _hash_val(self, b_key, entry_fn):
        """
        Computes a hash value using parts of an MD5 hash.
        :param b_key: Byte array from MD5 hash.
        :param entry_fn: Function to determine hash components.
        :return: Computed hash value.
        """
        return (
            (b_key[entry_fn(3)] << 24)
            | (b_key[entry_fn(2)] << 16)
            | (b_key[entry_fn(1)] << 8)
            | b_key[entry_fn(0)]
        )

    def _hash_digest(self, key):
        """
        Generates an MD5 digest for a given key.
        :param key: The string key to hash.
        :return: List of bytes from the MD5 hash.
        """
        key = key.encode() if isinstance(key, str) else key
        m = hashlib.md5()
        m.update(key)
        return list(m.digest())
