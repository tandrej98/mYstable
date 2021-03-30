import tree
import unittest


class TestNameSpace(unittest.TestCase):
    def setUp(self):
        self.ns = tree.NameSpace()

    def test_space_add(self):
        # self.ns = tree.NameSpace()
        self.ns.space_add('k', '/etc/gss/bc')
        self.ns.space_update()
        self.assertTrue(self.ns.space_test('k', '/etc/gss/bc'))
        self.assertFalse(self.ns.space_test('j', '/etc/gss/bc'))
        self.assertFalse(self.ns.space_test('k', '/etc/gss'))
        self.assertFalse(self.ns.space_test('k', '/etc/gss/bsd'))

        self.ns.space_add(
            'k',
            '/etc/gss/bc',
            '/etc/ssh/id_rsa',
            '/home/user/elis/images',
            '/home/user/david/documents/',
            '/e/sitepackages/tree',
        )

        self.ns.space_add(
            'j',
            '/',
            '/home/user/elis',
        )
        self.ns.space_update()

        self.assertTrue(self.ns.space_test('k', '/etc/gss/bc'))
        self.assertTrue(self.ns.space_test('k', '/etc/ssh/id_rsa'))
        self.assertTrue(self.ns.space_test('k', '/home/user/elis/images'))
        self.assertTrue(self.ns.space_test('k', '/home/user/david/documents/'))
        self.assertTrue(self.ns.space_test('k', '/e/sitepackages/tree'))
        self.assertFalse(self.ns.space_test('k', '/'))
        self.assertFalse(self.ns.space_test('k', '/home/user/elis'))
        self.assertTrue(self.ns.space_test('j', '/'))
        self.assertTrue(self.ns.space_test('j', '/home/user/elis'))

    def test_space_sub(self):
        # self.ns = tree.NameSpace()
        self.ns.space_add(
            'k',
            '/etc/gss/bc',
            '/etc/ssh/id_rsa',
            '/home/user/elis/images',
            '/home/user/david/documents/',
            '/e/sitepackages/tree',
        )
        self.ns.space_add(
            'j',
            '/',
            '/home/user/elis',
        )
        self.ns.space_sub(
            'k',
            '/etc/ssh/id_rsa',
            '/home/user/elis/images',
            '/e/sitepackages/tree',
        )
        self.ns.space_sub(
            'j',
            '/',
        )
        self.ns.space_update()

        self.assertTrue(self.ns.space_test('k', '/etc/gss/bc'))
        self.assertFalse(self.ns.space_test('k', '/etc/ssh/id_rsa'))
        self.assertFalse(self.ns.space_test('k', '/home/user/elis/images'))
        self.assertTrue(self.ns.space_test('k', '/home/user/david/documents/'))
        self.assertFalse(self.ns.space_test('k', '/e/sitepackages/tree'))
        self.assertFalse(self.ns.space_test('j', '/'))
        self.assertTrue(self.ns.space_test('j', '/home/user/elis'))

        self.ns.space_sub(
            'k',
            '/etc/gss/bc',
            '/etc/ssh/id_rsa',
            '/home/user/elis/images',
            '/home/user/david/documents/',
            '/e/sitepackages/tree',
        )
        self.ns.space_sub(
            'j',
            '/',
            '/home/user/elis',
        )
        self.ns.space_update()

        self.assertFalse(self.ns.space_test('k', '/etc/gss/bc'))
        self.assertFalse(self.ns.space_test('k', '/etc/ssh/id_rsa'))
        self.assertFalse(self.ns.space_test('k', '/home/user/elis/images'))
        self.assertFalse(self.ns.space_test('k',
                                            '/home/user/david/documents/'))
        self.assertFalse(self.ns.space_test('k', '/e/sitepackages/tree'))
        self.assertFalse(self.ns.space_test('j', '/'))
        self.assertFalse(self.ns.space_test('j', '/home/user/elis'))

    def test_spaces_update(self):
        # self.ns = tree.NameSpace()
        self.ns.space_add('d', '/etc/gss/bc', '/etc/gss/mgr', '/etc/gss/phd')
        self.ns.space_add('k', 'd')
        self.ns.space_update()
        self.assertTrue(
            self.ns.space_test('k', '/etc/gss/bc', '/etc/gss/mgr',
                               '/etc/gss/phd'))
        self.assertTrue(
            self.ns.space_test('d', '/etc/gss/bc', '/etc/gss/mgr',
                               '/etc/gss/phd'))

    def test_spaces_cycle(self):
        '''
        space1 = path1 path2 ... space2 
        space2 = path3 path4 ... space3
        space3 = path5 path6 ... space1
        '''
        self.ns.space_add('space1', '/etc/gss/bc', '/etc/gss/mgr',
                          '/etc/gss/phd', 'space2')
        self.ns.space_add('space2', '/etc/gss/bc', '/etc/gss/mgr',
                          '/etc/gss/phd', 'space3')
        self.ns.space_add('space3', '/etc/gss/bc', '/etc/gss/mgr',
                          '/etc/gss/phd', 'space1')
        self.ns.space_update()


if __name__ == '__main__':
    unittest.main()
