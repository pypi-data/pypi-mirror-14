
def interpretValue(value,*args,**kwargs):
    """Interprets a passed value. In this order:
     - If it's callable, call it with the parameters provided
     - If it's a tuple/list/dict and we have a single, non-kwarg parameter, look up that parameter within the tuple/list/dict
     - Else, just return it
     """
    if callable(value): return value(*args,**kwargs)
    if isinstance(value,tuple) or isinstance(value,list) or isinstance(value,dict):
        if len(args)==1 and kwargs=={}:
            return value[args[0]]
    return value


def specialInterpretValue(value,index,*args,**kwargs):
    """Interprets a passed value. In this order:
     - If it's callable, call it with the parameters provided
     - If it's a tuple/list/dict and index is not None, look up index within the tuple/list/dict
     - Else, just return it
     """
    if callable(value): return value(*args,**kwargs)
    if index is not None and (isinstance(value,tuple) or isinstance(value,list) or isinstance(value,dict)): return value[index]
    return value
