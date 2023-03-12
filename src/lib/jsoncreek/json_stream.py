import collections
from json_creek.tokenizer import TokenType

class StreamingAccessException(Exception):
    pass


def factory(token, token_stream):
    if token == '{':
        return StreamingObject(token_stream)
    if token == '[':
        return StreamingList(token_stream)


class StreamingBase:        
    def __init__(self, token_stream):
        self.streaming = True
        self._started = False
        self._stream = token_stream        
        self._child = None

        
    def _clear_child(self):
        if self._child is not None:
            self._child.read_all()
            self._child = None

    def _iter_items(self):
        self._started = True
        while True:
            if not self.streaming:
                return
            self._clear_child()
            try:
                item = self._load_item()
            except StopIteration:
                return
            yield item

    def _done(self):
        self.streaming = False
        raise StopIteration()

    def read_all(self):
        collections.deque(self._iter_items(), maxlen=0)            

    def _check_started(self):
        if self._started:
            raise StreamingAccessException("Cannot restart iteration of stream")
        
    def __getitem__(self, k):
        return self._find_item(k)
    
#    def __iter__(self):
#        self._check_started()
#        return 

class StreamingObject(StreamingBase):
    def __init__(self, token_stream) -> None:
        super().__init__(token_stream)
        self._started = False


    def _load_item(self):
        token_type, k = next(self._stream)
        if token_type == TokenType.OPERATOR:
            if k == '}':
                self._done()
            if k == ',':
                token_type, k = next(self._stream)
        if token_type != TokenType.STRING:
            raise ValueError(f"Expecting string, comma or }}, got {k} ({token_type})")
        
        token_type, token = next(self._stream)
        if token_type != TokenType.OPERATOR or token != ":":
            raise ValueError("Expecting :")
        
        token_type, v = next(self._stream)
        if token_type == TokenType.OPERATOR:
            self._child = v = factory(v, self._stream)
        return k, v
    

    def _find_item(self, k):
        was_started = self._started
        try:
            return self._find_item(k)
        except KeyError:
            if was_started:
                raise StreamingAccessException(
                    f"{k} not found in stream or already has been passed in stream",
                )
            raise

    def items(self):
        self._check_started()
        return self._iter_items()
    
    def keys(self):
        self._check_started()
        return (k for k, v in self._iter_items())
    
    def values(self):
        self._check_started()
        return (v for k, v in self._iter_items())

    def _find_item(self, k):
        for next_k, v in iter(self._iter_items()):
            if next_k == k:
                return v
        raise KeyError(k)

    def __iter__(self):
        return (k for k, v in self._iter_items())

class StreamingList(StreamingBase):
    def __init__(self, token_stream) -> None:
        super().__init__(token_stream)
        self._index = -1

    def _load_item(self):
        token_type, item = next(self._stream)
        if token_type == TokenType.OPERATOR:
            if item == ']':
                self._done()
            if item == ',':
                token_type, item = next(self._stream)
            elif item in '{[':
                pass
            else: 
                raise ValueError(f"Expecting a value, comma or ], got {item}")
        if token_type == TokenType.OPERATOR:
            self._child = item = factory(item, self._stream)

        self._index += 1
        return item
    
    def _find_item(self, i):
        if self._index > i:
            raise StreamingAccessException(f"Index {i} already passed in this stream")
        for v in iter(self._iter_items()):
            if self._index == i:
                return v
        raise IndexError(f"Index {i} out of range")


    def _get__iter__(self):
        return self._iter_items()

