_sentinel = object()


class BaseMock(object):
    methods = ()

    def passer(self, *args, **kwargs):
        pass

    def __init__(self):
        self.register(self.methods)

    def register(self, methods, stub=_sentinel):
        if stub is _sentinel:
            stub = self.passer

        for m in methods:
            setattr(self, m, stub)


class DummyNode(BaseMock):
    _node_type = 'node'

    methods = (
        'c',
        'extend',
        'clone_base',
        'clone',
        '__invert__',
        'alias',
        'bind_to',
        'asc',
        'desc',
        '__pos__',
        '__neg__',
        '_e',
        '__and__',
        '__or__',
        '__add__',
        '__sub__',
        '__mul__',
        '__div__',
        '__xor__',
        '__radd__',
        '__rsub__',
        '__rmul__',
        '__rdiv__',
        '__rand__',
        '__ror__',
        '__rxor__',
        '__eq__',
        '__ne__',
        '__lt__',
        '__le__',
        '__gt__',
        '__ge__',
        '__lshift__',
        '__rshift__',
        '__mod__',
        '__pow__',
        'bin_and',
        'bin_or',
        'in_',
        'not_in',
        'is_null',
        'contains',
        'startswith',
        'endswith',
        'between',
        'regexp',
        'concat',
    )


DummySQL = DummyNode


class DummyEntity(DummyNode):
    def __init__(self):
        super(DummyEntity, self).__init__()

        new_methods = ('__getattr__',)

        self.register(new_methods)


class DummyField(DummyNode):
    _field_counter = 0
    _order = 0
    _node_type = 'field'
    db_field = 'unknown'

    def __init__(self):
        super(DummyField, self).__init__()

        fields = (
            'null',
            'index',
            'unique',
            'verbose_name',
            'help_text',
            'db_column',
            'default',
            'choices',
            'primary_key',
            'squencee,'
            'constraints',
            'schema',
            '_is_bound'
        )

        self.register(fields, None)

        new_methods = (
            'add_to_class',
            'get_database',
            'get_column_type',
            'get_db_field',
            'get_modifiers',
            'coerce',
            'db_value',
            'python_value',
            'as_entity',
            '__ddl_column__',
            '__ddl__',
            '__hash__',
        )

        self.register(new_methods)


class DummyIntegerField(DummyField):
    db_field = 'int'
    coerce = int


class DummyPrimaryKeyField(DummyIntegerField):
    db_field = 'primary_key'


class DummyQuery(BaseMock):
    """Mock for pylint"""
    require_commit = None

    methods = (
        '_add_query_clauses',
        '_clone_joins',
        '_clone_attributes',
        'clone',
        '__repr__',
        'scalar',
        'execute',
        '_execute',
        'sql',
        'compiler',
        'filter',
        'convert_dict_to_node',
        'ensure_join',
        'switch',
        'join',
        'orwhere',
        'where',
        '_model_shorthand'
    )


class DummySelect(DummyQuery):
    _node_type = None

    def __init__(self):
        super(DummySelect, self).__init__()

        new_methods = (
            'compound_op',
            '_compound_op_static',
            '__or__',
            '__and__',
            '__sub__',
            '__xor__',
            'union_all',
            '__select',
            'select',
            'from_',
            'group_by',
            'having',
            'order_by',
            'window',
            'limit',
            'offset',
            'paginate',
            'distinct',
            'for_update',
            'naive',
            'tuples',
            'dicts',
            'aggregate_rows',
            'alias',
            'annotate',
            'aggregate',
            '_aggregate',
            'count',
            'wrapped_count',
            'exists',
            'get',
            'first',
            'verify_naive',
            'get_query_meta',
            '_get_result_wrapper',
            'execute',
            '__iter__',
            'iterator',
            '__getitem__',
            '__len__',
            '__hash__',
        )

        self.register(new_methods)


class DummyWriteQuery(DummyQuery):
    def __init__(self):
        super(DummyWriteQuery, self).__init__()

        new_methods = (
            'requires_returning',
            'returning',
            'tuples',
            'dicts',
            'get_result_wrapper',
            '_execute_with_result_wrapper',
        )

        self.register(new_methods)


class DummyUpdate(DummyWriteQuery):
    def __init__(self):
        super(DummyUpdate, self).__init__()

        new_methods = (
            'on_conflict',
            '__iter__',
            'iterator',
        )

        self.register(new_methods)


class DummyInsert(DummyWriteQuery):
    def __init__(self):
        super(DummyInsert, self).__init__()

        new_methods = (
            '_iter_rows',
            'upsert',
            'on_conflict',
            'return_id_list',
            'is_insert_returning',
            '_insert_with_loop'
        )

        self.register(new_methods)


class DummyDelete(DummyWriteQuery):
    pass
