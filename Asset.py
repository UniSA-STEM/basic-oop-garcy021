"""
File: Asset.py
Description: <A brief description of this Python module.>
Author: <full name>
ID: <student_id>
Username: <username>
This is my own work as defined by the University's Academic Misconduct Policy.
"""

class Asset:
    """
    Represents a digital asset in the cyberpunk world.
    Each asset has a name, a description, and may be encrypted.
    """

    def __init__(self, name, description, encrypted=False):
        self._name = name
        self._description = description
        self._encrypted = encrypted

    # ----- Properties -----
    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def encrypted(self):
        return self._encrypted

    @encrypted.setter
    def encrypted(self, value):
        self._encrypted = value

    # ----- String Representation -----
    def __str__(self):
        base = f"{self._name}: {self._description}"
        return f"{base} [Encrypted]" if self._encrypted else base
