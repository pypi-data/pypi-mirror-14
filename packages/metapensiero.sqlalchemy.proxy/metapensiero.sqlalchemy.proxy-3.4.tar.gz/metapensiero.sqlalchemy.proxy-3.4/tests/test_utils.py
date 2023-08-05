# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Tests for utility functions
# :Created:   mer 03 feb 2016 11:23:52 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from __future__ import absolute_import

from datetime import date, datetime

from metapensiero.sqlalchemy.proxy.utils import compare_field, extract_raw_conditions
from fixture import persons


def test_extract_raw_conditions():
    erc = extract_raw_conditions

    rc = erc(dict(filter_col='foo', filter_value='bar'))
    assert rc == [('foo', 'bar')]

    rc = erc(dict(filter_col='foo'))
    assert rc == []

    rc = erc(dict(filter=[dict(property='foo', value='bar', operator='<')]))
    assert rc == [('foo', '<bar')]

    rc = erc(dict(filter=[dict(property='foo', value=1, operator='<')]))
    assert rc == [('foo', '<1')]

    rc = erc(dict(filter=[dict(property='foo', operator='<')]))
    assert rc == []

    rc = erc(dict(filter='[{"property": "foo", "value": "bar", "operator": "<"}]'))
    assert rc == [('foo', '<bar')]

    rc = erc(dict(filter_foo='bar'))
    assert rc == [('foo', 'bar')]


def test_compare_field():
    cf = compare_field

    expr = cf(persons.c.firstname, u'>=foo')
    s = str(expr)
    assert ' >= ' in s

    expr = cf(persons.c.firstname, u'>foo')
    s = str(expr)
    assert ' > ' in s

    expr = cf(persons.c.firstname, u'<=foo')
    s = str(expr)
    assert ' <= ' in s

    expr = cf(persons.c.firstname, u'<foo')
    s = str(expr)
    assert ' < ' in s

    expr = cf(persons.c.firstname, u'=foo')
    s = str(expr)
    assert ' = ' in s

    expr = cf(persons.c.firstname, u'<>foo')
    s = str(expr)
    assert ' != ' in s

    expr = cf(persons.c.firstname, u'~=foo')
    s = str(expr)
    assert 'LIKE ' in s

    expr = cf(persons.c.firstname, u'foo')
    s = str(expr)
    assert 'LIKE ' in s

    expr = cf(persons.c.firstname, u'~foo')
    s = str(expr)
    assert 'LIKE ' in s

    expr = cf(persons.c.firstname, u'NULL')
    s = str(expr)
    assert ' IS NULL' in s

    expr = cf(persons.c.firstname, u'!NULL')
    s = str(expr)
    assert ' IS NOT NULL' in s

    expr = cf(persons.c.firstname, u'<>NULL')
    s = str(expr)
    assert ' IS NOT NULL' in s

    expr = cf(persons.c.firstname, u'foo,bar')
    s = str(expr)
    assert ' IN (' in s

    expr = cf(persons.c.firstname, u'<>foo,bar')
    s = str(expr)
    assert ' NOT IN (' in s

    expr = cf(persons.c.id, (1,))
    s = str(expr)
    assert ' = ' in s
    assert ' IN (' not in s

    expr = cf(persons.c.id, (1, 2))
    s = str(expr)
    assert ' IN (' in s

    expr = cf(persons.c.id, '1,2')
    s = str(expr)
    assert ' IN (' in s

    expr = cf(persons.c.id, 'NULL,2')
    s = str(expr)
    assert ' IS NULL' in s
    assert ' OR ' in s
    assert ' = ' in s

    expr = cf(persons.c.id, (None, 2))
    s = str(expr)
    assert ' IS NULL' in s
    assert ' OR ' in s
    assert ' = ' in s

    expr = cf(persons.c.id, 'NULL,1,2')
    s = str(expr)
    assert ' IS NULL' in s
    assert ' OR ' in s
    assert ' IN (' in s

    expr = cf(persons.c.id, (None, 1, 2))
    s = str(expr)
    assert ' IS NULL' in s
    assert ' OR ' in s
    assert ' IN (' in s

    expr = cf(persons.c.id, '<>NULL,2')
    s = str(expr)
    assert 'NOT (' in s
    assert ' IS NULL' in s
    assert ' OR ' in s
    assert ' = ' in s

    expr = cf(persons.c.id, '<>NULL,1,2')
    s = str(expr)
    assert 'NOT (' in s
    assert ' IS NULL' in s
    assert ' OR ' in s
    assert ' IN (' in s

    expr = cf(persons.c.id, dict(start=1, end=2))
    s = str(expr)
    assert ' BETWEEN ' in s

    expr = cf(persons.c.id, dict(start=None, end=2))
    s = str(expr)
    assert ' <= ' in s

    expr = cf(persons.c.id, dict(end=2))
    s = str(expr)
    assert ' <= ' in s

    expr = cf(persons.c.id, dict(start=1, end=None))
    s = str(expr)
    assert ' >= ' in s

    expr = cf(persons.c.id, dict(start=1))
    s = str(expr)
    assert ' >= ' in s

    try:
        expr = cf(persons.c.id, dict(start=None, end=None))
    except UserWarning:
        pass

    expr = cf(persons.c.id, '<>0')
    s = str(expr)
    # sqlite uses !=, others use <> ...
    assert (' <> ' in s) or (' != ' in s)
    assert 'NULL' not in s

    expr = cf(persons.c.birthdate, dict(start=date.today()))
    s = str(expr)
    assert ' >= ' in s

    expr = cf(persons.c.birthdate, dict(start=datetime.now()))
    s = str(expr)
    assert ' >= ' in s

    expr = cf(persons.c.birthdate, dict(end=date.today()))
    s = str(expr)
    assert ' <= ' in s

    expr = cf(persons.c.birthdate, dict(start=date.today(),
                                        end=date.today()))
    s = str(expr)
    assert ' BETWEEN ' in s

    expr = cf(persons.c.timestamp, dict(start=None, end=datetime.now()))
    s = str(expr)
    assert ' <= ' in s

    expr = cf(persons.c.timestamp, dict(start="2008-08-01",
                                        end=datetime.now()))
    s = str(expr)
    assert ' BETWEEN ' in s

    expr = cf(persons.c.timestamp, "2008-08-01T10:10:10,2009-07-01T12:12:12")
    s = str(expr)
    assert ' IN (' in s

    expr = cf(persons.c.timestamp, "2008-08-01T10:10:10><2009-07-01T12:12:12")
    s = str(expr)
    assert ' BETWEEN ' in s

    expr = cf(persons.c.id, "2><9")
    s = str(expr)
    assert ' BETWEEN ' in s

    expr = cf(persons.c.id, "><7")
    s = str(expr)
    assert ' <= ' in s

    expr = cf(persons.c.id, "2><")
    s = str(expr)
    assert ' >= ' in s

    expr = cf(persons.c.id, ">0")
    s = str(expr)
    assert ' > ' in s

    expr = cf(persons.c.smart, None)
    s = str(expr)
    assert ' IS NULL' in s

    expr = cf(persons.c.smart, True)
    s = str(expr)
    assert 'smart' in s

    expr = cf(persons.c.somevalue, 1)
    s = str(expr)
    assert 'somevalue' in s
