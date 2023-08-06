"containers.py -- typed container decorators for methods"

import functools

__all__ = ('container_method', 'container_key', 'container_class')
DUNDER = '__containers__'

class ContainerError(Exception): pass
class NoContainerKey(ContainerError): pass
class NotContainerType(ContainerError, TypeError): pass
class WontOverwriteClassmethod(ContainerError): pass

def check(item, item_class):
    # todo: use STRICT from Container classes
    if not isinstance(item, item_class):
        raise NotContainerType(type(item), item_class)

class DictContainer(dict):
    ITEM_CLASS = None

    def add_value(self, value):
        ""
        if not hasattr(self, 'autokey'):
            raise NoContainerKey
        check(value, self.ITEM_CLASS)
        key = getattr(value, self.autokey)()
        self[key] = value
        return key

    def __setitem__(self, key, value):
        check(value, self.ITEM_CLASS)
        # todo: setting to disallow this when autokey is set
        return super(DictContainer, self).__setitem__(key, value)

    def setdefault(self, *args):
        raise NotImplementedError('todo')

class ListContainer(list):
    ITEM_CLASS = None

    def append(self, value):
        check(value, self.ITEM_CLASS)
        return super(ListContainer, self).append(value)

    def extend(self, *args):
        raise NotImplementedError('todo')

def container(class_, container_class):
    "create a typed container for this class. container_class param should probably be list or dict"
    return getattr(class_, DUNDER)[container_class]()

def setup_class(class_):
    "add DUNDER to class if missing, do nothing if present"
    if not hasattr(class_, DUNDER):
        if hasattr(class_, 'container'):
            raise WontOverwriteClassmethod(class_, 'container')

        class DictSubclass(DictContainer):
            ITEM_CLASS = class_

        class ListSubclass(ListContainer):
            ITEM_CLASS = class_
        
        DictSubclass.__name__ = class_.__name__ + 'DictContainer'
        ListSubclass.__name__ = class_.__name__ + 'ListContainer'
        
        setattr(class_, DUNDER, {
            list: ListSubclass,
            dict: DictSubclass,
        })
        class_.container = classmethod(container)
        return True
    return False

def container_class(class_):
    setup_class(class_)
    cols = getattr(class_, DUNDER)
    for name, method in class_.__dict__.items():
        # note: types & key can both be defined
        if hasattr(method, DUNDER + 'types'):
            col_types = getattr(method, DUNDER + 'types')
            if col_types:
                for col_class in col_types:
                    setattr(cols[col_class], name, method)
            else:
                for col_subclass in cols.values():
                    setattr(col_subclass, name, method)
        
        if hasattr(method, DUNDER + 'key'):
            setattr(cols[dict], 'autokey', name)
    return class_

def container_method(*container_types):
    ""
    def decorator(f):
        setattr(f, DUNDER + 'types', container_types)
        return f
    return decorator

def container_key(f):
    ""
    setattr(f, DUNDER + 'key', True)
    return f
