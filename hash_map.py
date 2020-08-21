# hash_map.py
# ===================================================
# Implementation of a hash map with chaining
# ===================================================

# singly linked list node
class SLNode:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + str(self.key) + ', ' + str(self.value) + ')'

# standard singly linked list
class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Creates a new node and inserts it at the front of the linked list
        Arguments:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def remove(self, key):
        """Removes node from linked list
        Argumentss:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Arguments:
        	key: key of node
        Returns:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def __str__(self):
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out

# hash = sum of each character of key's unicode value
# cat and tac will each have 312
def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash

# hash = the sum of each character's unicode value multiplied by it's (index + 1).
# cat (641) and tac (607) are no longer equal
def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash

# Initializes a hash map
class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Arguments:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    # creates an empty list _buckets
    # iterates through each bucket in capacity filling each with a linked list object.
    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function
        self.size = 0

    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """

        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out

    def put(self, key, value):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Arguments:
            key: they key to use to has the entry
            value: the value associated with the entry
        """

        # acquires the hash value, index number, and linked list object at the index
        hash = self._hash_function(key)
        index = (hash % self.capacity)
        hash_link = self._buckets[index]

        # if key is found, remove it and replace with new key:value pair, else add front and increment self.size
        if (hash_link.contains(key)):
            hash_link.remove(key)
            hash_link.add_front(key, value)
        else:
            hash_link.add_front(key, value)
            self.size += 1

        # Check table able load, if >= 2 double table size. 2 is an arbitrary number low enough to test.
        # if (self.table_load() >= 2 ):
        #     self.resize_table(self.capacity * 2)

    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """
        # clear self._buckets and repopulate with empty linked lists.
        self._buckets.clear()
        for i in range(self.capacity):
            self._buckets.append(LinkedList())

    def get(self, key):
        """
        Returns the value with the given key.
        Argumentss:
            key: the value of the key to look for
        Returns:
            The value associated to the key. None if the link isn't found.
        """

        # acquires hash, index number, linked list at index number, and head of linked list
        hash = self._hash_function(key)
        index = (hash % self.capacity)
        hash_link = self._buckets[index]
        cur = hash_link.head

        # check hash_link for key, if found return value, else return none.
        for i in range(hash_link.size):
            if (cur.key == key):
                return cur.value
            else:
                cur = cur.next

        return None

    def resize_table(self, capacity):
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Arguments:
            capacity: the new number of buckets.
        """

        # save self._buckets
        _oldBuckets = self._buckets

        # reset self._buckets with new capacity, reset object attributes
        self._buckets = []
        self.size = 0
        self.capacity = capacity
        for i in range(capacity):
            self._buckets.append(LinkedList())

        # rehash each link back into self._buckets.
        for i in range(len(_oldBuckets)):
            if _oldBuckets[i].size != 0:
                cur = _oldBuckets[i].head
                while (cur != None):
                    self.put(cur.key, cur.value)
                    cur = cur.next

    def remove(self, key):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Arguments:
            key: they key to search for and remove along with its value
        """
        hash = self._hash_function(key)
        index = (hash % self.capacity)
        hash_link = self._buckets[index]

        # if key exists in hash link, remove it
        if (hash_link.contains(key)):
            hash_link.remove(key)

    def contains_key(self, key):
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise

        """
        hash = self._hash_function(key)
        index = (hash % self.capacity)
        hash_link = self._buckets[index]

        # if key exists in hash link, remove it
        if (hash_link.contains(key)):
            return True
        else:
            return False

    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table
        """
        empty_count = 0
        for i in range(self.capacity):
            if (self._buckets[i].size == 0):
                empty_count += 1

        return empty_count

    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """
        return self.size/self.capacity
