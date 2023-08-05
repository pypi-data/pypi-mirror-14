import collections
from importlib import machinery
import logging
import os
import re


__all__ = ['Pijon', 'migrate']
log = logging.getLogger(__name__)


def migrate(data, in_place=False, folder=None):
    p = Pijon(folder)
    return p.migrate(data, in_place=in_place)


class Pijon(object):

    DEFAULT_FOLDER = 'migrations'
    MIGRATION_REGEX = r'(?P<ident>\d{4})_(?P<name>\w+)\.py'

    def __init__(self, folder=None):
        self.folder = folder or self.DEFAULT_FOLDER
        self.migrations = self.fetch_migrations()

    @property
    def last_migration(self):
        """
        Returns last migration identity number
        """
        return int(next(reversed(self.migrations))) if self.migrations else 0

    def fetch_migrations(self):
        """
        Return the `migrations` list
        """
        migrations = collections.OrderedDict()

        try:
            listdir = sorted(os.listdir(self.folder))
        except FileNotFoundError:
            os.mkdir(self.folder)
            log.info('Created migration folder at %s', self.folder)
            return migrations

        for filename in listdir:
            match = re.match(self.MIGRATION_REGEX, filename)
            if not match:
                log.debug('pass: %s', filename)
                continue

            # Match migration filename pattern
            ident = match.group('ident')
            name = match.group('name')

            # Load module
            module = machinery.SourceFileLoader(
                name, os.path.join(self.folder, filename)
            ).load_module(name)

            migrations[ident] = module
            log.debug("Loaded module '%s'", module)

        return migrations

    def _run_migrations(self, data, target=None):
        """
        Run migrations on `data` until `target` version is reached
        """
        initial_version = data.get('version', 0)
        for ident, module in self.migrations.items():
            migration_version = int(ident)

            # Skip if migration is past
            if migration_version <= initial_version:
                continue

            # Stop if target is reached
            if target and data.get('version', 0) >= target:
                break

            log.info("Applying migration %s '%s'", ident, module.__name__)
            module.migrate(data)
            data['version'] = migration_version

        return data

    def migrate(self, data, in_place=False, target=None):
        return self._run_migrations(data if in_place else data.copy(), target)
