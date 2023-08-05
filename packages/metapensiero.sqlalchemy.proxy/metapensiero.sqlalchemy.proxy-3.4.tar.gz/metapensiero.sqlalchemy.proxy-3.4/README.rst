.. -*- coding: utf-8 -*-
.. :Project:   metapensiero.sqlalchemy.proxy
.. :Created:   gio 30 apr 2009 10:01:20 CEST
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2009, 2010, 2012, 2013, 2014, 2016 Lele Gaifax
..

===============================
 metapensiero.sqlalchemy.proxy
===============================

Expose SQLAlchemy's queries and their metadata to a webservice
==============================================================

This package contains a few utilities to make it easier applying some filtering to a stock
query and obtaining the resultset in various formats.

An helper decorator explicitly designed for Pylons is included: it provides a `property` like
syntax to attach either a ProxiedQuery or a plain Python function to a Controller, handling
``GET``, ``POST`` or ``DEL`` request methods.

Since version 1.7 there are some Pyramid specific subclasses that help using the proxies within
a Pyramid view as well as a `expose` decorator that simplify their implementation.


Usage with Pyramid
------------------

First of all, there are some setup steps to follow:

1. Include the package in the configuration file::

    [app:main]
    use = egg:ph.data

    ...

    pyramid.includes =
        metapensiero.sqlalchemy.proxy.pyramid
        pyramid_tm

   This is not strictly needed, but it will override the standard ``json`` renderer with one
   that uses ``nssjson``, to handle the datetime type.

2. Configure the ``expose`` decorator, for example adding something like the following snippet
   to the ``.../views.py`` source::

    from metapensiero.sqlalchemy.proxy.pyramid import expose
    from .models import DBSession

    # Configure the `expose` decorator
    expose.create_session = staticmethod(lambda req: DBSession())

Then you can add views to expose either an entity or a plain select::

    @view_config(route_name='users', renderer='json')
    @expose(User, metadata=dict(
        password=dict(hidden=True, password=True, width=40),
        is_anonymous=False,
        ))
    def users(request, results):
        return results

    sessions_t = Session.__table__

    @view_config(route_name='sessions', renderer='json')
    @expose(select([sessions_t], sessions_t.c.iduser == bindparam('user_id')))
    def sessions(request, results):
        return results

The decorated function may be a generator instead, which has the opportunity of freely
manipulate either the arguments received from the request, or the final result, or both as
follows::

    @view_config(route_name='users', renderer='json')
    @expose(User, metadata=dict(
        password=dict(hidden=True, password=True, width=40),
        is_anonymous=False,
        ))
    def complex():
        # Receive request and arguments
        request, args = (yield)

        # Adjust parameters
        args['new'] = True

        # Note that bindparams by default are extracted from the “params”
        # keyword argument
        bindparams = args.setdefault('params', {})
        bindparams['user_id'] = 2

        if 'something' in params:
            # Inject other conditions
            something = args.pop('something')
            conditions = (User.c.foo == something,)
            result = yield args, conditions
        else:
            # Go on, and receive the final result
            result = yield args

        # Fix it up
        result['COMPLEX'] = 'MAYBE'

        yield result


Examples
~~~~~~~~

Assuming the ``users`` view is added as ``/views/users``, it could be called in the following
ways:

``GET /views/users``
  would return a JSON response containing **all** users, like::

    {
      "count": 1234,
      "message": "Ok",
      "success": true,
      "root": [
        {
          "first_name": "Lele",
          "last_name": "Gaifax",
          ...
        },
        {
          "first_name": "Mario",
          "last_name": "Rossi",
          ...
        },
        ...
      ]
    }

``GET /views/users?limit=1&start=2``
  would return a JSON response containing just **one** user, the second::

    {
      "count": 1234,
      "message": "Ok",
      "success": true,
      "root": [
        {
          "first_name": "Mario",
          "last_name": "Rossi",
          ...
        }
      ]
    }

``GET /views/users?filter_first_name=Lele``
  would return a JSON response containing the records satisfying the given condition::

    {
      "count": 1,
      "message": "Ok",
      "success": true,
      "root": [
        {
          "first_name": "Lele",
          "last_name": "Gaifax",
          ...
        }
      ]
    }

``GET /views/users?limit=1&only_cols=first_name,role_name``
  would return a JSON response containing only the requested fields of a single record::

    {
      "count": 1234,
      "message": "Ok",
      "success": true,
      "root": [
        {
          "first_name": "Lele",
          "role_name": "administrator"
        }
      ]
    }

``GET /views/users?metadata=metadata&limit=0``
  would return a JSON response containing a description of the schema::

    {
      "metadata": {
        "success_slot": "success",
        "primary_key": "iduser",
        "fields": [
          {
            "width": 60,
            "hint": "The unique ID of the user.",
            "align": "right",
            "nullable": false,
            "readonly": true,
            "type": "int",
            "hidden": true,
            "label": "User ID",
            "name": "iduser"
          },
          ...
        ],
        "root_slot": "root",
        "count_slot": "count"
      },
      "message": "Ok",
      "success": true
    }

Browse SoL__ sources for real usage examples.


__ https://bitbucket.org/lele/sol/src/master/src/sol/views/data.py
