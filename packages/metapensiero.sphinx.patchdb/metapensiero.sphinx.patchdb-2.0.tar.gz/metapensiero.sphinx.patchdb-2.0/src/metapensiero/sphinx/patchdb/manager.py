# -*- coding: utf-8 -*-
# :Project:   PatchDB -- Script&Patch Manager
# :Created:   ven 14 ago 2009 13:09:28 CEST
# :Author:    Lele Gaifax <lele@nautilus.homeip.net>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2009, 2010, 2012, 2013, 2014, 2015, 2016 Lele Gaifax
#

from __future__ import absolute_import, unicode_literals

from io import open
import logging
import sys

try:
    from sqlalchemy.util.topological import sort
except ImportError:
    # SQLAlchemy < 0.7
    from sqlalchemy.topological import sort

from .patch import DependencyError


logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)


class PatchManager(object):
    """
    An instance of this class collects a set of patches and acts as
    a dictionary. It's able to serialize the patches taking into
    account the dependencies.
    """

    def __init__(self):
        self.db = {}

    def __getitem__(self, patchid):
        """
        Return the patch given its `patchid`, or ``None`` if it does not exist.
        """
        return self.db.get(patchid)

    def __setitem__(self, patchid, patch):
        """
        Register the given `patch` identified by `patchid`.
        """
        self.db[patchid] = patch

    def neededPatches(self, context):
        """
        Return an iterator over *not yet applied* patches, in the
        right order to satisfy their inter-dependencies.
        """

        # SA topological sort relies on objects id()
        uniquified = {}
        def uniquify(t):
            return uniquified.setdefault(t, t)

        skippedcnt = 0
        constraints = set()
        missing = []
        always_first = []
        always_last = []

        logger.debug("Collecting and ordering patches...")
        for pid, patch in self.db.items():
            if not patch.always and patch.revision == context[pid]:
                logger.debug("Skipping %s, already applied", patch)
                continue

            patch.adjustUnspecifiedRevisions(self)

            if patch.verifyConditions(context.for_language(patch.language)):
                skip = False
                if patch.brings:
                    for depid, deprev in patch.depends:
                        current = context[depid]
                        if current is not None and current > deprev:
                            logger.debug("Ignoring %s because it depends on"
                                         " '%s@%d', currently at version %s",
                                         patch, depid, deprev, current)
                            skip = True
                            break
                if skip:
                    skippedcnt += 1
                    continue

                this = uniquify((patch.patchid, patch.revision))
                if patch.always:
                    if patch.always == 'first':
                        always_first.append(this)
                    else:
                        always_last.append(this)
                else:
                    missing.append(this)

                for dep in patch.depends:
                    constraints.add( (uniquify(dep), this) )
                for preceed in patch.preceeds:
                    constraints.add( (this, uniquify(preceed)) )
                for bring in patch.brings:
                    constraints.add( (this, uniquify(bring)) )
            else:
                logger.debug("Ignoring %s, because it does not satisfy the"
                             " conditions", patch)

        if always_first:
            logger.info("Applying execute-always-first patches...")
            for pid, rev in sort(constraints, always_first):
                yield self[pid]

        logger.info("Applying missing patches...")
        for pid, rev in sort(constraints, missing):
            if (pid, rev) in missing:
                currrev = context[pid]
                patch = self[pid]

                if currrev is None and not patch.script:
                    # This is a "placeholder" patch and it has not been applied yet
                    logger.critical("Placeholder %s has not been applied yet", patch)
                    raise DependencyError('%s is a placeholder implemented elsewhere'
                                          ' and not yet applied' % patch)

                if currrev is None or currrev < rev:
                    ignore = False
                    if patch.brings:
                        for depid,deprev in patch.depends:
                            currdeprev = context[depid]
                            if currdeprev is None or currdeprev != deprev:
                                logger.debug("Ignoring %s, because it depends"
                                             " on '%s@%d' which is currently"
                                             " at revision %s",
                                             patch, depid, deprev, currdeprev)
                                ignore = True
                    if not ignore:
                        yield patch
                else:
                    logger.debug("Skipping %s, already applied", patch)
            else:
                logger.debug("Skipping '%s@%d', introduced by dependencies",
                             pid, rev)

        if always_last:
            logger.info("Applying execute-always-last patches...")
            for pid, rev in sort(constraints, always_last):
                yield self[pid]


class PersistentPatchManager(PatchManager):
    """
    Patch manager that uses a Pickle/YAML/JSON/AXON file as its persistent storage.
    """

    def __init__(self, storage_path=None):
        super(PersistentPatchManager, self).__init__()
        self.storage_path = storage_path

    def save(self):
        if self.storage_path is None:
            return

        logger.debug("Writing patches to %s", self.storage_path)
        spendswith = self.storage_path.endswith
        if spendswith('.yaml') or spendswith('.json') or spendswith('.axon'):
            storage = open(self.storage_path, 'w', encoding='utf-8')

            # Order patches by id, both for easier lookup and to
            # avoid VCs stress

            asdicts = [self.db[sid].asdict for sid in sorted(self.db)]

            # Optimize for size and readability: store simple
            # dictionaries, with UTF-8 encoded strings; rename
            # "patchid" to "ID", as the latter will be the first key
            # in the YAML dictionary (entries are usually sorted
            # alphabetically).

            if spendswith('.yaml'):
                from yaml import dump_all
                content = dump_all(asdicts, default_flow_style=False, encoding=None)
            elif spendswith('.json'):
                from json import dumps
                content = dumps(asdicts, sort_keys=True, indent=1)
                if sys.version_info.major < 3 and not isinstance(content, unicode):
                    content = content.decode('utf-8')
            else:
                from axon import dumps
                content = dumps(asdicts, pretty=1)

            with open(self.storage_path, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            from pickle import dump

            storage = open(self.storage_path, 'wb')
            dump(self.db, storage)
        storage.close()
        logger.debug("Done writing patches")

    def load(self):
        py2 = sys.version_info.major < 3
        logger.debug("Reading patches from %s", self.storage_path)
        spendswith = self.storage_path.endswith
        if spendswith('.yaml') or spendswith('.json') or spendswith('.axon'):
            from .patch import make_patch

            with open(self.storage_path, 'r', encoding='utf-8') as storage:
                if spendswith('.yaml'):
                    from yaml import load_all
                    asdicts = load_all(storage.read())
                elif spendswith('.json'):
                    from json import loads
                    asdicts = loads(storage.read())
                else:
                    from axon import loads
                    asdicts = loads(storage.read())

            db = self.db = {}
            for d in asdicts:
                if py2:
                    for i in d:
                        if isinstance(d[i], str):
                            d[i] = d[i].decode('utf-8')
                db[d['ID']] = make_patch(d['ID'], d['script'], d)
        else:
            from pickle import load

            with open(self.storage_path, 'rb') as storage:
                self.db = load(storage)

        storage.close()
        logger.debug("Done reading patches")


__manager = None

def patch_manager(storage_path, overwrite=False, autosave=False):
    global __manager

    if not __manager:
        __manager = PersistentPatchManager(storage_path)
        if storage_path is not None: # used by doctests
            if not overwrite:
                __manager.load()
            if autosave:
                import atexit
                atexit.register(__manager.save)
    return __manager
