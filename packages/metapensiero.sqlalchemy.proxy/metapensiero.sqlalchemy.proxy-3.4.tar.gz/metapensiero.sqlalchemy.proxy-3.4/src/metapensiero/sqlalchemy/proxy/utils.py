# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Utility functions
# :Created:   mer 03 feb 2016 10:56:36 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from __future__ import absolute_import, unicode_literals

from collections import Mapping, Sequence
from datetime import datetime
import logging

from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, and_, not_, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.query import Query
from sqlalchemy.sql.elements import BinaryExpression

from .json import json2py


log = logging.getLogger(__name__)


try:
    basestring
except NameError: # pragma: nocover
    # Py3 compatibility
    basestring = str


def get_exception_message(e):
    """Extract the error message from the given exception.

    :param e: an Exception instance
    :rtype: a unicode string
    """

    msg = str(e)
    if isinstance(msg, bytes):
        for enc in ('utf-8', 'latin1'):
            try:
                msg = msg.decode(enc)
            except UnicodeDecodeError:
                pass
            else:
                break
        else:
            msg = msg.decode('utf-8', errors='replace')
    return msg


def get_adaptor_for_type(satype):
    """Create an adaptor for the given type.

    :param satype: an SQLAlchemy ``TypeEngine``
    :rtype: a function

    Create and return a function that adapts its unique argument
    to the given `satype`.
    """

    if isinstance(satype, Integer):
        coerce_value = lambda s: int(s) if s else None
    elif isinstance(satype, (Date, DateTime)):
        def coerce_date(s):
            if isinstance(s, basestring):
                res = s and json2py('"%s"' % s) or None
            else:
                res = s
            if isinstance(satype, Date) and isinstance(s, datetime):
                res = s.date()
            return res
        coerce_value = coerce_date
    elif isinstance(satype, Boolean):
        def coerce_boolean(s):
            if isinstance(s, basestring):
                return s.lower() == 'true'
            else:
                return bool(s)
        coerce_value = coerce_boolean
    else:
        coerce_value = lambda s: s if s else None

    return coerce_value


def _compare_with_values(field, values, coerce_value):
    """Helper function to build ``IN`` comparisons."""

    negate = False

    if isinstance(values, basestring):
        if values.startswith('<>'):
            values = values[2:]
            negate = True

        values = values.split(',')

        null = 'NULL'
        has_nulls = 'NULL' in values
    else:
        null = None
        has_nulls = None in values

    if has_nulls:
        other_values = [coerce_value(v) for v in values if v != null]
        if len(other_values) > 1:
            expr = or_(field == None, field.in_(other_values))
        else:
            expr = or_(field == None, field == other_values[0])
    else:
        if len(values) > 1:
            expr = field.in_([coerce_value(v) for v in values])
        else:
            expr = field == coerce_value(values[0])

    if negate:
        expr = not_(expr)

    return expr


def compare_field(field, value):
    """Build a comparison expression for the field.

    :param field: an SQLAlchemy ``Column``
    :param value: the value to compare with
    :rtype: an SQLALchemy ``Expression``

    Taking into account both the type of the field and of the value,
    create an SQLAlchemy expression usable as a filter on the field.

    If `value` is a string containing one or more commas (``,``), or a
    *sequence* (i.e. ``list`` or ``tuple``), the expression will use
    the ``IN`` operator to compare the field against all specified
    values; the string value may start with ``<>``: this negates the
    expression giving a ``NOT IN``. If the string contains a ``NULL``
    value, then this generates an expression like
    ``field IS NULL OR field IN (...)``.

    If `value` is a dictionary containing at least one of the keys
    `start` and `end` or a string like ``start><end``, then the expression
    will be something like ``field BETWEEN :start AND :end`` if both
    values are present, or ``field >= :start`` if `end` is not given or
    ``None``, otherwise ``field <= :end``.

    `value` can be prefixed with ``>=``, ``>``, ``=``, ``<``, ``<=`` or
    ``<>``, with the obvious meaning. ``~=value`` is translated into
    ``field ILIKE value%``. If the prefix is ``~``, or not recognized,
    the generated filter expression will be ``field ILIKE %value%``.

    Finally, `value` can be ``NULL`` to mean ``field IS NULL``,
    or ``!NULL`` or even ``<>NULL`` with the opposit meaning.
    """

    try:
        ftype = field.type
        try:
            ftype = ftype.impl
        except AttributeError:
            pass

        coerce_value = get_adaptor_for_type(ftype)

        if value is None:
            return field == None

        # Handle ranges, either a dictionary value with "start" or "end"
        # keys, or a string value in the form "start-value><end-value"

        if isinstance(value, basestring) and '><' in value:
            start, end = value.split('><')
            value = {'start': start, 'end': end}

        if isinstance(value, Mapping) and ('start' in value or 'end' in value):
            start = coerce_value(value.get('start', None))
            end = coerce_value(value.get('end', None))
            if start is not None and end is not None:
                return field.between(start, end)
            elif start is not None:
                return field >= start
            elif end is not None:
                return field <= end
            else:
                raise UserWarning('Range ends cannot be both None')

        if isinstance(value, basestring):
            if ',' in value:
                return _compare_with_values(field, value, coerce_value)
            elif value == 'NULL':
                return field == None
            elif value == '!NULL' or value == '<>NULL':
                return field != None
            elif value.startswith('~='):
                value = value[2:]
                return field.ilike(value+'%')
            elif value.startswith('~'):
                value = value[1:]
                return field.ilike('%'+value+'%')
            elif value.startswith('>='):
                value = value[2:]
                return field >= coerce_value(value)
            elif value.startswith('>'):
                value = value[1:]
                return field > coerce_value(value)
            elif value.startswith('<='):
                value = value[2:]
                return field <= coerce_value(value)
            elif value.startswith('<>'):
                value = value[2:]
                return field != coerce_value(value)
            elif value.startswith('<'):
                value = value[1:]
                return field < coerce_value(value)
            elif value.startswith('='):
                value = value[1:]
                return field == coerce_value(value)
            elif isinstance(ftype, String):
                return field.ilike('%'+value+'%')
            else:
                return field == coerce_value(value)
        elif isinstance(value, Sequence):
            return _compare_with_values(field, value, coerce_value)
        else:
            return field == coerce_value(value)
    except Exception as e:
        log.error('Error comparing field "%s" with value "%s": %s',
                  field.name, value, e)
        raise


def col_by_name(query, colname):
    "Helper: find the (first) columns with the given name."

    # First look in the selected columns
    for c in query.inner_columns:
        try:
            if c.name == colname:
                return c
        except AttributeError:
            if isinstance(c, BinaryExpression):
                l, r = c._orig
                if (isinstance(l, Column) and l.name == colname
                    or
                    isinstance(r, Column) and r.name == colname):
                    return c
            else:
                log.warning('Unhandled inner column type: %r', type(c).__name__)

    # Then in the froms
    for f in query.froms:
        c = f.columns.get(colname)
        if c is not None:
            return c

        papables = [c for c in f.columns if c.key == colname]
        if len(papables)>=1:
            c = papables[0]
            if len(papables)>1:
                log.warning('Ambiguous column name "%s" for %s:'
                            ' selecting "%s"', colname, str(query), c)
            return c

        papables = [c for c in f.columns if c.name.endswith('_'+colname)]
        if len(papables)>=1:
            c = papables[0]
            if len(papables)>1:
                log.warning('Ambiguous column name "%s" for %s:'
                            ' selecting "%s"', colname, str(query), c)
            return c


def csv2list(csv):
    """Build a list of strings from a CSV or JSON array.

    :param csv: a string containing either a ``CSV`` or a JSON array
    :rtype: a Python list

    This is very simplicistic: since its used to transfer a list of
    field names, that is plain ASCII strings, JSON escapes are not
    even considered.

    `csv` may be either a plain CSV string such as ``first,second,third``
    or a JSON array, such as ``["first","second","third"]``.
    """

    if csv.startswith('[') and csv.endswith(']'):
        res = [v[1:-1] for v in csv[1:-1].split(',')]
    else:
        res = [v.strip() for v in csv.split(',')]
    return res


def extract_raw_conditions(args):
    """Extract raw conditions

    :param args: a dictionary, usually request.params
    :rtype: a list of tuples

    Recognize three possible syntaxes specifying filtering conditions:

    1. the old ExtJS 2 way: ?filter_col=fieldname&filter_value=1
    2. the new ExtJS 4 way where the ``filters`` argument is a JSON
       encoded array of dictionaries, each containing a ``property`` slot
       with the field name as value, an ``operator`` slot and a ``value``
       slot.
    3. a custom syntax: ?filter_fieldname=1

    Build a list of (fieldname, fieldvalue) tuples, where `fieldvalue`
    may be prefixed by the ``operator`` specified with the second
    syntax above.

    Note that the `args` parameter is **modified** in place!
    """

    missing = object()

    conditions = []

    # Old syntax:
    # ?filter_col=fieldname&filter_value=1

    fcol = args.pop('filter_col', missing)
    fvalue = args.pop('filter_value', missing)

    if fcol is not missing and fvalue is not missing:
        conditions.append((fcol, fvalue))

    # ExtJS 4 syntax:
    # filter=[{"property": "fieldname", "operator": "=", "value": "1"},...]

    filters = []

    # Recognize both "filter" and "filters": the former is the standard ExtJS 4
    # `filterParam` setting, the latter is the old name; handling both allows
    # the trick of dinamically augmenting the static conditions written in the URL

    for fpropname in ('filter', 'filters'):
        filter = args.pop(fpropname, missing)
        if filter is not missing:
            if isinstance(filter, basestring):
                filter = json2py(filter)
            filters.extend(filter)

    for f in filters:
        fcol = f.get('property', missing)
        if fcol is missing:
            continue

        fvalue = f.get('value', missing)
        if fvalue is missing:
            continue

        fop = f.get('operator')
        if fop:
            if not isinstance(fvalue, basestring):
                fvalue = str(fvalue)
            if not fvalue.startswith(fop):
                fvalue = fop + fvalue

        conditions.append((fcol, fvalue))

    # Yet another syntax:
    # ?filter_fieldname=1

    # This is needed as we are going to change the dictionary
    fnames = list(args.keys())
    for f in fnames:
        if f.startswith('filter_'):
            fcol = f[7:]
            if not fcol:
                continue
            fvalue = args.pop(f, missing)
            if fvalue is not missing:
                conditions.append((fcol, fvalue))

    return conditions


def apply_filters(query, args):
    """Filter a given query.

    :param query: an SQLAlchemy ``Query``
    :param args: a dictionary
    :rtype: a tuple

    `query` may be either a SQL statement (not necessarily a
    ``SELECT``) or an ORM query.

    The `args` dictionary may contain some special keys, that will
    be used to build a filter expression, or to change the query
    in particular ways. All these keys will be *consumed*, that is
    removed from the `args` dictionary.

    filter_col
      the name of the field going to be filtered

    filter_value
      value of the filter

    filter_name-of-the-field
      specify both the `name-of-the-field` and the value to apply

    filter (or filters)
      a sequence of filter specifications, or a JSON string containing a list of
      dictionaries: each dictionary must contain a ``property`` and a ``value``
      slots and an optional ``operator`` which is prepended to the given value,
      if it already does not when specified

    only_cols
      filter the selected columns of the query, using only fields
      specified with this argument, assumed to be a comma separated
      list of field names

    query
      this is used combined with `fields`: if present, its value will
      be searched in the specified fields, within an ``OR`` expression

    fields
      this is a list of field names that selects which fields will be
      compared to the `query` value. Currently this functionality works
      only on ``String``\s: all fields of a different kind are ignored

    The function `compare_field()` is used to build the filter
    expressions.

    Returns a tuple with the modified query at the first slot, and another
    which is either `None` or the list of columns specified by `only_cols`.
    """

    if isinstance(query, Query):
        stmt = query.statement
    else:
        stmt = query

    rconditions = extract_raw_conditions(args)
    conditions = []

    for fcol, fvalue in rconditions:
        col = col_by_name(stmt, fcol)
        if col is not None:
            cond = compare_field(col, fvalue)
            conditions.append(cond)

    if conditions:
        if len(conditions)>1:
            fexpr = and_(*conditions)
        else:
            fexpr = conditions[0]
        if isinstance(query, Query):
            query = query.filter(fexpr)
        else:
            query = query.where(fexpr)

    qvalue = args.pop('query', None)
    only_cols = args.pop('only_cols', None)
    qfields = args.pop('fields', only_cols)

    if qvalue:
        if qfields is None:
            qfields = [c.name for c in stmt.inner_columns]
        if isinstance(qfields, basestring):
            qfields = csv2list(qfields)
        conds = []
        for fcol in qfields:
            col = col_by_name(stmt, fcol)
            if col is not None:
                ct = col.type
                try:
                    ct = ct.impl
                except AttributeError:
                    pass
                if isinstance(ct, String):
                    conds.append(compare_field(col, qvalue))
        if conds:
            if len(conds)>1:
                cond = or_(*conds)
            else:
                cond = conds[0]
            if isinstance(query, Query):
                query = query.filter(cond)
            else:
                query = query.where(cond)

    if only_cols:
        if isinstance(only_cols, basestring):
            only_cols = csv2list(only_cols)
        if not isinstance(query, Query):
            cols = [col for col in [col_by_name(query, c) for c in only_cols]
                    if col is not None]
            if not cols:
                raise ValueError("No valid column in only_cols='%s'" % only_cols)
            query = query.with_only_columns(cols)

    return query, only_cols


def apply_sorters(query, sort, dir):
    """Order a given query.

    :param query: an SQLAlchemy ``Query``
    :param sort: either a string, the name of the field, or a sequence of a
                 dictionaries (possibly a JSON encoded array), each containing
                 a ``property`` slot and a ``direction`` slot, respectively
                 the field name and the ordering direction
    :param dir: a string, either "ASC" or "DESC", for ascending or descending
                order respectively
    :rtype: an SQLAlchemy ``Query``

    `query` may be either a SQL statement (not necessarily a
    ``SELECT``) or an ORM query.
    """

    if isinstance(sort, basestring):
        if sort.startswith('['):
            sort = json2py(sort)
        else:
            sort = [{'property': field, 'direction': dir}
                    for field in sort.split(',')]

    if isinstance(query, Query):
        stmt = query.statement
    else:
        stmt = query

    for item in sort:
        property = item['property']
        direction = item.get('direction') or 'ASC'

        col = col_by_name(stmt, property)

        if col is not None:
            if direction != 'ASC':
                col = col.desc()
            query = query.order_by(col)
        else:
            log.warning('Requested sort on "%s", which does'
                        ' not exist in %s', property, query)

    return query


def create_change_saver(adaptor=None, save_changes=None,
                        modified_slot_name='modified_records',
                        deleted_slot_name='deleted_records',
                        inserted_ids_slot='inserted_ids',
                        modified_ids_slot='modified_ids',
                        deleted_ids_slot='deleted_ids',
                        result_slot='root',
                        success_slot='success',
                        message_slot='message'):
    """Function factory to implement the standard POST handler for a proxy.

    :param adaptor: a function that adapts the changes before application
    :param save_changes: the function that concretely applies the changes
    :param modified_slot_name: a string, by default 'modified_records'
    :param deleted_slot_name: a string, by default 'deleted_records'
    :param inserted_ids_slot: a string, by default 'inserted_ids'
    :param modified_ids_slot: a string, by default 'modified_ids'
    :param deleted_ids_slot: a string, by default 'deleted_ids'
    :param result_slot: a string, by default 'root'
    :param success_slot: a string, by default 'success'
    :param message_slot: a string, by default 'message'
    :returns: a dictionary, with a boolean `success` slot with a
        ``True`` value if the operation was completed without errors,
        ``False`` otherwise: in the latter case the `message` slot
        contains the reason for the failure. Three other slots carry
        lists of dictionaries with the ids of the *inserted*,
        *modified* and *deleted* records.

    This implements the generic behaviour we need to save changes back to
    the database.

    The `adaptor` function takes four arguments, respectively the SA
    session, the request, a list of added/modified records and a list
    of deleted records; it must return two (possibly modified) lists,
    one containing added/modified records and the other with the
    records to delete, e.g.::

        def adaptor(sa_session, request, modified_recs, deleted_recs):
            # do any step to adapt incoming data
            return modified_recs, deleted_recs
    """

    def workhorse(sa_session, request, **args):
        mr = json2py(args[modified_slot_name])
        dr = json2py(args[deleted_slot_name])

        if adaptor is not None:
            try:
                mr, dr = adaptor(sa_session, request, mr, dr)
            except Exception as e:
                log.critical('Could not adapt changes: %s', e, exc_info=True)
                return {
                    success_slot: False,
                    message_slot: 'Internal error, consult application log'
                }

        try:
            iids, mids, dids = save_changes(sa_session, request, mr, dr)
            status = True
            statusmsg = "Ok"
        except SQLAlchemyError as e:
            msg = get_exception_message(e)
            log.error('Could not save changes to the database: %s', msg)
            status = False
            statusmsg = msg.split('\n')[0]
            iids = mids = dids = None
        except Exception as e:
            msg = get_exception_message(e)
            log.critical('Could not save changes to the database: %s',
                         msg, exc_info=True)
            status = False
            statusmsg = 'Internal error, consult application log.'
            iids = mids = dids = None

        return { success_slot: status,
                 message_slot: statusmsg,
                 inserted_ids_slot: iids,
                 modified_ids_slot: mids,
                 deleted_ids_slot: dids,
               }

    return workhorse
