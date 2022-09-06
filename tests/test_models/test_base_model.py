#!/usr/bin/python3
"""
Test BaseModel for expected behavior and documentation
"""
from datetime import datetime
import inspect
from models import base_model
import pycodestyle
import time
import unittest
from unittest import mock
BaseModel = base_model.BaseModel
module_doc = base_model.__doc__


class TestBaseModelDocs(unittest.TestCase):
    """Tests to check the documentation and style of BaseModel class"""

    @classmethod
    def setUpClass(self):
        """Set up for docstring tests"""
        self.base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/base_model.py conforms to PEP8."""
        for path in ['models/base_model.py',
                     'tests/test_models/test_base_model.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(module_doc, None,
                         "base_model.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "base_model.py needs a docstring")

    def test_class_docstring(self):
        """Test for the BaseModel class docstring"""
        self.assertIsNot(BaseModel.__doc__, None,
                         "BaseModel class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1,
                        "BaseModel class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in BaseModel methods"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__,
                    None,
                    "{:s} method needs a docstring".format(func[0])
                )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class TestBaseModel(unittest.TestCase):
    """
    Tests the functionality of the BaseModel
    """
    def testInit(self):
        """
        Tests the initialization of the class
        """
        hold = BaseModel()
        self.assertIs(type(hold), BaseModel)
        hold.name = "duba"
        hold.number = 77
        attr = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "number": int
        }
        for att, typ in attr.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertIn(att, hold.__dict__)
                self.assertIs(type(hold.__dict__[att]), typ)
        self.assertEqual(hold.name, "duba")
        self.assertEqual(hold.number, 77)

    def test_dates(self):
        """
        Testing the datetime attributes
        """
        start = datetime.now()
        hold = BaseModel()
        end = datetime.now()
        self.assertTrue(start <= hold.created_at <= end)
        time.sleep(1e-4)
        start = datetime.now()
        hold2 = BaseModel()
        end = datetime.now()
        self.assertTrue(start <= hold2.created_at <= end)
        self.assertNotEqual(hold.created_at, hold2.created_at)
        self.assertEqual(hold.created_at, hold.updated_at)
        self.assertNotEqual(hold.updated_at, hold2.updated_at)
        self.assertEqual(hold2.created_at, hold2.updated_at)

    def test_uuid(self):
        """
        Test that id is a valid uuid
        """
        hold1 = BaseModel()
        hold2 = BaseModel()
        for inst in [hold1, hold2]:
            uuid = inst.id
            with self.subTest(uuid=uuid):
                self.assertIs(type(uuid), str)
                self.assertRegex(uuid,
                                 '^[0-9a-f]{8}-[0-9a-f]{4}'
                                 '-[0-9a-f]{4}-[0-9a-f]{4}'
                                 '-[0-9a-f]{12}$')
        self.assertNotEqual(hold1.id, hold2.id)

    def test_to_dict(self):
        """
        Test conversion of object attributes to dictionary for json
        """
        my_model = BaseModel()
        my_model.name = "Osoraa"
        my_model.my_number = 99
        d = my_model.to_dict()
        expected_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "my_number",
                          "__class__"]
        self.assertCountEqual(d.keys(), expected_attrs)
        self.assertEqual(d['__class__'], 'BaseModel')
        self.assertEqual(d['name'], "Osoraa")
        self.assertEqual(d['my_number'], 99)

    def test_to_dict_values(self):
        """
        Test that values in dict returned from to_dict are correct
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        bm = BaseModel()
        new_d = bm.to_dict()
        self.assertEqual(new_d["__class__"], "BaseModel")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"],
                         bm.created_at.strftime(time_format))
        self.assertEqual(new_d["updated_at"],
                         bm.updated_at.strftime(time_format))

    def test_str(self):
        """
        Tests string representation of object
        """
        hold = BaseModel()
        string = "[BaseModel] ({}) {}".format(hold.id, hold.__dict__)
        self.assertEqual(string, str(hold))

    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        """
        Tests that only updated_at is changed after saving
        and that storage.save is called
        """
        hold = BaseModel()
        old_created_at = hold.created_at
        old_updated_at = hold.updated_at
        hold.save()
        new_created_at = hold.created_at
        new_updated_at = hold.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)
        self.assertTrue(mock_storage.save.called)


if __name__ == '__main__':
    unittest.main()
