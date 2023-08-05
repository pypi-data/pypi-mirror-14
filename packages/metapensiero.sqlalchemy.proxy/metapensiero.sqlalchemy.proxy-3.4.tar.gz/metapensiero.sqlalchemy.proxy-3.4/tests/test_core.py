# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Tests for ProxiedQuery
# :Created:   mer 03 feb 2016 11:34:16 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2008, 2013, 2014, 2015, 2016 Lele Gaifax
#

from __future__ import absolute_import

from datetime import date

from sqlalchemy import Date, desc, exists, func, select
from sqlalchemy.exc import StatementError

from metapensiero.sqlalchemy.proxy.core import ProxiedQuery
from fixture import Complex, Pet, Session, persons, setup, teardown


def test_slots():
    proxy = ProxiedQuery(persons.select())

    sas = Session()

    for slotname in ('success', 'message', 'count', 'metadata'):
        for value in (True, 'true', 'True'):
            for resultvalue in (False, 'false', 'False', 'None', ''):
                res = proxy(sas, **{'result': resultvalue, slotname: value})
                assert slotname in res
                assert resultvalue not in res

        for value in (False, 'false', 'False', 'None', ''):
            res = proxy(sas, **{'result': 'root', slotname: value})
            assert slotname not in res
            assert value not in res


def test_query_metadata():
    proxy = ProxiedQuery(persons.select())

    sas = Session()

    res = proxy(sas, result=False, metadata='metadata')
    assert res['metadata']['primary_key'] == 'id'

    proxy = ProxiedQuery(Complex.__table__.select())
    res = proxy(sas, result=False, metadata='metadata')
    assert res['metadata']['primary_key'] == ['id1', 'id2']

    proxy = ProxiedQuery(persons.select(), dict(id=False))
    res = proxy(sas, result=False, metadata='metadata')
    assert 'id' not in res['metadata']['fields']


def test_simple_select():
    proxy = ProxiedQuery(persons.select())

    assert 'SELECT ' in str(proxy)

    sas = Session()

    res = proxy(sas, result='root',
                filter_col='lastname', filter_value="foo")
    assert res['message'] == 'Ok'
    assert len(res['root']) == 0

    res = proxy(sas, result='root', only_cols='firstname,lastname',
                filter_col='lastname', filter_value="foo")
    assert res['message'] == 'Ok'
    assert len(res['root']) == 0

    try:
        res = proxy(sas, result='root', only_cols='foo,bar',
                    filter_col='lastname', filter_value="foo")
    except ValueError:
        pass
    else:
        assert False, "Should raise a ValueError"

    res = proxy(sas, result='result',
                filter_col='lastname', filter_value="=foo")
    assert res['message'] == 'Ok'
    assert len(res['result']) == 0

    res = proxy(sas, result='result',
                filter_col='firstname', filter_value="Lele")
    assert res['message'] == 'Ok'
    assert len(res['result']) == 1

    res = proxy(sas, result='result',
                fields='firstname', query="Lele")
    assert res['message'] == 'Ok'
    assert len(res['result']) == 1

    res = proxy(sas, persons.c.firstname == 'Lele', result='result')
    assert res['message'] == 'Ok'
    assert len(res['result']) == 1

    res = proxy(sas, persons.c.firstname == 'Lele', persons.c.lastname == 'Gaifax',
                result='result')
    assert res['message'] == 'Ok'
    assert len(res['result']) == 0

    res = proxy(sas, result='result', count='count',
                filter_firstname="Lele")
    assert res['message'] == 'Ok'
    assert len(res['result']) == res['count']

    for none in (None, 'None', 'False', 'false'):
        res = proxy(sas, result=none, count='count')
        assert res['message'] == 'Ok'
        assert none not in res
        assert 'result' not in res
        assert res['count'] > 1

    res = proxy(sas, result='result', count='count', start=1, limit=1)
    assert res['message'] == 'Ok'
    assert len(res['result']) == 1
    assert res['count'] > 1

    res = proxy(sas, result=True, asdict=True)
    assert len(res) == 2
    assert 'goodfn' in res[0]

    res = proxy(sas, result=None, metadata='metadata')
    assert res['message'] == 'Ok'
    assert res['metadata']['fields']

    res = proxy(sas, result='True', sort="firstname")
    assert res[1].firstname > res[0].firstname

    res = proxy(sas, sort="firstname", dir="DESC")
    assert res[0].firstname > res[1].firstname


def test_simple_select_decl():
    proxy = ProxiedQuery(Pet.__table__.select())

    sas = Session()

    res = proxy(sas, result='root', filter_col='name', filter_value="foo")
    assert res['message'] == 'Ok'
    assert len(res['root']) == 0

    res = proxy(sas, filter_name='Yacu')
    assert len(res) == 1

    res = proxy(sas, filter_='Yacu')
    assert len(res) > 1

    res = proxy(sas, filter_timestamp="2009-12-07T19:00:00,2009-12-07T19:00:00",
                result=False, count='count', format=None)
    assert res['count'] == 2

    proxy = ProxiedQuery(persons.select())

    res = proxy(sas, filter_timestamp="2009-12-07T19:00:00,2009-12-07T19:00:00",
                result=False, count='count', format=None)
    assert res['count'] == 1

    proxy = ProxiedQuery(select([persons.c.firstname.label('FN')]))

    res = proxy(sas, result=False, metadata='metadata')
    assert len(res['metadata']['fields']) == 1
    assert res['metadata']['fields'][0]['label'] == 'First name'


def test_with_join():
    pets = Pet.__table__
    proxy = ProxiedQuery(
        select([persons.c.firstname, func.count(pets.c.id).label('number')],
               from_obj=persons.outerjoin(pets)).group_by(persons.c.firstname),
        dict(number=dict(label='Number',
                         hint='Number of pets')))

    sas = Session()

    res = proxy(sas, result='root', metadata='metadata')
    assert len(res['root']) == 2
    assert res['metadata']['fields'][0]['label'] == 'First name'
    assert res['metadata']['fields'][1]['label'] == 'Number'

    res = proxy(sas, sort="number")
    assert res[0].firstname == 'Lallo'

    res = proxy(sas, sort="number", dir="DESC")
    assert res[0].firstname == 'Lele'

    res = proxy(sas, sort='[{"property":"number","direction":"DESC"},{"property":"non-existing","direction":"ASC"}]')
    assert res[0].firstname == 'Lele'

    proxy = ProxiedQuery(
        select([persons.c.id, persons.c.birthdate, pets.c.birthdate],
               from_obj=persons.outerjoin(pets)))

    res = proxy(sas, result=False, count='count', filter_birthdate=None)
    assert res['count'] == 0

    proxy = ProxiedQuery(
        select([persons.c.firstname],
               from_obj=persons.outerjoin(pets)))

    res = proxy(sas, result=False, count='count', filter_persons_id=-1)
    assert res['count'] == 0

    res = proxy(sas, result=False, count='count', filter_weight=1)
    assert res['count'] == 0

    proxy = ProxiedQuery(
        select([persons.c.firstname, pets.c.name],
               from_obj=persons.outerjoin(pets)))

    res = proxy(sas, result=False, count='count', filter_birthdate=None)
    assert res['count'] == 0


def test_with_aliased_join():
    persons_alias = persons.alias('prs')
    pets_alias = Pet.__table__.alias('pts')
    proxy = ProxiedQuery(select([persons_alias.c.firstname, pets_alias.c.name],
                                from_obj=persons_alias.join(pets_alias)))

    sas = Session()

    res = proxy(sas, result='root', metadata='metadata')
    assert len(res['root']) == 2
    assert res['metadata']['fields'][0]['label'] == 'First name'
    assert res['metadata']['fields'][1]['label'] == 'Pet name'


def test_with_labelled_aliased_join():
    persons_alias = persons.alias('prs')
    pets_alias = Pet.__table__.alias('pts')
    proxy = ProxiedQuery(select([persons_alias.c.firstname.label('Person'),
                                 pets_alias.c.name.label('PetName')],
                                from_obj=persons_alias.join(pets_alias)))

    sas = Session()

    res = proxy(sas, result='root', metadata='metadata')
    assert len(res['root']) == 2
    assert res['metadata']['fields'][0]['label'] == 'First name'
    assert res['metadata']['fields'][1]['name'] == 'PetName'
    assert res['metadata']['fields'][1]['label'] == 'Pet name'


def test_select_with_bindparams():
    from sqlalchemy.sql import bindparam

    query = select([persons.c.firstname],
                   persons.c.birthdate == bindparam('birth', type_=Date,
                                                    value=date(1955, 9, 21)))
    proxy = ProxiedQuery(query)

    sas = Session()

    res = proxy(sas, result='root')
    assert res['message'] == 'Ok'
    assert len(res['root']) == 1
    assert res['root'][0][0] == 'Lallo'

    res = proxy(sas, result=False, count='count')
    assert res['count'] == 1

    res = proxy(sas, result=False, count='count',
                params=dict(birth=date(2000, 1, 1)))
    assert res['count'] == 0

    res = proxy(sas, result='root',
                params=dict(birth=date(1968, 3, 18)))
    assert res['message'] == 'Ok'
    assert len(res['root']) == 1
    assert res['root'][0][0] == 'Lele'

    res = proxy(sas, result='root',
                params=dict(birth=date(2000, 1, 1), foo=1))
    assert res['message'] == 'Ok'
    assert len(res['root']) == 0

    res = proxy(sas, result='root', params=dict(birth="1968-03-18"))
    assert res['message'] == 'Ok'
    assert len(res['root']) == 1
    assert res['root'][0][0] == 'Lele'


def test_select_with_typeless_bindparams():
    from sqlalchemy.sql import bindparam

    query = select([persons.c.firstname],
                   persons.c.birthdate == bindparam('birth'))
    proxy = ProxiedQuery(query)

    sas = Session()

    res = proxy(sas, result='root', params=dict(birth=None))
    assert res['message'] == 'Ok'
    assert len(res['root']) == 0

    res = proxy(sas, result=False, count='count', params=dict(birth=None))
    assert res['count'] == 0

    res = proxy(sas, result='root', params=dict(birth=date(1968, 3, 18)))
    assert res['message'] == 'Ok'
    assert len(res['root']) == 1
    assert res['root'][0][0] == 'Lele'

    res = proxy(sas, result='root', params=dict(birth="1968-03-18"))
    assert res['message'] == 'Ok'
    assert len(res['root']) == 1
    assert res['root'][0][0] == 'Lele'

    res = proxy(sas, result=False, count='count',
                params=dict(birth="1968-03-18"))
    assert res['message'] == 'Ok'
    assert res['count'] == 1

    res = proxy(sas, result=False, count='count',
                params=dict(birth="1968-03-18",
                            foo="bar"))
    assert res['message'] == 'Ok'
    assert res['count'] == 1

    try:
        proxy(sas, result=False, count='count')
    except StatementError:
        pass
    else:
        assert False, "Should raise a StatementError"


def test_select_ordered_on_subselect():
    pets = Pet.__table__
    query = select([persons.c.firstname,
                    exists()
                    .where(pets.c.person_id == persons.c.id)
                    .label("Petted")]) \
            .order_by(desc("Petted"))
    proxy = ProxiedQuery(query)

    sas = Session()

    res = proxy(sas, result='root', count='count')
    assert res['count'] == 2
    assert res['root'][0]['firstname'] == 'Lele'


def test_select_with_aggregate_function():
    pets = Pet.__table__
    query = select([persons.c.id,
                    persons.c.firstname,
                    func.group_concat(pets.c.name).label("Pets")],
                   pets.c.person_id == persons.c.id) \
            .group_by(persons.c.id)
    proxy = ProxiedQuery(query)

    sas = Session()

    res = proxy(sas, result='root', count='count', metadata='metadata')
    assert res['count'] == 1
    assert res['root'][0]['firstname'] == 'Lele'
    assert res['metadata']['fields'][1]['label'] == 'First name'
    assert res['metadata']['fields'][2]['label'] == 'Pets'
    assert res['metadata']['fields'][2]['type'] == 'string'


# Silence pylint
setup, teardown
