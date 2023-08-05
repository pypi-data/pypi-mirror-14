# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Core variant of the proxy
# :Created:   mer 03 feb 2016 11:12:51 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from __future__ import absolute_import, unicode_literals

import logging

from sqlalchemy import and_, func, select
from sqlalchemy.sql.expression import Selectable

from .base import ProxiedBase
from .utils import apply_filters, get_adaptor_for_type


log = logging.getLogger(__name__)


class ProxiedQuery(ProxiedBase):
    """Facility class to expose a SQLAlchemy statement to Pylons.

    An instance of this class wraps a standard SQLAlchemy query,
    either a selectable or an updateable. When called it applies the
    arguments filtering or changing the original query, calling it
    and returning the results set.
    """

    def __init__(self, query, metadata=None):
        """Initialize the proxy.

        `query` is the basic SA statement, either a ``SELECT`` or any
        *DML* statement (although only the first kind is currently
        supported!).

        `metadata` is a dictionary, containing extra information
        about fields: when possibile, these info are collected from
        the SA definition (each field has a `info` dictionary); for
        computed fields when the returned value does not correspond to
        a physical field, or simply to override/expand such
        information on a per query basis, you may pass an additional
        dictionary of values, keyed on the field name.
        """

        super(ProxiedQuery, self).__init__()

        self.query = query
        self.metadata = metadata

    def __str__(self):
        return str(self.query)

    def filterQueryWithArgs(self, session, conditions, args):
        """Apply filter conditions to the query.

        `conditions`, if specified, is a list of SQLAlchemy
        expressions to be applied as filters to the query, using
        the ``AND`` operator.

        The query gets then massaged by `apply_filters()`, further
        filtered and modified as specified by the `args` dictionary.

        Return the altered query.
        """

        if conditions:
            if len(conditions)>1:
                query = self.query.where(and_(*conditions))
            else:
                query = self.query.where(conditions[0])
        else:
            query = self.query
        query, only_cols = apply_filters(query, args)

        values = self.params = {}
        params = args.pop('params', None)
        if params is not None:
            from sqlalchemy.sql.visitors import traverse

            # Extract the eventual bindparams from the query and
            # adapt each argument value to the declared type.
            def adapt_args(bind):
                if bind.key in params and bind.key not in values:
                    coerce_value = get_adaptor_for_type(bind.type)
                    values[bind.key] = coerce_value(params[bind.key])
            traverse(query, {},  {'bindparam': adapt_args})

        return query

    def getColumns(self, query):
        """Return the selected columns."""

        return query.inner_columns

    def getCount(self, session, query):
        """Execute a query to get the actual count of matching records."""

        pivot = next(query.inner_columns)
        simple = query.with_only_columns([pivot]).order_by(None)
        tquery = select([func.count()], from_obj=simple.alias('cnt'))
        return session.execute(tquery, self.params).scalar()

    def getResult(self, session, query, asdict):
        """Execute the query in the given session, returning the result.

        If `asdict` is `True` return a list of dictionaries, one for
        each row, otherwise return the SQLAlchemy resultset (as
        returned by ``.fetchall()``).
        """

        # XXX: this does not currently handle SA Updateables!

        if isinstance(query, Selectable):
            result = session.execute(query, self.params)
            if asdict:
                fn2key = dict((c.name, c.key) for c in self.getColumns(query))
                result = [dict((fn2key[fn], r[fn]) for fn in fn2key) for r in result]
            else:
                result = result.fetchall()
        else:
            result = None
        return result

    def getMetadata(self, session, query, countslot, resultslot, successslot):
        """Augment superclass implementation with primary key name.

        Beware, this implements a rather simplicistic heuristic such that it
        identifies only the primary key of the first table involved in the
        query: in other words, it assumes that the primary key fields come
        as early as possible in the list of columns.
        """

        result = super(ProxiedQuery, self).getMetadata(session, query,
                                                       countslot, resultslot,
                                                       successslot)

        pk = []
        pkt = None
        pkl = 0
        for c in self.getColumns(query):
            if getattr(c, 'table', False) is not False and getattr(c, 'primary_key', False):
                if pkt is None:
                    pkt = c.table
                    pkl = len(pkt.primary_key)
                if c.table is pkt:
                    pk.append(c)
                    if len(pk) == pkl:
                        break

        if pk and pkl == len(pk):
            if len(pk) == 1:
                result['primary_key'] = pk[0].name
            else:
                result['primary_key'] = [c.name for c in pk]
        else:
            log.warning("Could not determine primary key fields"
                        " for query %s", query)

        return result
