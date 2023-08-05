from astroid import MANAGER
from astroid import scoped_nodes

from .mocks import (DummySelect, DummyInsert, DummyDelete, DummyUpdate,
                    DummyPrimaryKeyField)


def register(linter):
    pass


def _returns(ret_val):
    return lambda: ret_val


def transform(cls):
    if 'db.Model' in cls.basenames:
        overrides = {
            'select': _returns(DummySelect()),
            'get': _returns(DummySelect()),
            'insert': _returns(DummyInsert()),
            'update': _returns(DummyUpdate()),
            'delete': _returns(DummyDelete()),
            # @TODO: There has to be a better way to see if the id field is
            # missing or just not needed
            'id': DummyPrimaryKeyField(),
            'create': _returns(cls.instantiate_class()),
        }
        for key in overrides:
            cls.locals[key] = [overrides[key]]


MANAGER.register_transform(scoped_nodes.Class, transform)
