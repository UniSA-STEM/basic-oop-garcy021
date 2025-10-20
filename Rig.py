"""
File: Rig.py
Description: Implements the Rig class representing a hacker’s workstation, managing storage, upgrades, and durability.
Author: CHIRAG GARG
ID: 110395864
Username: GARCY021
This is my own work as defined by the University's Academic Misconduct Policy.
"""

from Asset import Asset

"""
   Represents a hacker's rig — their digital workstation.
   Handles storage, upgrades, durability, and asset management.
"""

class Rig:
    def __init__(self, name):
        self._name = name  # Name of the rig
        self._damage = 0    # Tracks damage level; when threshold reached, rig breaks
        self._broken = False
        self._upgrade_level = 0
        self._storage = []     # Holds the assets stored in this rig
# Initial assets
        self._storage.append(Asset("Data Spike", "Offensive payload"))
        self._storage.append(Asset("Data Spike", "Offensive payload"))
        self._storage.append(Asset("Removable Drive", "Portable extraction media"))

    @property
    def name(self):
        return self._name

    @property
    def damage(self):
        return self._damage

    @property
    def broken(self):
        return self._broken

    @property
    def upgrade_level(self):
        return self._upgrade_level

    @property
    def storage(self):
        # returns the actual list (assignment expects simple interactions)
        return self._storage


    def _capacity(self):
        # base capacity 5, +3 per upgrade level
        return 5 + self._upgrade_level * 3

    def _break_threshold(self):
        # base break threshold 2, +1 per upgrade level
        return 2 + self._upgrade_level

    def condition(self):    #Return readable damage state of the rig.
        if self._broken:
            state = "Broken"
        elif self._damage == 0:
            state = "Pristine"
        else:
            state = "Worn"
        return f"{state} (Level {self._upgrade_level})"

    def __str__(self):  #Readable description of the rig and its stored assets.
        assets = ", ".join(a.name + ("[E]" if a.encrypted else "") for a in self._storage) or "Empty"
        return f"Rig<{self._name}> {self.condition()} | Stored: {assets}"

    def take_hit(self): #Apply one hit to the rig. If damage reaches threshold, rig becomes broken.
        if self._broken:
            return
        self._damage += 1
        if self._damage >= self._break_threshold():
            self._broken = True

    def repair(self, token_available): #Repair the rig using a CryptoToken (token_available True if caller will consume token).
        #Returns True if repaired; False if no token or no repair needed.
        if not token_available:
            return False
        # if not damaged and not broken, no repair needed (print per spec)
        if self._damage == 0 and not self._broken:
            print("No repair needed.")
            return False
        self._damage = 0
        self._broken = False
        return True

    def upgrade(self, has_patch):
        """
        Upgrade the rig using a Hardware Patch (has_patch True if caller consumes it).
        Returns True on success, False if no patch supplied.
        """
        if not has_patch:
            return False
        self._upgrade_level += 1
        return True

    def can_store(self, asset):
        """Return True if the rig has capacity to accept one more asset."""
        return len(self._storage) < self._capacity()

    def store(self, asset):
        """
        Store an asset in the rig if capacity allows.
        Encrypted assets are allowed to be stored but cannot be released until decrypted.
        """
        if not self.can_store(asset):
            return False
        self._storage.append(asset)
        return True

    def release(self, name=None):  # Release assets out of the rig into a hacker's inventory.
        if name is None:
            movable = [a for a in self._storage if not a.encrypted]
            # keep only encrypted assets in storage
            self._storage = [a for a in self._storage if a.encrypted]
            return movable

        for i, a in enumerate(self._storage):
            if a.name.lower() == name.lower():
                if a.encrypted:
                    return []
                return [self._storage.pop(i)]
        return []

    def unsecured_assets(self): #Return list of unencrypted assets without removing them.
        return [a for a in self._storage if not a.encrypted]
