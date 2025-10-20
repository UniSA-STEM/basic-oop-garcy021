"""
File: Asset.py
Description: Defines the Asset class for items that can be stored, encrypted, or transferred between hackers and rigs.
Author: CHIRAG GARG
ID: 110395864
Username: GARCY021
This is my own work as defined by the University's Academic Misconduct Policy.
"""

"""
Represents a digital asset that hackers can own, store or transfer.
Each asset has a name, a description, and an encrypted state.
"""
class Asset:
    def __init__(self, name, description, encrypted=False):
        self._name = name
        self._description = description
        self._encrypted = encrypted

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

#Returns a readable text version of the asset. If encrypted, '[Encrypted]' appears at the end.
    def __str__(self):
        base = f"{self._name}: {self._description}"
        return f"{base} [Encrypted]" if self._encrypted else base
