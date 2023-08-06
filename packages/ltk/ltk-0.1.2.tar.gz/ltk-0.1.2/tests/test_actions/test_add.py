from tests.test_actions import *
from ltk.actions import Action
import os
import unittest

class TestAdd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        create_config()

    @classmethod
    def tearDownClass(cls):
        cleanup()

    def setUp(self):
        self.action = Action(os.getcwd())
        self.added_files = []

    def tearDown(self):
        for fn in self.added_files:
            self.action.rm_action(fn, True)
        self.action.clean_action(False, False, None)

    def test_add_db(self):
        # check document added to db
        file_name = 'sample.txt'
        text_file_path = create_txt_file(file_name)
        self.added_files.append(text_file_path)
        self.action.add_action(None, [file_name])
        # check that document added in db
        assert self.action.doc_manager.get_doc_by_prop('name', file_name)

    def test_add_remote(self):
        # check that document added to Lingotek
        file_name = 'sample.txt'
        text_file_path = create_txt_file(file_name)
        self.added_files.append(text_file_path)
        self.action.add_action(None, [file_name])
        doc_id = self.action.doc_manager.get_doc_ids()[0]
        assert poll_doc(self.action, doc_id)

    def test_add_pattern_db(self):
        # test that adding with a pattern gets all expected matches in local db
        files = ['sample.txt', 'sample1.txt', 'sample2.txt']
        for fn in files:
            self.added_files.append(create_txt_file(fn))
        self.action.add_action(None, ['sample*.txt'])
        for fn in files:
            assert self.action.doc_manager.get_doc_by_prop('name', fn)

    def test_add_pattern_remote(self):
        # test that adding with a pattern gets all expected matches in Lingotek
        files = ['sample.txt', 'sample1.txt', 'sample2.txt']
        for fn in files:
            self.added_files.append(create_txt_file(fn))
        self.action.add_action(None, ['sample*.txt'])
        doc_ids = self.action.doc_manager.get_doc_ids()
        for doc_id in doc_ids:
            assert poll_doc(self.action, doc_id)

    # todo test all those other args
