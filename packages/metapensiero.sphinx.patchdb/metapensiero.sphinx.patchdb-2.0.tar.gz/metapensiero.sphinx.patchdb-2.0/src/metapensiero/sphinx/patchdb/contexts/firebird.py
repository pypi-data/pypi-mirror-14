# -*- coding: utf-8 -*-
# :Project:   PatchDB -- Firebird SQL script execution context
# :Created:   sab 31 mag 2014 13:01:51 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2014, 2016 Lele Gaifax
#

from __future__ import unicode_literals

from . import logger
from .sql import SqlContext


class FirebirdContext(SqlContext):
    def makeConnection(self, dsn, username, password):
        import fdb as dbapi

        self.dsn = dsn
        self.username = username
        self.password = password
        logger.info('Connecting to %s', self.dsn)
        self.connection = dbapi.connect(dsn=self.dsn,
                                        user=self.username,
                                        password=self.password)

        fb_version = tuple([int(x) for x in self.connection.version.split('.')])

        self.assertions.update({
            'firebird': True,
            'firebird_2_x': (2,0) <= fb_version < (3,0),
            'firebird_3_x': (3,0) <= fb_version < (4,0),
            })

    def setupContext(self):
        from ..patch import MAX_PATCHID_LEN

        cursor = self.connection.cursor()
        cursor.execute("SELECT rdb$relation_name"
                       " FROM rdb$relations"
                       " WHERE rdb$relation_name = 'PATCHDB'")
        result = cursor.fetchone()
        if not result:
            logger.info('Creating patchdb table')
            cursor.execute("CREATE TABLE patchdb ("
                           " patchid VARCHAR(%d) NOT NULL PRIMARY KEY,"
                           " revision SMALLINT NOT NULL,"
                           " applied TIMESTAMP NOT NULL"
                           ")" % MAX_PATCHID_LEN)
