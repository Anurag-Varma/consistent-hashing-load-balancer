from consistent_hash import ConsistentHash

# Create a consistent hash ring with weighted nodes
con_hash = ConsistentHash({
    '192.168.0.101:11212': 5,
    '192.168.0.102:11212': 2,
    '192.168.0.103:11212': 1
})

# Add additional nodes to the hash ring
con_hash.add_nodes({'192.168.0.104:11212': 1})

# Verify the current nodes in the hash ring
current_nodes = con_hash.get_all_nodes()
print(f"Current nodes in hash ring: {current_nodes}")

# Retrieve the server responsible for storing 'my_key'
server = con_hash.get_node('my_key')
print(f"Server handling 'my_key': {server}")

# Remove nodes from the hash ring
con_hash.remove_nodes(['192.168.0.102:11212', '192.168.0.104:11212'])

# Verify the current nodes in the hash ring
all_nodes = con_hash.get_all_nodes()
print(f"Remaining nodes in hash ring: {all_nodes}")
