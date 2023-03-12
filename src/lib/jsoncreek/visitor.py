from json_creek.json_stream import factory, StreamingObject, StreamingList, StreamingBase
from json_creek.tokenizer import tokenize

def _visit(obj, visitor, path):
    """
    This is going to be a problem on a microcontroller with limited memory.
    """
    k = None
    if isinstance(obj, StreamingObject):
        for k, v in obj.items():
            _visit(v, visitor, path + (k,))
        if k is None:
            visitor({}, path)
    elif isinstance(obj, StreamingList):
        for k, v in enumerate(obj):
            _visit(v, visitor, path + (k,))
        if k is None:
            visitor([], path)
    else:
        visitor(obj,path)


def visit(iterator, visitor):
    """
    visit every kvp in the json file.  
    """
    token_stream = tokenize(iterator)
    _, token = next(token_stream)
    obj = factory(token, token_stream)
    _visit(obj, visitor, ())


def visit_items(iterator, visitor, items):
    """
    visit only the items passed in, disregard the rest
    """
    pass