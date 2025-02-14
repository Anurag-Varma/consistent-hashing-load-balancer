
# Consistent Hashing

This Python package implements consistent hashing, an algorithm that helps distribute keys (or requests) across a changing set of server nodes. It's useful when the number of servers can dynamically increase or decrease. The algorithm used is based on libketama.

## Usage

Using the consistent hash implementation is simple and intuitive. Here are the three ways you can construct a consistent hash:

1. **Using a dictionary with nodes and weights:**

    ```python
    from consistent_hash import ConsistentHash

    con_hash = ConsistentHash({'192.168.0.101:11212':1, '192.168.0.102:11212':2, '192.168.0.103:11212':1})
    ```

2. **Using a list of nodes (without weights):**

    ```python
    con_hash = ConsistentHash(['192.168.0.101:11212', '192.168.0.102:11212', '192.168.0.103:11212'])
    ```

3. **Using a single node as a string:**

    ```python
    con_hash = ConsistentHash('192.168.0.101:11212')
    ```

### Add servers to the hash ring

You can add additional nodes to the hash ring:

```python
con_hash.add_nodes({'192.168.0.104:11212':1})
```

### Get a server for a specific key

Retrieve a server for a given key:

```python
server = con_hash.get_node('my_key')
```

### Remove servers from the hash ring

Remove nodes from the hash ring. No need to specify the weights:

```python
con_hash.remove_nodes(['192.168.0.102:11212', '192.168.0.104:11212'])
```

## Demo testing

You can run the demo test file present in the repo so see the Consistant Hash project working:

```bash
python test.py
```