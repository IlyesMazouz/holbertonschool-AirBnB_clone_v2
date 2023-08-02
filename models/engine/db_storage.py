#!/usr/bin/python3
"""This module defines a class to manage file storage for the hbnb clone"""

import json


class FileStorage:
    """This class manages the storage of hbnb models in JSON format"""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of models currently in storage.

        If cls is provided, returns a dictionary
        of models of the specified class.
        """
        if cls is not None:
            new = {}
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    new[key] = value
            return new
        return FileStorage.__objects

    def new(self, obj):
        """Adds a new object to the storage dictionary"""
        self.all().update({obj.to_dict()["__class__"] + "." + obj.id: obj})

    def save(self):
        """Saves the storage dictionary to a file in JSON format"""
        with open(FileStorage.__file_path, "w") as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f, indent=2)

    def reload(self):
        """Loads the storage dictionary from the JSON file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.place import Place
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Review": Review,
        }
        try:
            temp = {}
            with open(FileStorage.__file_path, "r") as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val["__class__"]](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes an object from the storage dictionary"""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
        else:
            return
        if key in self.__objects:
            del self.__objects[key]
            self.save()

    def close(self):
        """Closes the session and reloads the data"""
        self.reload()
