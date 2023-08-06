import datetime
from StringIO import StringIO
import dateutil.parser
import pytz
from vtr_storages.storages import AbstractStorage


class Storage(AbstractStorage):
    """KVDB Interface like in zato

    kvdb.conn.blabla
    """

    def __init__(self, kvdb, location='kvdb_storage'):
        self.kvdb = kvdb
        self.prefix = location
        self._metadata_name = '__metadata__'
        self._datetime_name = '__datetime__'
        self._created_name = '__created__'
        self._modified_name = '__modified__'
        self._accessed_name = '__accessed__'

    def delete(self, *names):
        paths = self.path(*names)
        if isinstance(paths, basestring):
            paths = [paths]
        self._delete_paths(*paths)

    def _delete_paths(self, *paths):
        paths = list(paths)

        for path in paths[:]:
            paths.append(self.get_datetime_modified_path(path))
            paths.append(self.get_datetime_accessed_path(path))
            paths.append(self.get_datetime_created_path(path))

        self.kvdb.conn.delete(*paths)

    def size(self, name):
        data = self.kvdb.conn.get(self.path(name))
        return len(data)

    def get_metadata_path(self, path):
        return '{}/{}'.format(self._metadata_name, path)

    def get_datetime_path(self, path):
        return self.get_metadata_path('{}/{}'.format(self._datetime_name, path))

    def get_datetime_created_path(self, path):
        return self.get_datetime_path('{}//{}'.format(self._created_name, path))

    def get_datetime_modified_path(self, path):
        return self.get_datetime_path('{}//{}'.format(self._modified_name, path))

    def get_datetime_accessed_path(self, path):
        return self.get_datetime_path('{}//{}'.format(self._accessed_name, path))

    def update_accessed_datetime(self, name, dt=None):
        if dt is None:
            dt = datetime.datetime.now(tz=pytz.utc)
        self.kvdb.conn.set(self.get_datetime_accessed_path(self.path(name)), dt.isoformat())

    def update_modified_datetime(self, name, dt=None):
        if dt is None:
            dt = datetime.datetime.now(tz=pytz.utc)
        self.kvdb.conn.set(self.get_datetime_modified_path(self.path(name)), dt.isoformat())
        self.update_accessed_datetime(name, dt=dt)

    def update_created_datetime(self, name, dt=None):
        if dt is None:
            dt = datetime.datetime.now(tz=pytz.utc)
        self.kvdb.conn.set(self.get_datetime_created_path(self.path(name)), dt.isoformat())
        self.update_modified_datetime(name, dt=dt)

    def _save(self, name, content, rewrite, encoding='utf8'):
        if self.exists(name):
            if not rewrite:
                name = self.get_available_name(name)
                self.update_created_datetime(name)
            self.update_modified_datetime(name)
        else:
            self.update_created_datetime(name)

        if isinstance(content, unicode):
            content = content.encode(encoding=encoding)

        self.kvdb.conn.set(self.path(name), content)
        return name

    def modified_time(self, name):
        if self.exists(name):
            return self.iso_to_datetime(self.kvdb.conn.get(self.get_datetime_modified_path(self.path(name))))
        else:
            raise ValueError(u'name: {} not found'.format(name))

    def _open(self, name, mode):
        self.update_accessed_datetime(name)
        data = self.kvdb.conn.get(self.path(name))
        data = data.decode(encoding='utf8')
        return StringIO(data)

    def exists(self, name):
        return self.kvdb.conn.exists(self.path(name))

    def accessed_time(self, name):
        if self.exists(name):
            return self.iso_to_datetime(self.kvdb.conn.get(self.get_datetime_accessed_path(self.path(name))))
        else:
            raise ValueError(u'name: {} not found'.format(name))

    def listdir(self, path_mask='*', full=True):
        keys = self.kvdb.conn.keys(self.path(path_mask))
        if full:
            return keys
        else:
            return [key.replace('{}/'.format(self.prefix), '') for key in keys]

    def path(self, *names):
        def _path(name):
            return '{}/{}'.format(self.prefix, name)
        if len(names) == 0:
            return self.prefix
        elif len(names) == 1:
            return _path(names[0])
        else:
            return (_path(name) for name in names)

    def iso_to_datetime(self, iso):
        return dateutil.parser.parse(iso)

    def created_time(self, name):
        if self.exists(name):
            return self.iso_to_datetime(self.kvdb.conn.get(self.get_datetime_created_path(self.path(name))))
        else:
            raise ValueError(u'name: {} not found'.format(name))

    def compare(self, *names):
        names = list(set(names))
        if len(names) <= 1:
            return True
        return len(set([self.kvdb.conn.get(name) for name in self.path(*names)])) == 1
