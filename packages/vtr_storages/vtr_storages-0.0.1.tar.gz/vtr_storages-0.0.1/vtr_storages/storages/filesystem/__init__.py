# FileSystem Storage, forked from django project
import errno
import os
from datetime import datetime
from vtr_storages import locks
from vtr_storages.storages import AbstractStorage


class Storage(AbstractStorage):

    def __init__(self, location=None, file_permissions_mode=None,
                 directory_permissions_mode=None, **kwargs):
        self.location = location
        self.file_permissions_mode = file_permissions_mode
        self.directory_permissions_mode = directory_permissions_mode
        self.kwargs =kwargs

    def compare(self, *names):
        names = list(set(names))
        if len(names) <= 1:
            return True
        return len(set([self.open(name).read() for name in names])) == 1

    def _open(self, name, mode):
        return open(self.path(name), mode)

    def path(self, *names):
        def _path(name):
            return os.path.join(self.location, name)
        if len(names) == 0:
            return self.location
        elif len(names) == 1:
            return _path(names[0])
        else:
            return (_path(name) for name in names)

    def size(self, name):
        return os.path.getsize(self.path(name))

    def exists(self, name):
        return os.path.exists(self.path(name))

    def delete(self, name):
        assert name, "The name argument is not allowed to be empty."
        name = self.path(name)
        # If the file exists, delete it from the filesystem.
        # Note that there is a race between os.path.exists and os.remove:
        # if os.remove fails with ENOENT, the file was removed
        # concurrently, and we can continue normally.
        if os.path.exists(name):
            try:
                os.remove(name)
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise

    def listdir(self, path=''):
        path = self.path(path)
        directories, files = [], []
        for entry in os.listdir(path):
            if os.path.isdir(os.path.join(path, entry)):
                directories.append(entry)
            else:
                files.append(entry)
        return directories, files

    def accessed_time(self, name):
        return datetime.fromtimestamp(os.path.getatime(self.path(name)))

    def created_time(self, name):
        return datetime.fromtimestamp(os.path.getctime(self.path(name)))

    def modified_time(self, name):
        return datetime.fromtimestamp(os.path.getmtime(self.path(name)))

    def _save(self, name, content, rewrite, encoding='utf8'):
        """
        :param name: name of file, can be with dirs, save to self.location
        :param content: any bytes
        :param rewrite: create new file with name_random_string if False, rewrite file if True
        :return: name of file
        """
        full_path = self.path(name)
        if isinstance(content, unicode):
            content = content.encode(encoding=encoding)

        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            try:
                if self.directory_permissions_mode is not None:
                    # os.makedirs applies the global umask, so we reset it,
                    # for consistency with file_permissions_mode behavior.
                    old_umask = os.umask(0)
                    try:
                        os.makedirs(directory, self.directory_permissions_mode)
                    finally:
                        os.umask(old_umask)
                else:
                    os.makedirs(directory)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

        if not os.path.isdir(directory):
            raise IOError("%s exists and is not a directory." % directory)

        while True:
            try:
                flags = (os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                         getattr(os, 'O_BINARY', 0))
                # The current umask value is masked out by os.open!
                fd = os.open(full_path, flags, 0o666)
                _file = None
                try:
                    locks.lock(fd, locks.LOCK_EX)
                    mode = 'wb' if isinstance(content, bytes) else 'wt'
                    _file = os.fdopen(fd, mode)
                    _file.write(content)
                finally:
                    locks.unlock(fd)
                    if _file is not None:
                        _file.close()
                    else:
                        os.close(fd)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    # Ooops, the file exists. We need a new file name.
                    if not rewrite:
                        name = self.get_available_name(name)
                        full_path = self.path(name)
                    else:
                        self.delete(name)
                else:
                    raise
            else:
                break

        if self.file_permissions_mode is not None:
            os.chmod(full_path, self.file_permissions_mode)

        return name