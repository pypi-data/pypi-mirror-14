import tempfile
import unittest

class TestFileSystemStorage(unittest.TestCase):

    def test_fs(self):
        from vtr_storages.storages.filesystem import Storage

        location = tempfile.mkdtemp()
        s = Storage(location=location)

        name = s.save('jopa', 'test')
        self.assertEqual(s.open(name).read(), 'test')

        self.assertEqual(s.size(name), 4)

        self.assertTrue(s.exists(name))

        s.delete(name)

        self.assertFalse(s.exists(name))

        import errno
        def remove(name):
            er = OSError()
            er.errno = errno.ENOENT
            raise er

        import os
        os.remove = remove
        name = s.save(name, 'test')
        s.delete(name)

        reload(os)

        s.delete(name)
        self.assertFalse(s.exists(name))

        s.save('test/test.txt', '')
        s.save(name, 'test')
        dirs = s.listdir('')
        self.assertEqual(dirs, (['test'], [name]))

        s.save('text.txt', 'old')
        name = s.save('text.txt', 'new')
        self.assertNotEqual('text.txt', name)

        name = s.save('text.txt', 'new', rewrite=True)
        self.assertEqual(name, 'text.txt')

        s.accessed_time(name)
        s.modified_time(name)
        s.created_time(name)


        storage = s
        storage.save('compare1', 'compare')
        storage.save('compare2', 'compare')
        storage.save('compare3', 'compare_')
        storage.save('compare4', 'compare')

        self.assertFalse(storage.compare('compare1', 'compare2', 'compare3', 'compare4'))
        self.assertTrue(storage.compare('compare1'))
        self.assertTrue(storage.compare('compare1', 'compare2', 'compare4'))
        self.assertTrue(storage.compare('compare3', 'compare3'))
        self.assertFalse(storage.compare('compare1', 'compare3'))
        self.assertTrue(storage.compare())

        storage.save('unicode', u'compare')

        self.assertEqual(storage.path(), location)

        storage.save('new/1', '1')
        storage.save('new/2', '2')
        storage.save('new/3', '3')

        files = storage.listdir('new')[1]
        files.sort()
        self.assertEqual(files, ['1', '2', '3'])
        self.assertEqual(list(storage.path('new/1', 'new/2', 'new/3')), [os.path.join(location, 'new/1'), os.path.join(location, 'new/2'), os.path.join(location, 'new/3')])
