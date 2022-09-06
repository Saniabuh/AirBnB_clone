#!/usr/bin/python3
"""
This module contains unittests for class Review
"""

import inspect
from models import review
from models.base_model import BaseModel
import pycodestyle
import unittest
Review = review.Review


class TestReviewDocs(unittest.TestCase):
    """Tests to check the documentation and style of Review class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.review_f = inspect.getmembers(Review, inspect.isfunction)

    def test_pep8_conformance_review(self):
        """Test that models/review.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/review.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_review(self):
        """Test that tests/test_models/test_review.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_review.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_review_module_docstring(self):
        """Test for the review.py module docstring"""
        self.assertIsNot(review.__doc__, None,
                         "review.py needs a docstring")
        self.assertTrue(len(review.__doc__) >= 1,
                        "review.py needs a docstring")

    def test_review_class_docstring(self):
        """Test for the review class docstring"""
        self.assertIsNot(Review.__doc__, None,
                         "Review class needs a docstring")
        self.assertTrue(len(Review.__doc__) >= 1,
                        "Review class needs a docstring")

    def test_review_func_docstrings(self):
        """Test for the presence of docstrings in Review methods"""
        for func in self.review_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestReview(unittest.TestCase):
    """
    Tests the functionality of the Review class
    """

    def test_Inheritance(self):
        """
        Tests that Review is a subclass of BaseModel
        """
        review = Review()
        self.assertIsInstance(review, BaseModel)
        self.assertTrue(hasattr(review, "id"))
        self.assertTrue(hasattr(review, "created_at"))
        self.assertTrue(hasattr(review, "updated_at"))

    def test_Attributes(self):
        """
        Tests that the class has the correct attributes
        """
        review = Review()
        self.assertTrue(hasattr(Review, "user_id"))
        self.assertEqual(Review.user_id, "")
        self.assertTrue(hasattr(Review, "place_id"))
        self.assertEqual(Review.place_id, "")
        self.assertTrue(hasattr(Review, "text"))
        self.assertEqual(Review.text, "")

    def test_to_dict(self):
        """
        Tests that to_dict method works with Review
        """
        ri = Review()
        ndict = ri.to_dict()
        self.assertEqual(type(ndict), dict)
        for attr in ri.__dict__:
            self.assertTrue(attr in ndict)
            self.assertTrue("__class__" in ndict)

    def test_dict_values(self):
        """
        Tests that dictionary has correct values
        """
        isoforma = "%Y-%m-%dT%H:%M:%S.%f"
        ri = Review()
        new_d = ri.to_dict()
        self.assertEqual(new_d["__class__"], "Review")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], ri.created_at.strftime(isoforma))
        self.assertEqual(new_d["updated_at"], ri.updated_at.strftime(isoforma))

    def test_str(self):
        """
        Tests that str method returns correct output
        """
        review = Review()
        string = "[Review] ({}) {}".format(review.id, review.__dict__)
        self.assertEqual(string, str(review))
