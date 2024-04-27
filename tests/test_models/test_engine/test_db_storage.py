#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""


class TestDBStorage(unittest.TestCase):
    """Test cases for the DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the test class"""
        # Initialize DBStorage instance
        models.storage = DBStorage()

    def test_get_existing_object(self):
        """Test retrieving an existing object by ID"""
        # Create a State object and save it to the database
        state = State(name="California")
        state.save()
        # Retrieve the State object by ID using the get method
        retrieved_state = models.storage.get(State, state.id)
        # Assert that the retrieved object matches the original object
        self.assertEqual(retrieved_state.id, state.id)
        self.assertEqual(retrieved_state.name, state.name)

    def test_get_non_existing_object(self):
        """Test retrieving a non-existing object by ID"""
        # Attempt to retrieve an object with an invalid ID
        retrieved_state = models.storage.get(State, "invalid_id")
        # Assert that the retrieved object is None
        self.assertIsNone(retrieved_state)

    def test_get_invalid_input_types(self):
        """Test retrieving an object with invalid input types"""
        # Attempt to retrieve an object with invalid input types
        with self.assertRaises(TypeError):
            models.storage.get(State, None)
        with self.assertRaises(TypeError):
            models.storage.get(State, 123)

    def test_count_objects(self):
        """Test counting objects for a specific class"""
        # Create multiple State objects and save them to the database
        State(name="New York").save()
        State(name="Texas").save()
        # Count the number of State objects in the database
        state_count = models.storage.count(State)
        # Assert that the count matches the number of State objects created
        self.assertEqual(state_count, 2)

    def test_count_no_objects(self):
        """Test counting objects when there are no objects present"""
        # Count the number of State objects in the empty database
        state_count = models.storage.count(State)
        # Assert that the count is zero
        self.assertEqual(state_count, 0)

    def test_count_all_objects(self):
        """Test counting objects for all classes"""
        # Count the total number of objects in the database
        total_count = models.storage.count()
        # Assert that the count is equal to the sum of counts for all classes
        self.assertEqual(total_count, 2)  # Assuming 2 State created

    def test_count_invalid_input_types(self):
        """Test counting objects with invalid class input types"""
        # Attempt to count objects with invalid class input types
        with self.assertRaises(TypeError):
            models.storage.count(None)
        with self.assertRaises(TypeError):
            models.storage.count("State")
