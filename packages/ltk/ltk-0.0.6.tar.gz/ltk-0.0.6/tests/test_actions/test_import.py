from tests.test_actions import *
from ltk.actions import Action

import unittest

class TestImport(unittest.TestCase):
    def setUp(self):
        create_config()
        self.action = Action(os.getcwd())

    def tearDown(self):
        cleanup()

    def test_import_all(self):
        pass

    def test_import_locale(self):
        # test importing a document that already has a locale
        pass

    def test_import_no_locale(self):
        pass
