# -*- coding: utf-8 -*-
# :Project:   PatchDB -- MySQL script execution context
# :Created:   lun 02 giu 2014 09:21:14 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2014, 2016 Lele Gaifax
#

from __future__ import unicode_literals

from . import logger
from .sql import SqlContext, FakeDataDomainsMixin


class MySQLContext(FakeDataDomainsMixin, SqlContext):
    def __init__(self, **args):
        SqlContext.__init__(self, **args)

        self._domains = {}
        "A dictionary containing defined domains."

    def makeConnection(self, host, port, db, username, password, charset, driver):
        import importlib
        import re

        self.dbapi = importlib.import_module(driver)
        self.host = host
        self.port = port
        self.db = db
        self.username = username
        self.password = password
        self.charset = charset
        logger.info('Connecting to %s/%s', self.host, self.db)
        self.connection = self.dbapi.connect(host=self.host,
                                             port=self.port,
                                             user=self.username,
                                             passwd=self.password,
                                             db=self.db,
                                             charset=self.charset,
                                             use_unicode=True)
        cursor = self.connection.cursor()
        cursor.execute("SELECT version()")
        v = cursor.fetchone()
        m = re.match('(\d+)\.(\d+)\.(\d+)', v[0])
        assert m, "Could not determine mysql version"
        version = tuple([int(x) for x in m.group(1, 2)])

        self.assertions.update({
            'mysql': True,
            'mysql_6_x': (6,0) <= version < (7,0),
            'mysql_5_x': (5,0) <= version < (6,0),
            'mysql_4_x': (4,0) <= version < (5,0),
            })

    def setupContext(self):
        from ..patch import MAX_PATCHID_LEN

        cursor = self.connection.cursor()
        try:
            cursor.execute("DESCRIBE patchdb")
        except self.dbapi.err.ProgrammingError:
            logger.info('Creating patchdb table')
            cursor.execute("CREATE TABLE patchdb ("
                           " patchid VARCHAR(%d) CHARACTER SET utf8mb4 NOT NULL PRIMARY KEY,"
                           " revision SMALLINT NOT NULL,"
                           " applied DATETIME NOT NULL"
                           ")" % MAX_PATCHID_LEN)

    def classifyError(self, exc):
        if hasattr(exc, 'errmsg'):
            msg = exc.errmsg
            code = exc.errno
        else:
            code, msg = exc.args
        if hasattr(msg, 'decode'):
            try:
                msg = msg.decode('utf-8')
            except UnicodeDecodeError:
                msg = msg.decode('latin1', 'ignore')
        msg = '[%d] %s' % (code, msg)
        # See http://dev.mysql.com/doc/refman/5.5/en/error-messages-server.html
        syntaxerror = code in (1064, 1149)
        nonexistingobj = code in (1051, 1091, 1146)
        return msg, syntaxerror, nonexistingobj
