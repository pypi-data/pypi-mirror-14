"containers.py -- typed container decorators for methods"

import six

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

def common_add_value(dict_like, value):
    "this is like __setitem__ but the key is automatic"
    if not hasattr(dict_like, 'autokey'):
        raise NoContainerKey
    check(value, dict_like.ITEM_CLASS)
    key = getattr(value, dict_like.autokey)()
    dict_like[key] = value
    return key

class DictContainer(dict):
    ITEM_CLASS = None

    def add_value(self, value):
        return common_add_value(self, value)

    def __setitem__(self, key, value):
        check(value, self.ITEM_CLASS)
        # todo: setting to disallow this when autokey is set
        return super(DictContainer, self).__setitem__(key, value)

    def setdefault(self, *args):
        raise NotImplementedError('todo')

class MultimapContainer(dict):
    ITEM_CLASS = None
    LIST_CLASS = None

    def __getitem__(self, key):
        list_ = self.get(key)
        if list_ is None:
            newlist = self.LIST_CLASS()
            super(MultimapContainer, self).__setitem__(key, newlist)
            return newlist
        else:
            return list_

    def append(self, key, value):
        self[key].append(value)

    def __setitem__(self, key, value):
        check(value, self.LIST_CLASS)
        # todo: setting to disallow this when autokey is set
        super(MultimapContainer, self).__setitem__(key, value)

    def append_value(self, value):
        "like append() but with automatic key"
        if not hasattr(self, 'autokey'):
            raise NoContainerKey
        check(value, self.ITEM_CLASS)
        key = getattr(value, self.autokey)()
        self.append(key, value)
        return key

    def values(self):
        return sum(super(MultimapContainer, self).values(), self.LIST_CLASS())

    def itervalues(self):
        # todo: values vs itervalues should be consistent with py2 / py3 standards
        for list_ in six.itervalues(super(MultimapContainer, self)):
            for item in list_:
                yield item

class ListContainer(list):
    ITEM_CLASS = None

    def append(self, value):
        check(value, self.ITEM_CLASS)
        return super(ListContainer, self).append(value)

    def extend(self, *args):
        raise NotImplementedError('todo')

    def values(self):
        "this exists so some container_methods can work on lists and dicts"
        return self

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

        class MultimapSubclass(MultimapContainer):
            ITEM_CLASS = class_
            LIST_CLASS = ListSubclass
        
        DictSubclass.__name__ = class_.__name__ + 'DictContainer'
        ListSubclass.__name__ = class_.__name__ + 'ListContainer'
        MultimapSubclass.__name__ = class_.__name__ + 'MultimapContainer'
        
        setattr(class_, DUNDER, {
            list: ListSubclass,
            dict: DictSubclass,
            'multimap': MultimapSubclass
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
            setattr(cols['multimap'], 'autokey', name)
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
