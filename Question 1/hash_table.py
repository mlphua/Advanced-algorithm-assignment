class Slot:

    EMPTY = 0
    OCCUPIED = 1
    DELETED = 2
    __slots__ = ("key", "value", "state")

    def __init__(self):
        self.key = None
        self.value = None
        self.state = Slot.EMPTY


class HashTable:
    def __init__(self, size=31):
        if size < 1:
            raise ValueError("Table size must be at least 1")
        self._size = size
        self._slots = [Slot() for _ in range(size)]
        self._count = 0
        self.last_probes = 0  # probes used by the most recent operation

    # ---------- helpers ----------
    def _hash(self, key):
        """Division method: hash(key) mod table size."""
        return hash(key) % self._size

    def _find(self, key):
        """Return the slot index holding key, or -1. Linear probing: idx, idx+1, ..."""
        start = self._hash(key)
        self.last_probes = 0
        for i in range(self._size):
            pos = (start + i) % self._size
            slot = self._slots[pos]
            self.last_probes += 1
            if slot.state == Slot.EMPTY:      # chain ends: key cannot be further on
                return -1
            if slot.state == Slot.OCCUPIED and slot.key == key:
                return pos
            # DELETED or a different key: keep probing
        return -1

    # ---------- public operations ----------
    def insert(self, key, value):
        """Insert (or overwrite) a record. Returns the slot index used."""
        start = self._hash(key)
        first_free = None
        for i in range(self._size):
            pos = (start + i) % self._size
            slot = self._slots[pos]
            if slot.state == Slot.EMPTY:
                if first_free is None:
                    first_free = pos
                break
            if slot.state == Slot.DELETED:
                if first_free is None:
                    first_free = pos          # reuse the first tombstone we saw
            elif slot.key == key:             # key already exists: overwrite
                slot.value = value
                return pos
        if first_free is None:
            raise OverflowError("Hash table is full")
        slot = self._slots[first_free]
        slot.key, slot.value, slot.state = key, value, Slot.OCCUPIED
        self._count += 1
        return first_free

    def search(self, key):
        """Return the value stored for key, or None."""
        pos = self._find(key)
        return self._slots[pos].value if pos != -1 else None

    def slot_of(self, key):
        """Return the slot index of key, or -1 (handy for display/testing)."""
        return self._find(key)

    def delete(self, key):
        """Remove key. Returns True if it existed."""
        pos = self._find(key)
        if pos == -1:
            return False
        slot = self._slots[pos]
        slot.key, slot.value, slot.state = None, None, Slot.DELETED
        self._count -= 1
        return True

    def is_full(self):
        return self._count >= self._size

    def load_factor(self):
        return self._count / self._size

    def __len__(self):
        return self._count

    def items(self):
        """Yield (slot_index, key, value) for every occupied slot."""
        for pos, slot in enumerate(self._slots):
            if slot.state == Slot.OCCUPIED:
                yield pos, slot.key, slot.value

    @property
    def size(self):
        return self._size