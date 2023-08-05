# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- nssjson glue
# :Created:   gio 04 dic 2008 13:56:51 CET
# :Author:    Lele Gaifax <lele@nautilus.homeip.net>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2008, 2009, 2010, 2012, 2013, 2014, 2016 Lele Gaifax
#

import decimal
from nssjson import JSONDecoder, JSONEncoder


JSONDateFormat = 'Y-m-d'
JSONTimeFormat = 'H:i:s'
JSONTimestampFormat = 'Y-m-d\\TH:i:s'


py2json = JSONEncoder(separators=(',', ':'),
                      handle_uuid=True,
                      use_decimal=True,
                      iso_datetime=True).encode

json2py = JSONDecoder(handle_uuid=True,
                      parse_float=decimal.Decimal,
                      iso_datetime=True).decode
