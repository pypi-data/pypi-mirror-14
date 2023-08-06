from collections import deque


class Store(object):
    """In-memory storage of recent data. A global instance is
    available as ``brush.stores.store``.

    :param int maxlen: Maximum number of points to store

    .. todo:: Implement a redis-backed version

    """
    def __init__(self, maxlen=60):
        assert maxlen > 0
        assert isinstance(maxlen, int)
        self.maxlen = maxlen
        self.clear()

    def __getitem__(self, idx):
        return self._data[idx]

    def __iter__(self):
        return self._data.__iter__()

    def append(self, data):
        """Append data to the store. The oldest data item will be
        removed if appending results in exceeding the maximum
        length.

        :param dict data:

        """
        assert isinstance(data, dict)
        self._data.appendleft(data.copy())

    def clear(self):
        self._data = deque(maxlen=self.maxlen)

    def get(self, amount=1):
        """Return all recent data.

        :param int amount: maximum number of data items to return or -1
                           to get all

        """
        assert amount >= 1 or amount == -1
        if amount == 1:
            return self._data[0]
        else:
            if amount == -1:
                stop = len(self._data)
            else:
                stop = amount
            result = dict()
            for i in range(stop):
                data = self._data[i]
                for key in data:
                    if key not in result:
                        result[key] = [data[key]]
                    else:
                        result[key].append(data[key])
            return result


store = Store()
