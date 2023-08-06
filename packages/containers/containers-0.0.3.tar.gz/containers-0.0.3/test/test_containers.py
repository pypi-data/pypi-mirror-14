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

@containers.container_class
class C:
    def __init__(self, x):
        self.x = x
    
    @containers.container_key
    def key(self):
        return self.x

    @containers.container_method()
    def sum(container):
        return sum(item.x for item in container.values())

def test_list_container():
    c_list = C.container(list)
    [c_list.append(C(i)) for i in (1,2)]
    with pytest.raises(TypeError):
        c_list.append(3)
    assert c_list.sum() == 3
    assert c_list.values() == c_list

def test_dict_container():
    c_dict = C.container(dict)
    [c_dict.add_value(C(i)) for i in (1,2)]
    with pytest.raises(TypeError):
        c_dict.add_value(3)
    assert c_dict.sum() == 3

def test_autokey():
    c_dict = C.container(dict)
    c_dict.add_value(C(1))
    assert c_dict[1].x == 1
    assert C(1).key() == 1

def test_multimap():
    mm = C.container('multimap')
    [mm.append_value(C(i)) for i in (1,2)]
    with pytest.raises(TypeError):
        mm.append_value(3)
    assert mm.sum() == 3
    mm.append_value(C(1))
    assert mm.sum() == 4
    assert list(mm.itervalues()) == mm.values()
    assert len(mm[1]) == 2
    assert len(mm[2]) == 1
    assert len(mm[3]) == 0
