import fakeredis
import unittest

class FakeKVDB(object):

    conn = fakeredis.FakeStrictRedis()

class TestKVDBStorage(unittest.TestCase):

    def test_kvdb(self):

        kvdb = FakeKVDB()

        from vtr_storages.storages.kvdb import Storage

        storage = Storage(kvdb)

        storage.save('lol', 'lol data')
        da = storage.accessed_time('lol')
        dc = storage.created_time('lol')
        dm = storage.modified_time('lol')
        data = storage.open('lol').read()
        self.assertEqual(data, 'lol data')
        self.assertNotEqual(da, storage.accessed_time('lol'))
        self.assertEqual(dc, dm)
        da = storage.accessed_time('lol')
        storage.save('lol', content='new lol data', rewrite=True)
        dm = storage.modified_time('lol')
        self.assertNotEqual(dm, dc)
        self.assertEqual(dm, storage.accessed_time('lol'))
        self.assertEqual(dc, storage.created_time('lol'))
        self.assertNotEqual(da, storage.accessed_time('lol'))
        self.assertEqual('new lol data', storage.open('lol').read())
        self.assertEqual(len(storage.open('lol').read()), len('new lol data'))
        self.assertEqual(len(storage.open('lol').read()), storage.size('lol'))
        self.assertEqual(len('new lol data'), storage.size('lol'))

        self.assertTrue(storage.exists('lol'))
        self.assertNotEqual(storage.get_available_name('lol'), 'lol')
        new_name = storage.save('lol', 'new lol content')
        self.assertNotEqual(new_name, 'lol')
        self.assertNotEqual(storage.created_time('lol'), storage.created_time(new_name))
        self.assertNotEqual(storage.modified_time('lol'), storage.modified_time(new_name))
        self.assertNotEqual(storage.accessed_time('lol'), storage.accessed_time(new_name))
        storage.delete('lol')
        self.assertFalse(storage.exists('lol'))
        self.assertRaises(ValueError, storage.accessed_time, 'lol')
        self.assertRaises(ValueError, storage.created_time, 'lol')
        self.assertRaises(ValueError, storage.modified_time, 'lol')

        self.assertEqual(storage.path(), storage.prefix)
        self.assertEqual(list(storage.path('1', '2')), [storage.path('1'), storage.path('2')])

        self.assertEqual(storage.get_available_name('lol'), 'lol')

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

        storage._delete_paths(*storage.listdir())
        self.assertEqual(storage.listdir(), [])

        storage.save('lol', 'lol data')
        self.assertEqual(storage.listdir('*', full=False), ['lol'])
        storage.delete(*storage.listdir('*', full=False))
        self.assertEqual(storage.listdir('*', full=False), [])

        storage.save(storage.get_metadata_path('lol'), content='lol')
        self.assertEqual(storage.listdir('*', full=False), [storage.get_metadata_path('lol')])

        storage._delete_paths(*storage.listdir())
        name = storage.get_datetime_created_path('lol')
        storage.save(name, content='lol')
        self.assertEqual(storage.listdir('*', full=False), [name])

        storage._delete_paths(*storage.listdir())
        name = storage.get_datetime_modified_path('lol')
        storage.save(name, content='lol')
        self.assertEqual(storage.listdir('*', full=False), [name])

        storage._delete_paths(*storage.listdir())
        name = storage.get_datetime_accessed_path('lol')
        storage.save(name, content='lol')
        self.assertEqual(storage.listdir('*', full=False), [name])

        storage._delete_paths(storage.path(name))
        self.assertEqual(storage.kvdb.conn.keys('*'), [])
