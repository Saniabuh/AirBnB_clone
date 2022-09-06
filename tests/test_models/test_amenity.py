#!/usr/bin/python3
"""
This module contains unittests for class Amenity
"""

import inspect
from models import amenity
from models.base_model import BaseModel
import pycodestyle
import unittest
Amenity = amenity.Amenity


class TestAmenityDocs(unittest.TestCase):
    """Tests to check the documentation and style of Amenity class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.amenity_f = inspect.getmembers(Amenity, inspect.isfunction)

    def test_pep8_conformance_amenity(self):
        """Test that models/amenity.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/amenity.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_amenity(self):
        """Test that tests/test_models/test_amenity.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_amenity.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_amenity_module_docstring(self):
        """Test for the amenity.py module docstring"""
        self.assertIsNot(amenity.__doc__, None,
                         "amenity.py needs a docstring")
        self.assertTrue(len(amenity.__doc__) >= 1,
                        "amenity.py needs a docstring")

    def test_amenity_class_docstring(self):
        """Test for the Amenity class docstring"""
        self.assertIsNot(Amenity.__doc__, None,
                         "Amenity class needs a docstring")
        self.assertTrue(len(Amenity.__doc__) >= 1,
                        "Amenity class needs a docstring")

    def test_amenity_func_docstrings(self):
        """Test for the presence of docstrings in Amenity methods"""
        for func in self.amenity_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestAmenity(unittest.TestCase):
    """
    Tests the functionality of the Amenity class
    """

    def test_Inheritance(self):
        """
        Tests that Amenity is a subclass of BaseModel
        """
        amenity = Amenity()
        self.assertIsInstance(amenity, BaseModel)
        self.assertTrue(hasattr(amenity, "id"))
        self.assertTrue(hasattr(amenity, "created_at"))
        self.assertTrue(hasattr(amenity, "updated_at"))

    def test_Attributes(self):
        """
        Tests that the class has the correct attributes
        """
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, "name"))
        self.assertEqual(amenity.name, "")

    def test_to_dict(self):
        """
        Tests that to_dict method works with Amenity
        """
        am = Amenity()
        ndict = am.to_dict()
        self.assertEqual(type(ndict), dict)
        for attr in am.__dict__:
            self.assertTrue(attr in ndict)
            self.assertTrue("__class__" in ndict)

    def test_dict_values(self):
        """
        Tests that dictionary has correct values
        """
        isoforma = "%Y-%m-%dT%H:%M:%S.%f"
        am = Amenity()
        new_d = am.to_dict()
        self.assertEqual(new_d["__class__"], "Amenity")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], am.created_at.strftime(isoforma))
        self.assertEqual(new_d["updated_at"], am.updated_at.strftime(isoforma))

    def test_str(self):
        """
        Tests that str method returns correct output
        """
        amenity = Amenity()
        string = "[Amenity] ({}) {}".format(amenity.id, amenity.__dict__)
        self.assertEqual(string, str(amenity))
