import os
import unittest
from tempfile import TemporaryDirectory

from jinjayaml import main


class MyTestCase(unittest.TestCase):
    def test_something(self):
        with TemporaryDirectory() as tmpdirname:
            resutl_path = tmpdirname + '/test.py'
            main(['-y', 'test.yaml', '-t', '.', '-o', tmpdirname, '-e', 'py'])
            self.assertTrue(os.path.exists(resutl_path))

            with open(resutl_path) as f:
                self.assertEqual(f.readline(), 'abc\n')


if __name__ == '__main__':
    unittest.main()
