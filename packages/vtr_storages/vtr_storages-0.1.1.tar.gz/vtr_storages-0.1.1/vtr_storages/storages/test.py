import unittest

class TestAbstractStorage(unittest.TestCase):

    def test_storage(self):

        from vtr_storages.storages import AbstractStorage, SuspiciousFileOperation

        class Storage(AbstractStorage):

            def _save(self, name, content, rewrite, encoding='utf8'):
                return name

            def _open(self, name, mode):
                return name, mode

            def exists(self, name):
                return name == 'exists'

            def compare(self, *names):
                """compare"""

        storage = Storage()
        f = storage.open('test', 'rb')
        self.assertEqual(f, ('test', 'rb'))

        res = storage.save('test', 'content')
        self.assertEqual(res, 'test')

        storage.get_available_name('exists')
        storage.get_available_name('exists', 10)
        ok = False
        try:
            storage.get_available_name('exists', 1)
        except SuspiciousFileOperation:
            ok = True

        self.assertTrue(ok)

        name = storage.get_valid_name('jopa!*!*!```~~~123')
        self.assertEqual(name, 'jopa123')

        # test not Implemented
        not_implemented_methods = [
            'path',
            'delete',
            'listdir',
            'size',
            'accessed_time',
            'created_time',
            'modified_time',
        ]
        for method_name in not_implemented_methods:
            ok = False
            try:
                method = getattr(storage, method_name)
                method('test')
            except NotImplementedError:
                ok = True

            self.assertTrue(ok)
