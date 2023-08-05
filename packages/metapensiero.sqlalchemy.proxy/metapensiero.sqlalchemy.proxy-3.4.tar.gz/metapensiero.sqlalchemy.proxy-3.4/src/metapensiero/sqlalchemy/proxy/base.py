# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Abstract base class
# :Created:   mer 03 feb 2016 11:03:22 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from __future__ import absolute_import, unicode_literals

from collections import Callable, Mapping
import logging

from sqlalchemy import (Boolean, Column, Date, DateTime, Integer, Interval, Numeric, String,
                        Text, Time)
from sqlalchemy.exc import SQLAlchemyError

from .utils import apply_sorters


log = logging.getLogger(__name__)


try:
    basestring
except NameError: # pragma: nocover
    # Py3 compatibility
    basestring = str


class MetaInfo(Mapping):
    "Helper class, a dictionary where values can be callables"

    def __init__(self, name, info):
        self.name = name
        if isinstance(info, Callable):
            info = info(name)
        self.info = info

    def __getitem__(self, key):
        item = self.info.get(key)
        if isinstance(item, Callable):
            item = item(self.name, key)
        return item

    def __contains__(self, key):
        return key in self.info

    def __iter__(self):
        return iter(self.info)

    def __len__(self):
        return len(self.info)


class ProxiedBase(object):
    """Abstract base for the proxy thingie"""

    def translate(self, msg):
        "Stub implementation of i18n basic functions, to be overridden."

        return msg

    def prepareQueryFromConditionsAndArgs(self, session, conditions, args):
        "Extract special meaning keyword arguments and return them, with a filtered query."

        start = args.pop('start', None)
        if start is not None:
            start = int(start)
        limit = args.pop('limit', None)
        if limit is not None:
            limit = int(limit)

        resultslot = args.pop('result', True)
        if resultslot in ('False', 'None', 'false', ''):
            resultslot = False
        elif resultslot in ('True', 'true'):
            resultslot = True

        slot = args.pop('success', 'success')
        if slot in (False, 'False', 'None', 'false', ''):
            successslot = False
        else:
            if slot in (True, 'True', 'true'):
                slot = 'success'
            successslot = resultslot is not True and slot

        slot = args.pop('message', 'message')
        if slot in (False, 'False', 'None', 'false', ''):
            messageslot = False
        else:
            if slot in (True, 'True', 'true'):
                slot = 'message'
            messageslot = resultslot is not True and slot

        slot = args.pop('count', None)
        if slot in (False, 'False', 'None', 'false', ''):
            countslot = False
        else:
            if slot in (True, 'True', 'true'):
                slot = 'count'
            countslot = resultslot is not True and slot

        slot = args.pop('metadata', None)
        if slot in (False, 'False', 'None', 'false', ''):
            metadataslot = False
        else:
            if slot in (True, 'True', 'true'):
                slot = 'metadata'
            metadataslot = resultslot is not True and slot

        asdict = args.pop('asdict', False)
        if asdict in ('False', 'None', 'false', ''):
            asdict = False

        sort = args.pop('sort', None)
        dir = args.pop('dir', 'ASC')

        result = {}
        if successslot:
            result[successslot] = False

        try:
            query = self.filterQueryWithArgs(session, conditions, args)
        except: # pragma: nocover
            log.exception("Unhandled exception applying filters"
                          " %r and args %r", conditions, args)
            raise

        return (query, result, asdict,
                resultslot, successslot, messageslot, countslot, metadataslot,
                sort, dir,
                start, limit)

    def __call__(self, session, *conditions, **args):
        """Apply filter conditions, execute the query and return results.

        :param session: an SQLAlchemy ``Session``
        :param conditions: a list of SQLAlchemy expressions
        :param args: a dictionary
        :rtype: depending on the arguments, either a dictionary, a list of
                tuples or a JSON string

        The first argument is the SQLAlchemy `session`, mandatory. All
        remaining arguments are eventually used to filter and change
        the query. Unused arguments remains accessible when the query
        is finally called.

        Some keyword arguments have special meaning:

        start
          This is the start of the interested range of records

        limit
          This is the maximum number of returned records

        result
          When ``False`` or ``None`` (or the strings ``"False"``,
          ``"None"`` and ``"false"``) means that no result set will be
          returned (reasonably either `metadata` or `count` are
          given); when ``True`` (or the strings ``"True"`` and
          ``"true"``), most of the other options are ignored and
          **only** the native Python results is returned; otherwise
          it's a string, the name of the *slot* of the returned
          dictionary containing the results set.

          ``True`` by default.

        success
          If `result` is not ``True``, this is a string used as the name
          of the slot containing execution status, that will be a boolean
          flag, ``True`` to indicate successfull execution, ``False``
          otherwise.

          By default it's ``"success"``.

        message
          If `result` is not ``True``, this is a string used as the name
          of the slot containing execution message, that will either ``"Ok"``
          when everything went good, otherwise a string with a possible reason
          of the failure.

          By default it's ``"message"``.

        count
          If `result` is not ``True``, this may be a string used as the
          name of the slot containing the total number of records that
          satisfy the conditions, ignoring the eventual range
          specified with `start` and `limit`. When ``False`` or ``None``
          (the default) the count won't be computed.

        metadata
          If `result` is not ``True``, this may be the name of the slot
          containing a description of the result, in a format
          compatible with ExtJS `Store`.

          ``None``, the default, disables the feature.

        asdict
          When you want to deal with plain Python dictionaries, one
          for each row, instead of the standard SQLAlchemy
          `resultset`, set this to ``True``. ``False`` by default.

        sort
          If specified, the name of the field to sort the result by. It may be a
          sequence of dictionaries, to specify an ordering based on multiple
          columns.

        dir
          When `sort` is specified, the direction to sort with. It
          defaults to "ASC", any different value will sort in
          DESCending order.

        All these keywords are pulled (that is, removed) from the
        execution *context* of the query, as well as those used by
        `apply_filters()` function.
        """

        (query, result, asdict,
         resultslot, successslot, messageslot, countslot, metadataslot,
         sort, dir,
         start, limit) = self.prepareQueryFromConditionsAndArgs(session, conditions, args)

        try:
            if limit != 0:
                if countslot:
                    result[countslot] = self.getCount(session, query)

                if resultslot:
                    if sort:
                        query = apply_sorters(query, sort, dir)
                    if start:
                        query = query.offset(start)
                    if limit:
                        query = query.limit(limit)
                    result[resultslot] = self.getResult(session, query, asdict)

            if metadataslot:
                result[metadataslot] = self.getMetadata(session, query,
                                                        countslot,
                                                        resultslot,
                                                        successslot)

            if successslot:
                result[successslot] = True

            if messageslot:
                result[messageslot] = 'Ok'
        except SQLAlchemyError as e: # pragma: nocover
            log.error("Error executing %s: %s", query, e)
            raise
        except: # pragma: nocover
            log.exception("Unhandled exception executing %s", query)
            raise

        if resultslot is True:
            return result[resultslot]
        else:
            return result

    def filterQueryWithArgs(self, session, conditions, args):
        """Apply filter conditions to the query.

        Should return a `query`, either a SQL statement or an ORM query.
        """

        raise NotImplemented('%s should reimplement this method',
                             self.__class__) # pragma: nocover

    def getColumns(self, query):
        """Return the columns of the given `query`."""

        raise NotImplemented('%s should reimplement this method',
                             self.__class__) # pragma: nocover

    def getCount(self, session, query):
        """Execute a query to get the actual count of matching records."""

        raise NotImplemented('%s should reimplement this method',
                             self.__class__) # pragma: nocover

    def getMetadata(self, session, query, countslot, resultslot, successslot):
        """Description of the result, used to configure an ExtJS store.

        :param session: an SQLAlchemy ``Session``
        :param query: an SQLAlchemy ``Query``
        :param countslot: a string or `None`
        :param resultslot: a string or `None`
        :param successslot: a string or `None`
        :rtype: a dictionary

        For each selected field in the query, this method builds a
        dictionary containing the following keys:

        name
          the name of the field

        type
          the type of the field

        format
          the format of the field, for `date` and `datetime` values

        label
          the localized header for the field

        hint
          a longer description of the field, also localized

        width
          the width of the grid column

        These dictionaries are collected in a list, called ``fields``.

        The information about each field is extracted by two sources:

        1. `self.metadata`, a dictionary keyed on field names: each
           slot may be either a dictionary or a callable accepting the
           field name as parameter and returning the actual dictionary

        2. field column `info`, either a dictionary or a callable
           accepting the field name as parameter and returning the
           actual dictionary

        Also the value of any single slot in the information
        dictionary may be either a scalar value or a callable
        accepting two parameters, the name of the field and the name
        of the slot, returning the actual scalar information, for
        example::

          def birthdate_info(name):
              return {
                  'min': date(1980, 1, 1),
                  'max': lambda fname, iname: date.today()
              }

          persons = Table('persons', metadata,
                          Column('id', Integer, primary_key=True),
                          Column('firstname', String),
                          Column('lastname', String),
                          Column('birthdate', Date, info=birthdate_info),
                         )

        The value coming from proxy `metadata` takes precedence over
        the one from the column `info`.

        Both dictionaries can contain any arbitrary extra slots that
        the caller may use for whatever reason.

        To fulfill ``ExtJS.data.JsonReader`` needs, the resulting
        dictionary contains also the name of the slots used to return
        the *status*, the *result* itself and the total *count* of
        items.

        With the exception of `name`, everything can be overridden
        by `self.metadata`.
        """

        from .json import JSONDateFormat, JSONTimeFormat, JSONTimestampFormat

        fields = []

        satypes_metadata = {
            basestring: dict(type='string'),
            Boolean: dict(type='boolean', width=50),
            Date: dict(type='date', width=85, format=JSONDateFormat),
            DateTime: dict(type='date', width=125, timestamp=True, format=JSONTimestampFormat),
            Integer: dict(type='int', width=60, align='right'),
            Interval: dict(type='string', width=85, align='right', timedelta=True),
            Numeric: dict(type='float', width=70, align='right'),
            String: dict(type='string'),
            Time: dict(type='date', width=65, align='right', time=True, format=JSONTimeFormat),
            }

        t = self.translate

        for c in self.getColumns(query):
            meta = dict()
            cinfo = None
            if isinstance(c, basestring):
                name = c
                ctype = basestring
            else:
                name = c.name
                ctype = c.type
                try:
                    ctype = ctype.impl
                except AttributeError:
                    pass
                cinfo = getattr(c, 'info', None)
                if cinfo:
                    cinfo = MetaInfo(name, cinfo)
                elif isinstance(c, Column):
                    # Maybe it's been aliased?
                    origt = getattr(c.table, 'original', None)
                    if origt is not None:
                        origc = origt.c[c.key]
                        cinfo = getattr(origc, 'info', None)
                        if cinfo:
                            cinfo = MetaInfo(name, cinfo)
                else:
                    # Or a labelled column?
                    base_cols = getattr(c, 'base_columns', None)
                    if base_cols is not None:
                        for bc in base_cols:
                            cinfo = getattr(bc, 'info', None)
                            if cinfo:
                                cinfo = MetaInfo(name, cinfo)
                                break

            fmeta = self.metadata and self.metadata.get(name)

            # An explicit ``False`` means skip the field completely
            if fmeta is False:
                continue

            if fmeta is not None:
                fmeta = MetaInfo(name, fmeta)

            # Explicit order!
            for klass in (String, basestring, Boolean, Numeric, Integer,
                          DateTime, Date, Time, Interval):
                if isinstance(ctype, klass):
                    meta.update(satypes_metadata[klass])
                    break
            else:
                # Fallback to string type, for filtering and alignment purposes
                meta['type'] = 'string'

            if isinstance(ctype, Numeric):
                try:
                    meta['decimals'] = ctype.scale
                except AttributeError:
                    pass

            if isinstance(ctype, Text):
                meta['width'] = 50
            elif isinstance(ctype, String):
                flen = ctype.length
                if flen is None or flen==1:
                    # Flags or SQL expressions like "field || 'suffix'"
                    flen = 10
                meta['width'] = flen*5
                meta['length'] = flen

            if getattr(c, 'primary_key', False) or getattr(c, 'foreign_keys', False):
                meta['hidden'] = True
                meta['readonly'] = True

            meta['nullable'] = getattr(c, 'nullable', False)

            label = fmeta and fmeta.get('label')
            if not label:
                label = cinfo and cinfo.get('label')
            if not label:
                label = name.capitalize()
            else:
                label = t(label)

            hint = fmeta and fmeta.get('hint')
            if not hint:
                hint = cinfo and cinfo.get('hint')
            if not hint:
                hint = ''
            else:
                hint = t(hint)

            # Take info at SA table definition as defaults
            if cinfo is not None:
                meta.update(cinfo)

            # Possibly overridable by metadata
            if fmeta is not None:
                meta.update(fmeta)

            # Override localized strings
            meta['label'] = label
            meta['hint'] = hint
            if 'dictionary' in meta:
                if isinstance(meta['dictionary'], Mapping):
                    meta['dictionary'] = {
                        k: t(v) for k, v in meta['dictionary'].items()}
                else:
                    meta['dictionary'] = [
                        [k, t(v)] for k, v in meta['dictionary']]
            # Do this last, so it cannot be overridden
            meta['name'] = name

            fields.append(meta)

        result = dict(fields=fields)
        if countslot:
            result['count_slot'] = countslot
        if resultslot:
            result['root_slot'] = resultslot
        if successslot:
            result['success_slot'] = successslot

        return result

    def getResult(self, session, query, asdict):
        """Execute the query in the given session, returning the result.

        :param session: an SQLAlchemy ``Session``
        :param query: an SQLAlchemy ``Query``
        :param asdict: a boolean

        If `asdict` is False then this should return either a
        ``ResultSet`` (for SQL selects) or a list of entities (when
        the query is at the ORM level), otherwise they should be
        translated into a list of dictionaries.
        """

        raise NotImplemented('%s should reimplement this method',
                             self.__class__) # pragma: nocover
