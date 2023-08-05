# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Tests fixtures
# :Created:   mer 03 feb 2016 11:26:04 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from datetime import date, datetime

from sqlalchemy import (Boolean, Column, Date, DateTime, ForeignKey,
                        Integer, MetaData, Numeric, String, Text,
                        Table, create_engine, orm)
from sqlalchemy.exc import SAWarning
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator


class Title(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        return value and value.title()


def birthdate_info(name):
    return {
        'min': date(1980, 1, 1),
        'max': lambda fname, iname: date.today()
    }

metadata = MetaData()

persons = Table('persons', metadata,
                Column('id', Integer, primary_key=True),
                Column('firstname', String, info=dict(label="First name",
                                                      hint="The first name of the person")),
                Column('lastname', String),
                Column('birthdate', Date, info=birthdate_info),
                Column('timestamp', DateTime),
                Column('smart', Boolean),
                Column('somevalue', Integer),
                Column('title', Title),
                Column('WeirdFN', String, key='goodfn'),
                )

class Person(object):
    def __init__(self, firstname, lastname, birthdate, timestamp, smart, title, goodfn):
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.timestamp = timestamp
        self.smart = smart
        self.somevalue = 0
        self.title = title
        self.goodfn = goodfn

orm.mapper(Person, persons)


class Pet(declarative_base(metadata=metadata)):
    __tablename__ = 'pets'

    id = Column(Integer, primary_key=True,
                info=dict(label='id', hint='the pet id'))
    name = Column(String, info=dict(label='Pet name', hint='The name of the pet'))
    person_id = Column(Integer, ForeignKey('persons.id'))
    birthdate = Column(Date, info=birthdate_info)
    weight = Column(Numeric(5,2),
                    info=dict(label='weight', hint='the weight'))
    notes = Column(Text, info=dict(label='notes', hint='random notes'))

    person = orm.relation(Person, backref=orm.backref('pets', order_by=id))


class Complex(declarative_base(metadata=metadata)):
    __tablename__ = 'complex'

    id1 = Column(Integer, primary_key=True,
                 info=dict(label='id1', hint='the first part of id'))
    id2 = Column(Integer, primary_key=True,
                 info=dict(label='id2', hint='the second part of id'))
    name = Column(String)


# Note: the echoed statements will be visible with "py.test -s"
engine = create_engine('sqlite:///:memory:', echo=True)
Session = orm.sessionmaker(bind=engine)

def setup():
    import warnings

    # Silence the warning about Decimal usage with sqlite
    warnings.filterwarnings(
        action='ignore', category=SAWarning,
        message=r'.*sqlite\+pysqlite does \*not\* support Decimal objects.*')

    metadata.create_all(engine)

    session = Session()

    me = Person('Lele', 'Gaifas', date(1968, 3, 18),
                datetime(2009, 12, 7, 19, 0, 0), False,
                "perito industriale", "foo")
    session.add(me)

    bro = Person('Lallo', 'Gaifas', date(1955, 9, 21),
                 datetime(2009, 12, 7, 20, 0, 0), True,
                 "ingegnere", "bar")
    session.add(bro)

    yaku = Pet(name='Yacu')
    yaku.person = me
    session.add(yaku)

    laika = Pet(name='Laika')
    laika.person = me
    session.add(laika)

    session.commit()


def teardown():
    metadata.drop_all(engine)
