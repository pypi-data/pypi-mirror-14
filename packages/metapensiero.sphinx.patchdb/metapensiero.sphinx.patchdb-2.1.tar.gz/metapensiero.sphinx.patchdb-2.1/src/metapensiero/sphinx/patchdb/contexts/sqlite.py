# -*- coding: utf-8 -*-
# :Project:   PatchDB -- SQLite specialized context
# :Created:   lun 22 feb 2016 11:02:21 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from __future__ import unicode_literals

from . import logger
from .sql import SqlContext, FakeDataDomainsMixin


class SQLiteContext(FakeDataDomainsMixin, SqlContext):
    # SQLite uses qmarks as param style
    GET_PATCH_REVISION_STMT = ("SELECT revision"
                               " FROM patchdb"
                               " WHERE patchid = ?")
    INSERT_PATCH_STMT = ("INSERT INTO patchdb (patchid, revision, applied)"
                         " VALUES (?, ?, CURRENT_TIMESTAMP)")
    UPDATE_PATCH_STMT = ("UPDATE patchdb"
                         " SET revision = ?, applied = CURRENT_TIMESTAMP"
                         " WHERE patchid = ?")

    def makeConnection(self, database):
        from sqlite3 import connect, sqlite_version_info

        self.database = database
        logger.info('Connecting to %s', self.database)
        self.connection = connect(database)
        # See http://bugs.python.org/issue10740
        self.connection.isolation_level = None

        self.assertions.update({
            'sqlite': True,
            'sqlite3': sqlite_version_info[0] == 3,
            })

    def setupContext(self):
        from ..patch import MAX_PATCHID_LEN

        cursor = self.connection.cursor()
        cursor.execute("PRAGMA table_info('patchdb')")
        result = cursor.fetchone()
        if not result:
            logger.info('Creating patchdb table')
            cursor.execute("CREATE TABLE patchdb ("
                           " patchid VARCHAR(%d) NOT NULL PRIMARY KEY,"
                           " revision SMALLINT NOT NULL,"
                           " applied DATETIME NOT NULL"
                           ")" % MAX_PATCHID_LEN)
            self.connection.commit()

    def savePoint(self, point):
        cursor = self.connection.cursor()
        cursor.execute("savepoint point_%s" % point)

    def rollbackPoint(self, point):
        cursor = self.connection.cursor()
        cursor.execute("rollback to savepoint point_%s" % point)

    def classifyError(self, exc):
        msg = str(exc)
        syntaxerror = msg.endswith('syntax error')
        nonexistingobj = msg.startswith('no such')
        return msg, syntaxerror, nonexistingobj
