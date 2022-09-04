#!/usr/bin/python3

"""
Test module for the console 'create' command
"""
import os
import sys
import json
import unittest
from io import StringIO
from unittest.mock import patch

import models
from models.user import User
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel
from console import HBNBCommand as CMD

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
"""Add parent dir to sys path"""
sys.path.append(parent_dir)


class TestConsole(unittest.TestCase):
    """Test 'help', 'quit', 'EOF' and  empty line'"""

    def test_help(self):
        ideal = ("Documented commands (type help <topic>):\n"
                 "========================================\n"
                 "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as f:
            CMD().onecmd("help")
            self.assertEqual(f.getvalue().strip(), ideal)

    def test_quit(self):
        """test quit"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertTrue(CMD().onecmd("quit"))

    def test_EOF(self):
        """test EOF"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertTrue(CMD().onecmd("EOF"))

    def test_empty_line(self):
        """test empty line"""
        with patch("sys.stdout", new=StringIO()) as f:
            CMD().onecmd("")
            self.assertEqual(f.getvalue().strip(), "")


class TestCreateCommand(unittest.TestCase):
    """
    Tests for create command
    """

    def setUp(self):
        """Reset storage object"""
        models.storage.clean()

    def tearDown(self):
        """Remove storage after every test"""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def output(self, cmd):
        """Returns console output"""
        with patch('sys.stdout', new=StringIO()) as f:
            CMD().onecmd(cmd)
            return f.getvalue()

    def storage(self):
        """Retrieves storage content"""
        try:
            with open('file.json', mode='r', encoding='utf-8') as file:
                data = file.read()
                return json.loads(data)
        except Exception:
            return {}

    def validModel(self, model):
        """Tests with valid model"""
        cmd = "{} {}".format("create", model)
        output = (self.output(cmd)).strip("\n")
        data = self.storage()
        """Check json content"""
        self.assertEqual(1, len(data))
        """Validate key"""
        key = "{}.{}".format(model, output)
        self.assertIn(key, data.keys())
        """Validate initial attributes"""
        value = data.get(key, {})
        values = value.keys()
        self.assertTrue(type(value) == dict)
        self.assertIn("id", values)
        self.assertIn("created_at", values)
        self.assertIn("updated_at", values)
        self.assertTrue("__class__", values)
        """Check attribute values"""
        self.assertEqual(value.get("id", None), output)
        self.assertEqual(value.get("__class__", None), model)

    def test_without_model(self):
        """without model"""
        output = self.output('create')
        expected = '** class name missing **\n'
        self.assertEqual(output, expected)

    def test_with_unknown_model(self):
        """With unknown model"""
        output = self.output("create Django")
        expected = "** class doesn't exist **\n"
        self.assertEqual(output, expected)

    def test_with_user_model(self):
        """with User model"""
        self.validModel("User")

    def test_with_base_model(self):
        """with BaseModel model"""
        self.validModel("BaseModel")

    def test_with_city_model(self):
        """with City model"""
        self.validModel("City")

    def test_with_state_model(self):
        """with State model"""
        self.validModel("State")

    def test_with_place_model(self):
        """with Place model"""
        self.validModel("Place")

    def test_with_review_model(self):
        """with Review model"""
        self.validModel("Review")

    def test_with_amenity_model(self):
        """with Amenity model"""
        self.validModel("Review")


class TestShowCommand(unittest.TestCase):
    """
    Test show command
    """

    def setUp(self):
        """Reset storage object"""
        models.storage.clean()

    def tearDown(self):
        """Remove storage after every test"""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def output(self, cmd):
        """Returns console output"""
        with patch('sys.stdout', new=StringIO()) as f:
            CMD().onecmd(cmd)
            return f.getvalue()

    def test_without_model(self):
        """test without model"""
        output = self.output("show")
        expected = "** class name missing **\n"
        self.assertEqual(output, expected)

    def test_with_invalid_model(self):
        """test with invalid model"""
        output = self.output("show MyModel")
        expected = "** class doesn't exist **\n"
        self.assertEqual(output, expected)

    def test_with_base_model_without_id(self):
        """test with BaseModel model no id"""
        expected = "** instance id missing **\n"
        output = self.output("show BaseModel")
        self.assertEqual(output, expected)

    def test_with_user_model_without_id(self):
        """test with User model no id"""
        expected = "** instance id missing **\n"
        output = self.output("show User")
        self.assertEqual(output, expected)

    def test_with_city_model_without_id(self):
        """test with City model no id"""
        expected = "** instance id missing **\n"
        output = self.output("show City")
        self.assertEqual(output, expected)

    def test_with_state_model_without_id(self):
        """test with State model no id"""
        expected = "** instance id missing **\n"
        output = self.output("show State")
        self.assertEqual(output, expected)

    def test_with_place_model_without_id(self):
        """test with Place model no id"""
        expected = "** instance id missing **\n"
        output = self.output("show Place")
        self.assertEqual(output, expected)

    def test_with_review_model_without_id(self):
        """test with Review model no id"""
        expected = "** instance id missing **\n"
        output = self.output("show Review")
        self.assertEqual(output, expected)

    def test_with_amenity_model_without_id(self):
        """test with Amenity model no id"""
        expected = "** instance id missing **\n"
        output = self.output("show Amenity")
        self.assertEqual(output, expected)

    def test_with_base_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("show BaseModel 88888")
        self.assertEqual(output, expected)

    def test_with_user_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("show User 88888")
        self.assertEqual(output, expected)

    def test_with_city_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("show City 88888")
        self.assertEqual(output, expected)

    def test_with_state_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("show State 88888")
        self.assertEqual(output, expected)

    def test_with_place_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("show Place 88888")
        self.assertEqual(output, expected)

    def test_with_review_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("show Review 88888")
        self.assertEqual(output, expected)

    def test_with_amenity_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("show Amenity 88888")
        self.assertEqual(output, expected)

    def test_with_user_model_valid_id(self):
        user = User()
        cmd = "show User {}".format(user.id)
        output = (self.output(cmd)).strip('\n')
        expected = str(user)
        self.assertEqual(output, expected)

    def test_with_base_model_valid_id(self):
        base = BaseModel()
        cmd = "show BaseModel {}".format(base.id)
        output = (self.output(cmd)).strip('\n')
        expected = str(base)
        self.assertEqual(output, expected)

    def test_with_city_model_valid_id(self):
        city = City()
        cmd = "show City {}".format(city.id)
        output = (self.output(cmd)).strip('\n')
        expected = str(city)
        self.assertEqual(output, expected)

    def test_with_state_model_valid_id(self):
        state = State()
        cmd = "show State {}".format(state.id)
        output = (self.output(cmd)).strip('\n')
        expected = str(state)
        self.assertEqual(output, expected)

    def test_with_place_model_valid_id(self):
        place = Place()
        cmd = "show Place {}".format(place.id)
        output = (self.output(cmd)).strip('\n')
        expected = str(place)
        self.assertEqual(output, expected)

    def test_with_review_model_valid_id(self):
        review = Review()
        cmd = "show Review {}".format(review.id)
        output = (self.output(cmd)).strip('\n')
        expected = str(review)
        self.assertEqual(output, expected)

    def test_with_amenity_model_valid_id(self):
        amenity = Amenity()
        cmd = "show Amenity {}".format(amenity.id)
        output = (self.output(cmd)).strip('\n')
        expected = str(amenity)
        self.assertEqual(output, expected)


class TestModelDotShowCommand(unittest.TestCase):
    """
    Test show command
    """
    def setUp(self):
        """Reset storage object"""
        models.storage.clean()

    def tearDown(self):
        """Remove storage after every test"""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def output(self, cmd):
        """Returns console output"""
        with patch('sys.stdout', new=StringIO()) as f:
            CMD().onecmd(cmd)
            return f.getvalue()

    def test_with_invalid_model(self):
        """test with invalid model"""
        output = self.output("MyModel.show()")
        expected = "** class doesn't exist **\n"
        self.assertEqual(output, expected)

    def withoutId(self, model):
        """test without model"""
        expected = "** instance id missing **\n"
        cmd = '{}.show()'.format(model)
        output = self.output(cmd)
        self.assertEqual(output, expected)

    def test_with_base_model_without_id(self):
        """test with BaseModel model no id"""
        self.withoutId("BaseModel")

    def test_with_user_model_without_id(self):
        """test with User model no id"""
        self.withoutId("User")

    def test_with_city_model_without_id(self):
        """test with City model no id"""
        self.withoutId("City")

    def test_with_state_model_without_id(self):
        """test with State model no id"""
        self.withoutId("State")

    def test_with_place_model_without_id(self):
        """test with Place model no id"""
        self.withoutId("Place")

    def test_with_review_model_without_id(self):
        """test with Review model no id"""
        self.withoutId("Review")

    def test_with_amenity_model_without_id(self):
        """test with Amenity model no id"""
        self.withoutId("Amenity")

    def test_with_base_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output('BaseModel.show("88888")')
        self.assertEqual(output, expected)

    def test_with_user_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output('User.show("88888")')
        self.assertEqual(output, expected)

    def test_with_city_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output('City.show("88888")')
        self.assertEqual(output, expected)

    def test_with_state_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output('State.show("88888")')
        self.assertEqual(output, expected)

    def test_with_place_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output('Place.show("88888")')
        self.assertEqual(output, expected)

    def test_with_review_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output('Review.show("88888")')
        self.assertEqual(output, expected)

    def test_with_amenity_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output('Amenity.show("88888")')
        self.assertEqual(output, expected)

    def with_empty_id_string(self, model):
        expected = "** no instance found **\n"
        output = self.output('{}.show("")'.format(model))
        self.assertEqual(output, expected)

    def test_with_base_model_with_empty_id(self):
        self.with_empty_id_string("BaseModel")

    def test_with_user_model_with_empty_id(self):
        self.with_empty_id_string("User")

    def test_with_city_model_with_empty_id(self):
        self.with_empty_id_string("City")

    def test_with_state_model_with_empty_id(self):
        self.with_empty_id_string("State")

    def test_with_place_model_with_empty_id(self):
        self.with_empty_id_string("Place")

    def test_with_review_model_with_empty_id(self):
        self.with_empty_id_string("Review")

    def test_with_amenity_model_with_empty_id(self):
        self.with_empty_id_string("Amenity")

    def test_with_user_model_valid_id(self):
        user = User()
        cmd = 'User.show("{}")'.format(user.id)
        output = (self.output(cmd)).strip('\n')
        expected = str(user)
        self.assertEqual(output, expected)

    def test_with_base_model_valid_id(self):
        base = BaseModel()
        cmd = 'BaseModel.show("{}")'.format(base.id)
        output = (self.output(cmd)).strip('\n')
        expected = str(base)
        self.assertEqual(output, expected)

    def test_with_city_model_valid_id(self):
        city = City()
        cmd = 'City.show("{}")'.format(city.id)
        output = (self.output(cmd)).strip('\n')
        expected = str(city)
        self.assertEqual(output, expected)

    def test_with_state_model_valid_id(self):
        state = State()
        cmd = 'State.show("{}")'.format(state.id)
        output = (self.output(cmd)).strip('\n')
        expected = str(state)
        self.assertEqual(output, expected)

    def test_with_place_model_valid_id(self):
        place = Place()
        cmd = 'Place.show("{}")'.format(place.id)
        output = (self.output(cmd)).strip('\n')
        expected = str(place)
        self.assertEqual(output, expected)

    def test_with_review_model_valid_id(self):
        review = Review()
        cmd = 'Review.show("{}")'.format(review.id)
        output = (self.output(cmd)).strip('\n')
        expected = str(review)
        self.assertEqual(output, expected)

    def test_with_amenity_model_valid_id(self):
        amenity = Amenity()
        cmd = 'Amenity.show("{}")'.format(amenity.id)
        output = (self.output(cmd)).strip('\n')
        expected = str(amenity)
        self.assertEqual(output, expected)


class TestDestroyCommand(unittest.TestCase):
    """
    Test show command
    """
    @classmethod
    def setUpClass(cls):
        """Reset storage object"""
        models.storage.clean()
        cls.base = BaseModel()
        cls.user = User()
        cls.city = City()
        cls.state = State()
        cls.place = Place()
        cls.review = Review()
        cls.amenity = Amenity()
        objs = models.storage.all()

    @classmethod
    def tearDownClass(cls):
        """Remove storage after every test"""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def storage(self):
        """Retrieves storage content"""
        try:
            with open('file.json', mode='r', encoding='utf-8') as file:
                data = file.read()
                return json.loads(data)
        except Exception:
            return {}

    def output(self, cmd):
        """Returns console output"""
        with patch('sys.stdout', new=StringIO()) as f:
            CMD().onecmd(cmd)
            return f.getvalue()

    def test_without_model(self):
        """test without model"""
        output = self.output("destroy")
        expected = "** class name missing **\n"
        self.assertEqual(output, expected)

    def test_with_invalid_model(self):
        """test with invalid model"""
        output = self.output("destroy MyModel")
        expected = "** class doesn't exist **\n"
        self.assertEqual(output, expected)

    def test_with_base_model_without_id(self):
        """test with BaseModel model no id"""
        expected = "** instance id missing **\n"
        output = self.output("destroy BaseModel")
        self.assertEqual(output, expected)

    def test_with_user_model_without_id(self):
        """test with User model no id"""
        expected = "** instance id missing **\n"
        output = self.output("destroy User")
        self.assertEqual(output, expected)

    def test_with_city_model_without_id(self):
        """test with City model no id"""
        expected = "** instance id missing **\n"
        output = self.output("destroy City")
        self.assertEqual(output, expected)

    def test_with_state_model_without_id(self):
        """test with State model no id"""
        expected = "** instance id missing **\n"
        output = self.output("destroy State")
        self.assertEqual(output, expected)

    def test_with_place_model_without_id(self):
        """test with Place model no id"""
        expected = "** instance id missing **\n"
        output = self.output("destroy Place")
        self.assertEqual(output, expected)

    def test_with_review_model_without_id(self):
        """test with Review model no id"""
        expected = "** instance id missing **\n"
        output = self.output("destroy Review")
        self.assertEqual(output, expected)

    def test_with_amenity_model_without_id(self):
        """test with Amenity model no id"""
        expected = "** instance id missing **\n"
        output = self.output("destroy Amenity")
        self.assertEqual(output, expected)

    def test_with_base_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("destroy BaseModel 88888")
        self.assertEqual(output, expected)

    def test_with_user_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("destroy User 88888")
        self.assertEqual(output, expected)

    def test_with_city_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("destroy City 88888")
        self.assertEqual(output, expected)

    def test_with_state_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("destroy State 88888")
        self.assertEqual(output, expected)

    def test_with_place_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("destroy Place 88888")
        self.assertEqual(output, expected)

    def test_with_review_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("destroy Review 88888")
        self.assertEqual(output, expected)

    def test_with_amenity_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("destroy Amenity 88888")
        self.assertEqual(output, expected)

    def test_with_user_model_valid_id(self):
        key = "{}.{}".format("User", self.user.id)
        cmd = "destroy User {}".format(self.user.id)
        output = (self.output(cmd)).strip('\n')
        storage = self.storage()
        self.assertEqual(output, "")
        self.assertNotIn(key, models.storage.all())
        self.assertIsNone(storage.get(key, None))

    def test_with_base_model_valid_id(self):
        key = "{}.{}".format("BaseModel", self.base.id)
        cmd = "destroy BaseModel {}".format(self.base.id)
        output = (self.output(cmd)).strip('\n')
        storage = self.storage()
        self.assertEqual(output, "")
        self.assertNotIn(key, models.storage.all())
        self.assertIsNone(storage.get(key, None))

    def test_with_city_model_valid_id(self):
        key = "{}.{}".format("City", self.city.id)
        cmd = "destroy City {}".format(self.city.id)
        output = (self.output(cmd)).strip('\n')
        storage = self.storage()
        self.assertEqual(output, "")
        self.assertNotIn(key, models.storage.all())
        self.assertIsNone(storage.get(key, None))

    def test_with_state_model_valid_id(self):
        key = "{}.{}".format("Review", self.state.id)
        cmd = "destroy State {}".format(self.state.id)
        output = (self.output(cmd)).strip('\n')
        storage = self.storage()
        self.assertEqual(output, "")
        self.assertNotIn(key, models.storage.all())
        self.assertIsNone(storage.get(key, None))

    def test_with_place_model_valid_id(self):
        key = "{}.{}".format("Place", self.place.id)
        cmd = "destroy Place {}".format(self.place.id)
        output = (self.output(cmd)).strip('\n')
        storage = self.storage()
        self.assertEqual(output, "")
        self.assertNotIn(key, models.storage.all())
        self.assertIsNone(storage.get(key, None))

    def test_with_review_model_valid_id(self):
        key = "{}.{}".format("Review", self.review.id)
        cmd = "destroy Review {}".format(self.review.id)
        output = (self.output(cmd)).strip('\n')
        storage = self.storage()
        self.assertEqual(output, "")
        self.assertNotIn(key, models.storage.all())
        self.assertIsNone(storage.get(key, None))

    def test_with_amenity_model_valid_id(self):
        key = "{}.{}".format("Amenity", self.amenity.id)
        cmd = "destroy Amenity {}".format(self.amenity.id)
        output = (self.output(cmd)).strip('\n')
        storage = self.storage()
        self.assertEqual(output, "")
        self.assertNotIn(key, models.storage.all())
        self.assertIsNone(storage.get(key, None))


class TestModelDotDestroyCommand(unittest.TestCase):
    """
    Test show command
    """
    @classmethod
    def setUpClass(cls):
        """Reset storage object"""
        models.storage.clean()
        cls.base = BaseModel()
        cls.user = User()
        cls.city = City()
        cls.state = State()
        cls.place = Place()
        cls.review = Review()
        cls.amenity = Amenity()
        objs = models.storage.all()

    @classmethod
    def tearDownClass(cls):
        """Remove storage after every test"""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def storage(self):
        """Retrieves storage content"""
        try:
            with open('file.json', mode='r', encoding='utf-8') as file:
                data = file.read()
                return json.loads(data)
        except Exception:
            return {}

    def output(self, cmd):
        """Returns console output"""
        with patch('sys.stdout', new=StringIO()) as f:
            CMD().onecmd(cmd)
            return f.getvalue()

    def test_with_invalid_model(self):
        """test with invalid model"""
        output = self.output("MyModel.destroy()")
        expected = "** class doesn't exist **\n"
        self.assertEqual(output, expected)

    def withoutId(self, model):
        """test without model"""
        expected = "** instance id missing **\n"
        cmd = '{}.destroy()'.format(model)
        output = self.output(cmd)
        self.assertEqual(output, expected)

    def test_with_base_model_without_id(self):
        """test with BaseModel model no id"""
        self.withoutId("BaseModel")

    def test_with_user_model_without_id(self):
        """test with User model no id"""
        self.withoutId("User")

    def test_with_city_model_without_id(self):
        """test with City model no id"""
        self.withoutId("City")

    def test_with_state_model_without_id(self):
        """test with State model no id"""
        self.withoutId("State")

    def test_with_place_model_without_id(self):
        """test with Place model no id"""
        self.withoutId("Place")

    def test_with_review_model_without_id(self):
        """test with Review model no id"""
        self.withoutId("Review")

    def test_with_amenity_model_without_id(self):
        """test with Amenity model no id"""
        self.withoutId("Amenity")

    def test_with_base_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output('BaseModel.destroy("88888")')
        self.assertEqual(output, expected)

    def test_with_user_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output('User.destroy("88888")')
        self.assertEqual(output, expected)

    def test_with_city_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output('City.destroy("88888")')
        self.assertEqual(output, expected)

    def test_with_state_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output('State.destroy("88888")')
        self.assertEqual(output, expected)

    def test_with_place_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output('Place.destroy("88888")')
        self.assertEqual(output, expected)

    def test_with_review_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output('Review.destroy("88888")')
        self.assertEqual(output, expected)

    def test_with_amenity_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output('Amenity.destroy("88888")')
        self.assertEqual(output, expected)

    def with_empty_id_string(self, model):
        expected = "** no instance found **\n"
        output = self.output('{}.destroy("")'.format(model))
        self.assertEqual(output, expected)

    def test_with_base_model_with_empty_id(self):
        self.with_empty_id_string("BaseModel")

    def test_with_user_model_with_empty_id(self):
        self.with_empty_id_string("User")

    def test_with_city_model_with_empty_id(self):
        self.with_empty_id_string("City")

    def test_with_state_model_with_empty_id(self):
        self.with_empty_id_string("State")

    def test_with_place_model_with_empty_id(self):
        self.with_empty_id_string("Place")

    def test_with_review_model_with_empty_id(self):
        self.with_empty_id_string("Review")

    def test_with_amenity_model_with_empty_id(self):
        self.with_empty_id_string("Amenity")

    def test_with_user_model_valid_id(self):
        key = "{}.{}".format("User", self.user.id)
        cmd = 'User.destroy("{}")'.format(self.user.id)
        output = (self.output(cmd)).strip('\n')
        storage = self.storage()
        self.assertEqual(output, "")
        self.assertNotIn(key, models.storage.all())
        self.assertIsNone(storage.get(key, None))

    def test_with_base_model_valid_id(self):
        key = "{}.{}".format("BaseModel", self.base.id)
        cmd = 'BaseModel.destroy("{}")'.format(self.base.id)
        output = (self.output(cmd)).strip('\n')
        storage = self.storage()
        self.assertEqual(output, "")
        self.assertNotIn(key, models.storage.all())
        self.assertIsNone(storage.get(key, None))

    def test_with_city_model_valid_id(self):
        key = "{}.{}".format("City", self.city.id)
        cmd = 'City.destroy("{}")'.format(self.city.id)
        output = (self.output(cmd)).strip('\n')
        storage = self.storage()
        self.assertEqual(output, "")
        self.assertNotIn(key, models.storage.all())
        self.assertIsNone(storage.get(key, None))

    def test_with_state_model_valid_id(self):
        key = "{}.{}".format("Review", self.state.id)
        cmd = 'State.destroy("{}")'.format(self.state.id)
        output = (self.output(cmd)).strip('\n')
        storage = self.storage()
        self.assertEqual(output, "")
        self.assertNotIn(key, models.storage.all())
        self.assertIsNone(storage.get(key, None))

    def test_with_place_model_valid_id(self):
        key = "{}.{}".format("Place", self.place.id)
        cmd = 'Place.destroy("{}")'.format(self.place.id)
        output = (self.output(cmd)).strip('\n')
        storage = self.storage()
        self.assertEqual(output, "")
        self.assertNotIn(key, models.storage.all())
        self.assertIsNone(storage.get(key, None))

    def test_with_review_model_valid_id(self):
        key = "{}.{}".format("Review", self.review.id)
        cmd = 'Review.destroy("{}")'.format(self.review.id)
        output = (self.output(cmd)).strip('\n')
        storage = self.storage()
        self.assertEqual(output, "")
        self.assertNotIn(key, models.storage.all())
        self.assertIsNone(storage.get(key, None))

    def test_with_amenity_model_valid_id(self):
        key = "{}.{}".format("Amenity", self.amenity.id)
        cmd = 'Amenity.destroy("{}")'.format(self.amenity.id)
        output = (self.output(cmd)).strip('\n')
        storage = self.storage()
        self.assertEqual(output, "")
        self.assertNotIn(key, models.storage.all())
        self.assertIsNone(storage.get(key, None))


class TestAllCommand(unittest.TestCase):
    """
    Test show command
    """
    def setUp(self):
        """Reset storage object"""
        models.storage.clean()
        self.base = BaseModel()
        self.user = User()
        self.city = City()
        self.state = State()
        self.place = Place()
        self.review = Review()
        self.amenity = Amenity()

    def tearDown(self):
        """Remove storage after every test"""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def output(self, cmd):
        """Returns console output"""
        with patch('sys.stdout', new=StringIO()) as f:
            CMD().onecmd(cmd)
            return f.getvalue()

    def test_without_model(self):
        """test without model"""
        output = self.output("all")
        expected = '["{}", "{}", "{}", "{}", "{}", "{}", "{}"]'.format(
            str(self.base), str(self.user), str(self.city), str(self.state),
            str(self.place), str(self.review), str(self.amenity)
        )
        self.assertEqual(output.strip(), expected)

    def test_with_invalid_model(self):
        """test with invalid model"""
        output = self.output("all MyModel")
        expected = "** class doesn't exist **\n"
        self.assertEqual(output, expected)

    def test_with_base_model(self):
        """test with BaseModel model no id"""
        output = self.output("all BaseModel")
        expected = '["{}"]'.format(str(self.base))
        self.assertEqual(output.strip(), expected)

    def test_with_user_model(self):
        """test with User model no id"""
        output = self.output("all User")
        expected = '["{}"]'.format(str(self.user))
        self.assertEqual(output.strip(), expected)

    def test_with_city_model(self):
        """test with City model no id"""
        output = self.output("all City")
        expected = '["{}"]'.format(str(self.city))
        self.assertEqual(output.strip(), expected)

    def test_with_state_model(self):
        """test with State model no id"""
        output = self.output("all State")
        expected = '["{}"]'.format(str(self.state))
        self.assertEqual(output.strip(), expected)

    def test_with_place_model(self):
        """test with Place model no id"""
        output = self.output("all Place")
        expected = '["{}"]'.format(str(self.place))
        self.assertEqual(output.strip(), expected)

    def test_with_review_model(self):
        """test with Review model no id"""
        output = self.output("all Review")
        expected = '["{}"]'.format(str(self.review))
        self.assertEqual(output.strip(), expected)

    def test_with_amenity_model(self):
        """test with Amenity model no id"""
        output = self.output("all Amenity")
        expected = '["{}"]'.format(str(self.amenity))
        self.assertEqual(output.strip(), expected)

    def test_with_empty_storage(self):
        """test with empty file storage"""
        models.storage.clean()
        output = self.output("all")
        self.assertEqual(output.strip(), '[]')


class TestModelDotAllCommand(unittest.TestCase):
    """
    Test show command
    """
    def setUp(self):
        """Reset storage object"""
        models.storage.clean()
        self.base = BaseModel()
        self.user = User()
        self.city = City()
        self.state = State()
        self.place = Place()
        self.review = Review()
        self.amenity = Amenity()

    def tearDown(self):
        """Remove storage after every test"""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def output(self, cmd):
        """Returns console output"""
        with patch('sys.stdout', new=StringIO()) as f:
            CMD().onecmd(cmd)
            return f.getvalue()

    def test_with_invalid_model(self):
        """test with invalid model"""
        output = self.output("MyModel.all()")
        expected = "** class doesn't exist **\n"
        self.assertEqual(output, expected)

    def test_with_base_model(self):
        """test with BaseModel model no id"""
        output = self.output("BaseModel.all()")
        expected = '["{}"]'.format(str(self.base))
        self.assertEqual(output.strip(), expected)

    def test_with_user_model(self):
        """test with User model no id"""
        output = self.output("User.all()")
        expected = '["{}"]'.format(str(self.user))
        self.assertEqual(output.strip(), expected)

    def test_with_city_model(self):
        """test with City model no id"""
        output = self.output("City.all()")
        expected = '["{}"]'.format(str(self.city))
        self.assertEqual(output.strip(), expected)

    def test_with_state_model(self):
        """test with State model no id"""
        output = self.output("State.all()")
        expected = '["{}"]'.format(str(self.state))
        self.assertEqual(output.strip(), expected)

    def test_with_place_model(self):
        """test with Place model no id"""
        output = self.output("Place.all()")
        expected = '["{}"]'.format(str(self.place))
        self.assertEqual(output.strip(), expected)

    def test_with_review_model(self):
        """test with Review model no id"""
        output = self.output("Review.all()")
        expected = '["{}"]'.format(str(self.review))
        self.assertEqual(output.strip(), expected)

    def test_with_amenity_model(self):
        """test with Amenity model no id"""
        output = self.output("Amenity.all()")
        expected = '["{}"]'.format(str(self.amenity))
        self.assertEqual(output.strip(), expected)

    def test_with_empty_storage(self):
        """test with empty file storage"""
        models.storage.clean()
        output = self.output("User.all()")
        self.assertEqual(output.strip(), '[]')


class TestModelDotCountCommand(unittest.TestCase):
    """
    Test show command
    """
    def setUp(self):
        """Reset storage object"""
        models.storage.clean()
        self.base = BaseModel()
        self.user = User()
        self.city = City()
        self.state = State()
        self.place = Place()
        self.review = Review()
        self.amenity = Amenity()

    def tearDown(self):
        """Remove storage after every test"""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def output(self, cmd):
        """Returns console output"""
        with patch('sys.stdout', new=StringIO()) as f:
            CMD().onecmd(cmd)
            return f.getvalue()

    def test_with_invalid_model(self):
        """test with invalid model"""
        output = self.output("MyModel.count()")
        expected = "** class doesn't exist **\n"
        self.assertEqual(output, expected)

    def test_with_base_model(self):
        """test with BaseModel model no id"""
        output = self.output("BaseModel.count()")
        self.assertEqual(output.strip(), '1')

    def test_with_user_model(self):
        """test with User model no id"""
        output = self.output("User.count()")
        self.assertEqual(output.strip(), '1')

    def test_with_city_model(self):
        """test with City model no id"""
        output = self.output("City.count()")
        self.assertEqual(output.strip(), '1')

    def test_with_state_model(self):
        """test with State model no id"""
        output = self.output("State.count()")
        self.assertEqual(output.strip(), '1')

    def test_with_place_model(self):
        """test with Place model no id"""
        output = self.output("Place.count()")
        self.assertEqual(output.strip(), '1')

    def test_with_review_model(self):
        """test with Review model no id"""
        output = self.output("Review.count()")
        self.assertEqual(output.strip(), '1')

    def test_with_amenity_model(self):
        """test with Amenity model no id"""
        output = self.output("Amenity.count()")
        self.assertEqual(output.strip(), '1')

    def test_with_empty_storage(self):
        """test with empty file storage"""
        models.storage.clean()
        output = self.output("User.count()")
        self.assertEqual(output.strip(), '0')


class TestAllCommand(unittest.TestCase):
    """
    Test show command
    """
    def setUp(self):
        """Reset storage object"""
        models.storage.clean()
        self.base = BaseModel()
        self.user = User()
        self.city = City()
        self.state = State()
        self.place = Place()
        self.review = Review()
        self.amenity = Amenity()

    def tearDown(self):
        """Remove storage after every test"""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def output(self, cmd):
        """Returns console output"""
        with patch('sys.stdout', new=StringIO()) as f:
            CMD().onecmd(cmd)
            return f.getvalue()

    def test_without_model(self):
        """test without model"""
        output = self.output("all")
        expected = '["{}", "{}", "{}", "{}", "{}", "{}", "{}"]'.format(
            str(self.base), str(self.user), str(self.city), str(self.state),
            str(self.place), str(self.review), str(self.amenity)
        )
        self.assertEqual(output.strip(), expected)

    def test_with_invalid_model(self):
        """test with invalid model"""
        output = self.output("all MyModel")
        expected = "** class doesn't exist **\n"
        self.assertEqual(output, expected)

    def test_with_base_model(self):
        """test with BaseModel model no id"""
        output = self.output("all BaseModel")
        expected = '["{}"]'.format(str(self.base))
        self.assertEqual(output.strip(), expected)

    def test_with_user_model(self):
        """test with User model no id"""
        output = self.output("all User")
        expected = '["{}"]'.format(str(self.user))
        self.assertEqual(output.strip(), expected)

    def test_with_city_model(self):
        """test with City model no id"""
        output = self.output("all City")
        expected = '["{}"]'.format(str(self.city))
        self.assertEqual(output.strip(), expected)

    def test_with_state_model(self):
        """test with State model no id"""
        output = self.output("all State")
        expected = '["{}"]'.format(str(self.state))
        self.assertEqual(output.strip(), expected)

    def test_with_place_model(self):
        """test with Place model no id"""
        output = self.output("all Place")
        expected = '["{}"]'.format(str(self.place))
        self.assertEqual(output.strip(), expected)

    def test_with_review_model(self):
        """test with Review model no id"""
        output = self.output("all Review")
        expected = '["{}"]'.format(str(self.review))
        self.assertEqual(output.strip(), expected)

    def test_with_amenity_model(self):
        """test with Amenity model no id"""
        output = self.output("all Amenity")
        expected = '["{}"]'.format(str(self.amenity))
        self.assertEqual(output.strip(), expected)

    def test_with_empty_storage(self):
        """test with empty file storage"""
        models.storage.clean()
        output = self.output("all")
        self.assertEqual(output.strip(), '[]')


class TestUpdateCommand(unittest.TestCase):
    """
    Test show command
    """
    @classmethod
    def setUpClass(cls):
        """Reset storage object"""
        models.storage.clean()
        cls.base = BaseModel()
        cls.user = User()
        cls.city = City()
        cls.state = State()
        cls.place = Place()
        cls.review = Review()
        cls.amenity = Amenity()

    @classmethod
    def tearDownClass(cls):
        """Remove storage after every test"""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def storage(self):
        """Retrieves storage content"""
        try:
            with open('file.json', mode='r', encoding='utf-8') as file:
                data = file.read()
                return json.loads(data)
        except Exception:
            return {}

    def output(self, cmd):
        """Returns console output"""
        with patch('sys.stdout', new=StringIO()) as f:
            CMD().onecmd(cmd)
            return f.getvalue()

    def test_without_model(self):
        """test without model"""
        output = self.output("update")
        expected = "** class name missing **\n"
        self.assertEqual(output, expected)

    def test_with_invalid_model(self):
        """test with invalid model"""
        output = self.output("update MyModel")
        expected = "** class doesn't exist **\n"
        self.assertEqual(output, expected)

    def test_with_base_model_without_id(self):
        """test with BaseModel model no id"""
        expected = "** instance id missing **\n"
        output = self.output("update BaseModel")
        self.assertEqual(output, expected)

    def test_with_user_model_without_id(self):
        """test with User model no id"""
        expected = "** instance id missing **\n"
        output = self.output("update User")
        self.assertEqual(output, expected)

    def test_with_city_model_without_id(self):
        """test with City model no id"""
        expected = "** instance id missing **\n"
        output = self.output("update City")
        self.assertEqual(output, expected)

    def test_with_state_model_without_id(self):
        """test with State model no id"""
        expected = "** instance id missing **\n"
        output = self.output("update State")
        self.assertEqual(output, expected)

    def test_with_place_model_without_id(self):
        """test with Place model no id"""
        expected = "** instance id missing **\n"
        output = self.output("update Place")
        self.assertEqual(output, expected)

    def test_with_review_model_without_id(self):
        """test with Review model no id"""
        expected = "** instance id missing **\n"
        output = self.output("update Review")
        self.assertEqual(output, expected)

    def test_with_amenity_model_without_id(self):
        """test with Amenity model no id"""
        expected = "** instance id missing **\n"
        output = self.output("update Amenity")
        self.assertEqual(output, expected)

    def test_with_base_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("update BaseModel 88888")
        self.assertEqual(output, expected)

    def test_with_user_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("update User 88888")
        self.assertEqual(output, expected)

    def test_with_city_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("update City 88888")
        self.assertEqual(output, expected)

    def test_with_state_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("update State 88888")
        self.assertEqual(output, expected)

    def test_with_place_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("update Place 88888")
        self.assertEqual(output, expected)

    def test_with_review_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("update Review 88888")
        self.assertEqual(output, expected)

    def test_with_amenity_model_invalid_id(self):
        expected = "** no instance found **\n"
        output = self.output("update Amenity 88888")
        self.assertEqual(output, expected)

    def test_with_user_model_without_attribute(self):
        cmd = "update User {}".format(self.user.id)
        output = self.output(cmd)
        expected = "** attribute name missing **\n"
        self.assertEqual(output, expected)

    def test_with_base_model_without_attribute(self):
        cmd = "update BaseModel {}".format(self.base.id)
        output = self.output(cmd)
        expected = "** attribute name missing **\n"
        self.assertEqual(output, expected)

    def test_with_city_model_without_attribute(self):
        cmd = "update City {}".format(self.city.id)
        output = self.output(cmd)
        expected = "** attribute name missing **\n"
        self.assertEqual(output, expected)

    def test_with_state_model_without_attribute(self):
        cmd = "update State {}".format(self.state.id)
        output = self.output(cmd)
        expected = "** attribute name missing **\n"
        self.assertEqual(output, expected)

    def test_with_place_model_without_attribute(self):
        cmd = "update Place {}".format(self.place.id)
        output = self.output(cmd)
        expected = "** attribute name missing **\n"
        self.assertEqual(output, expected)

    def test_with_review_model_without_attribute(self):
        cmd = "update State {}".format(self.state.id)
        output = self.output(cmd)
        expected = "** attribute name missing **\n"
        self.assertEqual(output, expected)

    def test_with_amenity_model_without_attribute(self):
        cmd = "update Amenity {}".format(self.amenity.id)
        output = self.output(cmd)
        expected = "** attribute name missing **\n"
        self.assertEqual(output, expected)

    def test_with_base_model_without_attribute_value(self):
        cmd = "update BaseModel {} name".format(self.base.id)
        output = self.output(cmd)
        expected = "** value missing **\n"
        self.assertEqual(output, expected)

    def test_with_user_model_without_attribute_value(self):
        cmd = "update User {} name".format(self.user.id)
        output = self.output(cmd)
        expected = "** value missing **\n"
        self.assertEqual(output, expected)

    def test_with_city_model_without_attribute(self):
        cmd = "update City {} name".format(self.city.id)
        output = self.output(cmd)
        expected = "** value missing **\n"
        self.assertEqual(output, expected)

    def test_with_state_model_without_attribute(self):
        cmd = "update State {} name".format(self.state.id)
        output = self.output(cmd)
        expected = "** value missing **\n"
        self.assertEqual(output, expected)

    def test_with_place_model_without_attribute_value(self):
        cmd = "update Place {} name".format(self.place.id)
        output = self.output(cmd)
        expected = "** value missing **\n"
        self.assertEqual(output, expected)

    def test_with_review_model_without_attribute_value(self):
        cmd = "update Review {} name".format(self.review.id)
        output = self.output(cmd)
        expected = "** value missing **\n"
        self.assertEqual(output, expected)

    def test_with_amenity_model_without_attribute_value(self):
        cmd = "update Amenity {} name".format(self.amenity.id)
        output = self.output(cmd)
        expected = "** value missing **\n"
        self.assertEqual(output, expected)

    def single(self, model, obj):
        cmd = "update {} {} name Ludten".format(model, obj.id)
        previousUpdate = obj.updated_at
        output = self.output(cmd)
        self.assertEqual(output, "")
        self.assertTrue(obj.updated_at > previousUpdate)
        self.assertEqual(getattr(obj, "name", ""), "Ludten")

    def test_with_base_model_with_single_attribute_value(self):
        self.single('BaseModel', self.base)

    def test_with_user_model_with_single_attribute_value(self):
        self.single('User', self.user)

    def test_with_city_model_with_single_attribute_value(self):
        self.single('City', self.city)

    def test_with_state_model_with_single_attribute_value(self):
        self.single('State', self.state)

    def test_with_place_model_with_single_attribute_value(self):
        self.single('Place', self.place)

    def test_with_review_model_with_single_attribute_value(self):
        self.single('Review', self.review)

    def test_with_amenity_model_with_single_attribute_value(self):
        self.single('Amenity', self.amenity)

    def double(self, model, obj):
        cmd = "update {} {} 'grade' '1st class' age 27".format(model, obj.id)
        previousUpdate = obj.updated_at
        output = self.output(cmd)
        self.assertEqual(output, "")
        self.assertTrue(obj.updated_at > previousUpdate)
        self.assertEqual(getattr(obj, "grade", ""), "1st class")
        self.assertFalse(hasattr(obj, 'age'))

    def test_with_base_model_with_double_attribute_value(self):
        self.double('BaseModel', self.base)

    def test_with_user_model_with_double_attribute_value(self):
        self.double('User', self.user)

    def test_with_city_model_with_double_attribute_value(self):
        self.double('City', self.city)

    def test_with_state_model_with_double_attribute_value(self):
        self.double('State', self.state)

    def test_with_place_model_with_double_attribute_value(self):
        self.double('Place', self.place)

    def test_with_review_model_with_double_attribute_value(self):
        self.double('Review', self.review)

    def test_with_amenity_model_with_double_attribute_value(self):
        self.double('Amenity', self.amenity)


class TestModelDotUpdateCommand(unittest.TestCase):
    """
    Test dotted update command
    """
    @classmethod
    def setUpClass(cls):
        """Reset storage object"""
        models.storage.clean()
        cls.base = BaseModel()
        cls.user = User()
        cls.city = City()
        cls.state = State()
        cls.place = Place()
        cls.review = Review()
        cls.amenity = Amenity()

    @classmethod
    def tearDownClass(cls):
        """Remove storage after every test"""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def storage(self):
        """Retrieves storage content"""
        try:
            with open('file.json', mode='r', encoding='utf-8') as file:
                data = file.read()
                return json.loads(data)
        except Exception:
            return {}

    def output(self, cmd):
        """Returns console output"""
        with patch('sys.stdout', new=StringIO()) as f:
            CMD().onecmd(cmd)
            return f.getvalue()

    def test_with_invalid_model(self):
        """test with invalid model"""
        output = self.output(f"MyModel.update('9787676', 'name', 'Ludten')")
        expected = "** class doesn't exist **\n"
        self.assertEqual(output, expected)

    def withoutId(self, model):
        """test without model"""
        expected = "** instance id missing **\n"
        cmd = "{}.update()".format(model)
        output = self.output(cmd)
        self.assertEqual(output, expected)

    def test_with_base_model_without_id(self):
        self.withoutId('BaseModel')

    def test_with_user_model_without_id(self):
        self.withoutId('User')

    def test_with_city_model_without_id(self):
        self.withoutId('City')

    def test_with_state_model_without_id(self):
        self.withoutId('State')

    def test_with_place_model_without_id(self):
        self.withoutId('Place')

    def test_with_review_model_without_id(self):
        self.withoutId('Review')

    def test_with_amenity_model_without_id(self):
        self.withoutId('Amenity')

    def withInvalidId(self, model):
        """test with in valid id"""
        expected = "** no instance found **\n"
        cmd = '{}.update("687876786")'.format(model)
        output = self.output(cmd)
        self.assertEqual(output, expected)

    def test_with_base_model_invalid_id(self):
        self.withInvalidId('BaseModel')

    def test_with_user_model_invalid_id(self):
        self.withInvalidId('User')

    def test_with_city_model_invalid_id(self):
        self.withInvalidId('City')

    def test_with_state_model_invalid_id(self):
        self.withInvalidId('State')

    def test_with_place_model_invalid_id(self):
        self.withInvalidId('Place')

    def test_with_review_model_invalid_id(self):
        self.withInvalidId('Review')

    def test_with_amenity_model_invalid_id(self):
        self.withInvalidId('Amenity')

    def withoutAttribute(self, model, uid):
        expected = "** attribute name missing **\n"
        cmd = '{}.update("{}")'.format(model, uid)
        output = self.output(cmd)
        self.assertEqual(output, expected)

    def test_with_user_model_without_attribute(self):
        self.withoutAttribute('BaseModel', self.base.id)

    def test_with_base_model_without_attribute(self):
        self.withoutAttribute('User', self.user.id)

    def test_with_city_model_without_attribute(self):
        self.withoutAttribute('City', self.city.id)

    def test_with_state_model_without_attribute(self):
        self.withoutAttribute('State', self.state.id)

    def test_with_place_model_without_attribute(self):
        self.withoutAttribute('Place', self.place.id)

    def test_with_review_model_without_attribute(self):
        self.withoutAttribute('Review', self.review.id)

    def test_with_amenity_model_without_attribute(self):
        self.withoutAttribute('Amenity', self.amenity.id)

    def withoutAttributeValue(self, model, uid):
        """test without attribute value"""
        expected = "** value missing **\n"
        cmd = '{}.update("{}", "name")'.format(model, uid)
        output = self.output(cmd)
        self.assertEqual(output, expected)

    def test_with_base_model_without_attribute_value(self):
        self.withoutAttributeValue('BaseModel', self.base.id)

    def test_with_user_model_without_attribute_value(self):
        self.withoutAttributeValue('User', self.user.id)

    def test_with_city_model_without_attribute(self):
        self.withoutAttributeValue('City', self.city.id)

    def test_with_state_model_without_attribute(self):
        self.withoutAttributeValue('State', self.state.id)

    def test_with_place_model_without_attribute_value(self):
        self.withoutAttributeValue('Place', self.place.id)

    def test_with_review_model_without_attribute_value(self):
        self.withoutAttributeValue('Review', self.review.id)

    def test_with_amenity_model_without_attribute_value(self):
        self.withoutAttributeValue('Amenity', self.amenity.id)

    def with_valid_id_attribute_and_value(self, model, obj):
        cmd = '{}.update("{}", "name" "John Doe")'.format(model, obj.id)
        previousUpdate = obj.updated_at
        output = self.output(cmd)
        self.assertEqual(output, "")
        self.assertTrue(obj.updated_at > previousUpdate)
        self.assertEqual(getattr(obj, "name", ""), "John Doe")

    def test_with_base_model_with_string_attribute_value(self):
        self.with_valid_id_attribute_and_value('BaseModel', self.base)

    def test_with_user_model_with_string_attribute_value(self):
        self.with_valid_id_attribute_and_value('User', self.user)

    def test_with_city_model_with_string_attribute_value(self):
        self.with_valid_id_attribute_and_value('City', self.city)

    def test_with_state_model_with_string_attribute_value(self):
        self.with_valid_id_attribute_and_value('State', self.state)

    def test_with_place_model_with_string_attribute_value(self):
        self.with_valid_id_attribute_and_value('Place', self.place)

    def test_with_review_model_with_string_attribute_value(self):
        self.with_valid_id_attribute_and_value('Review', self.review)

    def test_with_amenity_model_with_string_attribute_value(self):
        self.with_valid_id_attribute_and_value('Amenity', self.amenity)

    def with_valid_id_and_empty_dictionary(self, model, obj):
        cmd = '{}.update("{}", {})'.format(model, obj.id, {})
        updated_at = obj.updated_at
        output = self.output(cmd)
        expected = ""
        self.assertEqual(output, expected)
        self.assertEqual(updated_at, obj.updated_at)

    def test_base_model_with_empty_dictionary(self):
        self.with_valid_id_and_empty_dictionary('BaseModel', self.base)

    def test_user_model_with_empty_dictionary(self):
        self.with_valid_id_and_empty_dictionary('User', self.user)

    def test_city_model_with_empty_dictionary(self):
        self.with_valid_id_and_empty_dictionary('City', self.city)

    def test_state_model_with_empty_dictionary(self):
        self.with_valid_id_and_empty_dictionary('State', self.state)

    def test_place_model_with_empty_dictionary(self):
        self.with_valid_id_and_empty_dictionary('Place', self.place)

    def test_review_model_with_empty_dictionary(self):
        self.with_valid_id_and_empty_dictionary('Review', self.review)

    def test_amenity_model_with_empty_dictionary(self):
        self.with_valid_id_and_empty_dictionary('Amenity', self.amenity)

    def with_valid_id_and_dictionary(self, model, obj):
        cmd = '{}.update("{}", {})'.format(
            model, obj.id, {"grade": "1st class", "age": 27}
        )
        previousUpdate = obj.updated_at
        output = self.output(cmd)
        self.assertEqual(output, "")
        self.assertTrue(obj.updated_at > previousUpdate)
        self.assertTrue(hasattr(obj, 'grade'))
        self.assertEqual(getattr(obj, "grade", ""), "1st class")
        self.assertTrue(hasattr(obj, 'age'))
        self.assertEqual(getattr(obj, 'age', 0), 27)

    def test_with_base_model_with_double_attribute_value(self):
        self.with_valid_id_and_dictionary('BaseModel', self.base)

    def test_with_user_model_with_double_attribute_value(self):
        self.with_valid_id_and_dictionary('User', self.user)

    def test_with_city_model_with_double_attribute_value(self):
        self.with_valid_id_and_dictionary('City', self.city)

    def test_with_state_model_with_double_attribute_value(self):
        self.with_valid_id_and_dictionary('State', self.state)

    def test_with_place_model_with_double_attribute_value(self):
        self.with_valid_id_and_dictionary('Place', self.place)

    def test_with_review_model_with_double_attribute_value(self):
        self.with_valid_id_and_dictionary('Review', self.review)

    def test_with_amenity_model_with_double_attribute_value(self):
        self.with_valid_id_and_dictionary('Amenity', self.amenity)
