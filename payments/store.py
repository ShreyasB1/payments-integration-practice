from collections import defaultdict

from payments.errors import NotFound


class Store:
    """In-memory storage. Objects are kept by id, one table per kind."""

    def __init__(self):
        self._tables = defaultdict(dict)
        self._counters = defaultdict(int)

    def next_id(self, prefix):
        self._counters[prefix] += 1
        return f"{prefix}_{self._counters[prefix]}"

    def put(self, kind, obj):
        self._tables[kind][obj.id] = obj
        return obj

    def get(self, kind, obj_id):
        try:
            return self._tables[kind][obj_id]
        except KeyError:
            raise NotFound(kind, obj_id) from None

    def all(self, kind):
        """Every object of a kind, in the order they were stored."""
        return list(self._tables[kind].values())
