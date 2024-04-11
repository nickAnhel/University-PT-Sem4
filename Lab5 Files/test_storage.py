from storage import Item, Storage


# Item tests
def test_item_init():
    item = Item("test")
    assert item.title == "test"
    assert item.id is not None


def test_item_to_dict():
    item = Item("test")
    assert item.to_dict() == {"title": "test", "id": str(item.id)}


def test_item_from_dict():
    item: Item = Item("test")
    from_dict_item: Item = Item.from_dict(item.to_dict())
    assert item.id == from_dict_item.id
    assert item.title == from_dict_item.title


# Storage tests
def test_storage_init():
    storage = Storage()
    assert storage.items == []
    assert storage.id is not None


def test_storage_add():
    storage = Storage()
    item = Item("test")
    storage.add(item)
    assert item in storage
    assert storage.items == [item]
    assert len(storage) == 1


def test_storage_pop():
    storage = Storage()
    item = Item("test")
    storage.add(item)
    assert storage.pop() == item
    assert item not in storage
    assert len(storage) == 0


def test_storage_remove():
    storage = Storage()
    item = Item("test")
    storage.add(item)
    storage.remove(item)
    assert item not in storage
    assert len(storage) == 0


def test_storage_clear():
    storage = Storage()
    item = Item("test")
    storage.add(item)
    storage.clear()
    assert storage.items == []
    assert len(storage) == 0


def test_storage_to_dict():
    storage = Storage()
    item = Item("test")
    storage.add(item)
    assert storage.to_dict() == {"id": str(storage.id), "items": [item.to_dict()]}


def test_storage_from_dict():
    storage = Storage()
    item = Item("test")
    storage.add(item)
    from_dict_storage = Storage.from_dict(storage.to_dict())
    assert from_dict_storage.items == storage.items
    assert from_dict_storage.id == storage.id
