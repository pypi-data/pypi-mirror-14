import collections
from importlib import machinery
import logging
import os
import re


__all__ = ['Pijon', 'migrate', 'list', 'last']
log = logging.getLogger(__name__)


def migrate(data, in_place=False, folder=None):
    p = Pijon(folder)
    return p.migrate(data, in_place=in_place)


def list(folder=None):
    p = Pijon(folder, load=False)
    return p.migrations


def last(folder=None):
    p = Pijon(folder, load=False)
    return p.last_migration


Migration = collections.namedtuple(
    'Migration',
    ['ident', 'name', 'filename', 'module']
)


class Pijon(object):

    DEFAULT_FOLDER = 'migrations'
    MIGRATION_REGEX = r'(?P<ident>\d{4})_(?P<name>\w+)\.py'

    def __init__(self, folder=None, load=True):
        self.folder = folder or self.DEFAULT_FOLDER
        self.migrations = self.fetch(load)

    @property
    def last_migration(self):
        """
        Returns last migration identity number.
        """
        return int(next(reversed(self.migrations))) if self.migrations else 0

    def fetch(self, load=True):
        """
        Fetch and load the migrations list (as Python modules).
        """
        migrations = collections.OrderedDict()

        try:
            listdir = sorted(os.listdir(self.folder))
        except FileNotFoundError:
            os.mkdir(self.folder)
            log.info("Created migration folder at {}".format(self.folder))
            return migrations

        for filename in listdir:
            match = re.match(self.MIGRATION_REGEX, filename)
            if not match:
                continue

            # Match migration filename pattern
            ident = match.group('ident')
            name = match.group('name')

            # Auto-load the module for further use
            module = self._load(name, self.folder, filename) if load else None

            migrations[ident] = Migration(ident, name, filename, module)
            log.debug("Fetching migration {} ({})".format(ident, name))

        return migrations

    @staticmethod
    def _load(name, folder, filename):
        return machinery.SourceFileLoader(
            name, os.path.join(folder, filename)
        ).load_module(name)

    def _run(self, data, target=None):
        """
        Run migrations on `data` until `target` version is reached.
        """
        initial_version = data.get('version', 0)
        for ident, migration in self.migrations.items():
            version = int(ident)

            # Skip if migration is past
            if version <= initial_version:
                log.debug("Ignoring migration {}".format(ident))
                continue

            # Stop if target is reached
            if target and data.get('version', 0) >= target:
                log.info("Migration target ({}) is reached".format(target))
                break

            module = migration.module or self._load(
                migration.name, self.folder, migration.filename
            )
            log.info("Applying migration {}".format(ident))
            module.migrate(data)
            data['version'] = version

        return data

    def migrate(self, data, in_place=False, target=None):
        return self._run(data if in_place else data.copy(), target)
