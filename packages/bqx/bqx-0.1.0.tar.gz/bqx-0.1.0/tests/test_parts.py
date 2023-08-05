"""
Test of bqx.parts.

Run Test: `tox` or `python setup.py test`
"""

import pytest
from bqx.parts import Table, Column


table = Table('table')
table_as = Table('table').AS('tbl')
column = Column('column')
column_as = Column('column').AS('col')


def test_table():
    with pytest.raises(Exception):
        table.column  # Access column without defining alias

    assert str(table_as) == 'tbl'
    assert str(table_as.column) == 'tbl.column'


def test_column():
    ops = [
        (column_as.__lt__, '<'),
        (column_as.__le__, '<='),
        (column_as.__eq__, '='),
        (column_as.__ne__, '!='),
        (column_as.__gt__, '>'),
        (column_as.__ge__, '>='),
        (column_as.__add__, '+'),
        (column_as.__sub__, '-'),
        (column_as.__mul__, '*'),
        (column_as.__truediv__, '/'),
        (column_as.__mod__, '%'),
        (column_as.__and__, '&'),
        (column_as.__or__, '|'),
    ]

    for op, rep in ops:
        assert op(column_as) == 'col %s col' % rep
        assert op(column) == 'col %s column' % rep


def test_complex_calc():
    assert str(column_as + column_as + column_as + column_as) == '((col + col) + col) + col'
    assert str(column_as + column_as - column_as * column_as / column_as) == '(col + col) - (col * col) / col'