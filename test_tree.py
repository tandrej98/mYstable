import tree
import unittest


class TestNameSpace(unittest.TestCase):
    def setUp(self):
        self.ns = tree.NameSpace()

    def test_space_add(self):
        self.ns.space_add('k', '/etc/gss/bc')
        self.assertTrue(self.ns.space_test('k', '/etc/gss/bc'))
        self.assertFalse(self.ns.space_test('j', '/etc/gss/bc'))
        self.assertFalse(self.ns.space_test('k', '/etc/gss'))
        self.assertFalse(self.ns.space_test('k', '/etc/gss/bsd'))

        self.ns.space_add(
            'k', 'etc/gss/bc', '/etc/ssh/id_rsa', '/home/user/elis/images',
            '/home/user/david/documents/','/e/sitepackages/tree',
        )
        self.ns.space_add(
            'j', '/', '/home/user/elis',
        )
        self.assertTrue(self.ns.space_test('k', '/etc/gss/bc'))
        self.assertTrue(self.ns.space_test('k', '/etc/ssh/id_rsa'))
        self.assertTrue(self.ns.space_test('k', '/home/user/elis/images'))
        self.assertTrue(self.ns.space_test('k', '/home/user/david/documents/'))
        self.assertTrue(self.ns.space_test('k', '/e/sitepackages/tree'))
        self.assertFalse(self.ns.space_test('k', '/'))
        self.assertFalse(self.ns.space_test('k', '/home/user/elis'))
        self.assertTrue(self.ns.space_test('j', '/'))
        self.assertTrue(self.ns.space_test('j', '/home/user/elis'))

    def test_space_remove(self):
        self.ns.space_add(
            'k', '/etc/gss/bc', '/etc/ssh/id_rsa', '/home/user/elis/images',
            '/home/user/david/documents/','/e/sitepackages/tree',
        )
        self.ns.space_add(
            'j', '/', '/home/user/elis',
        )
        self.ns.space_remove(
            'k', '/etc/ssh/id_rsa', '/home/user/elis/images', '/e/sitepackages/tree',
        )
        self.ns.space_remove(
            'j', '/',
        )
        self.assertTrue(self.ns.space_test('k', '/etc/gss/bc'))
        self.assertFalse(self.ns.space_test('k', '/etc/ssh/id_rsa'))
        self.assertFalse(self.ns.space_test('k', '/home/user/elis/images'))
        self.assertTrue(self.ns.space_test('k', '/home/user/david/documents/'))
        self.assertFalse(self.ns.space_test('k', '/e/sitepackages/tree'))
        self.assertFalse(self.ns.space_test('j', '/'))
        self.assertTrue(self.ns.space_test('j', '/home/user/elis'))
        
        self.ns.space_remove(
            'k', '/etc/gss/bc', '/etc/ssh/id_rsa', '/home/user/elis/images',
            '/home/user/david/documents/','/e/sitepackages/tree',
        )
        self.ns.space_remove(
            'j', '/', '/home/user/elis',
        )
        self.assertFalse(self.ns.space_test('k', '/etc/gss/bc'))
        self.assertFalse(self.ns.space_test('k', '/etc/ssh/id_rsa'))
        self.assertFalse(self.ns.space_test('k', '/home/user/elis/images'))
        self.assertFalse(self.ns.space_test('k', '/home/user/david/documents/'))
        self.assertFalse(self.ns.space_test('k', '/e/sitepackages/tree'))
        self.assertFalse(self.ns.space_test('j', '/'))
        self.assertFalse(self.ns.space_test('j', '/home/user/elis'))


if __name__ == '__main__':
    unittest.main()
    