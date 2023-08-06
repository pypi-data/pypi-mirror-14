import pytest
import containers

def test_setup_class():
    class C: pass
    assert not hasattr(C, containers.DUNDER)
    containers.setup_class(C)
    assert hasattr(C, containers.DUNDER)

def test_no_overwrite():
    class C:
        def container(self):
            pass

    with pytest.raises(containers.WontOverwriteClassmethod):
        containers.setup_class(C)

def test_list_container():
    @containers.container_class
    class C:
        def __init__(self, x):
            self.x = x
        
        @containers.container_method(list)
        def sum(container):
            return sum(item.x for item in container)

    c_list = C.container(list)
    c_list.append(C(1))
    c_list.append(C(2))
    with pytest.raises(TypeError):
        c_list.append(3)
    assert c_list.sum() == 3

def test_autokey():
    @containers.container_class
    class C:
        def __init__(self, x):
            self.x = x
        
        @containers.container_key
        def key(self):
            return self.x

    c_dict = C.container(dict)
    c_dict.add_value(C(1))
    assert c_dict[1].x == 1
    assert C(1).key() == 1
