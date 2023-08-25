from spycular.pointer.object_pointer import GetPointer
from spycular.store.virtual_store import VirtualStore


def test_create_virtual_store():
    store = VirtualStore()
    assert store.store == {}


def test_virtual_store_save():
    store = VirtualStore()
    for i in range(100):
        store.save(str(i), i)
    assert len(store.store) == 100


def test_virtual_store_get():
    store = VirtualStore()
    for i in range(100):
        store.save(str(i), i)
    for i in range(100):
        assert store.get(str(i)) == i


def test_virtual_store_get_all():
    store = VirtualStore()
    obj_list = list(range(100, 0, -1))
    for i in range(100):
        store.save(str(i), obj_list[i])
    assert len(store.get_all()) == 100
    assert list(store.get_all(0, 10).values()) == obj_list[0:10]
    assert list(store.get_all(1, 10).values()) == obj_list[10:20]
    assert list(store.get_all(2, 10).values()) == obj_list[20:30]
    assert list(store.get_all(3, 10).values()) == obj_list[30:40]
    assert list(store.get_all(4, 10).values()) == obj_list[40:50]
    assert list(store.get_all(5, 10).values()) == obj_list[50:60]
    assert list(store.get_all(6, 10).values()) == obj_list[60:70]
    assert list(store.get_all(7, 10).values()) == obj_list[70:80]
    assert list(store.get_all(8, 10).values()) == obj_list[80:90]
    assert list(store.get_all(9, 10).values()) == obj_list[90:100]
    assert list(store.get_all(-9, 10).values()) == []
    assert list(store.get_all(9, -10).values()) == []
    assert list(store.get_all(10, 11).values()) == []
    assert len(store.get_all(10, 10)) == 0


def test_virtual_store_delete():
    store = VirtualStore()
    for i in range(100):
        store.save(str(i), i)
    for i in range(100):
        assert len(store.store) == 100 - i
        store.delete(str(i))
    assert len(store.store) == 0


def test_virtual_store_has():
    store = VirtualStore()
    for i in range(100):
        store.save(str(i), i)
    for i in range(100):
        assert store.has(str(i))
        store.delete(str(i))
        assert not store.has(str(i))


def test_consumer_get_all(np, consumer, replies):
    for i in range(100):
        np.array([i, i, i, i])

    get_ptr = []
    for i in range(10):
        ptr = GetPointer(page_index=i, page_size=10)
        np.broker.send(ptr)
        get_ptr.append(ptr)

    consumer.listen()

    last_start = 0
    for ptr in get_ptr:
        end = last_start + 10
        assert {
            key: value
            for key, value in list(consumer.storage.store.items())[
                last_start:end
            ]
        } == replies[ptr.id]
        last_start += 10
