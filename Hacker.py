"""
File: Hacker.py
Description: <A brief description of this Python module.>
Author: <full name>
ID: <student_id>
Username: <username>
This is my own work as defined by the University's Academic Misconduct Policy.
"""

from Asset import Asset
from Rig import Rig

TRACE_THRESHOLD = 5  # risky actions blocked at or above this


# ----- small helpers (kept private by convention) -----
def _take_first_by_name(items, name):
    """Remove and return the first asset with the given name (case-insensitive), or None if absent."""
    for i, a in enumerate(items):
        if a.name.lower() == name.lower():
            return items.pop(i)
    return None


def _find_asset(items, name):
    """Return the first asset with the given name (case-insensitive) without removing it."""
    for a in items:
        if a.name.lower() == name.lower():
            return a
    return None


class Hacker:
    """
    Hacker: manages inventory, rig, trace, combat, and asset operations.
    """

    def __init__(self, name):
        self._name = name
        self._inventory = [Asset("CryptoToken", "Currency for rigs and repairs")]
        self._rig = None
        self._trace_level = 0

    # ----- Properties -----
    @property
    def name(self):
        return self._name

    @property
    def rig(self):
        return self._rig

    @property
    def trace_level(self):
        return self._trace_level

    @property
    def inventory(self):
        return self._inventory

    @property
    def exposed(self):
        """True when risky actions should be blocked due to high trace."""
        return self._trace_level >= TRACE_THRESHOLD

    # ----- Display -----
    def __str__(self):
        inv = ", ".join(a.name + ("[E]" if a.encrypted else "") for a in self._inventory) or "Empty"
        rig_name = self._rig.name if self._rig else "No Rig"
        return f"Hacker<{self._name}> | Rig: {rig_name} | Trace: {self._trace_level} | Inv: {inv}"

    # ----- Trace helpers -----
    def _risky_allowed(self):
        return self._trace_level < TRACE_THRESHOLD

    def _add_trace(self, n=1):
        self._trace_level += n

    def reduce_trace(self, n=1):
        self._trace_level = max(0, self._trace_level - n)

    # ----- Core actions -----
    def acquire_rig(self, rig=None):
        """Spend one CryptoToken to attach a rig (create one if not provided)."""
        token = _take_first_by_name(self._inventory, "CryptoToken")
        if not token:
            return False
        if rig is None:
            rig = Rig(f"{self._name}'s Rig")
        self._rig = rig
        print(f"[{self._name}] Rig '{rig.name}' activated.")
        return True

    def launch_data_spike(self, target):
        """
        Launch a Data Spike at target's rig.
        Requires both rigs, consumes 1 Data Spike, damages target, adds +1 trace.
        """
        if not self._rig or not target.rig:
            return False
        if not self._risky_allowed():
            return False
        spike = _take_first_by_name(self._rig.storage, "Data Spike")
        if not spike:
            return False
        target.rig.take_hit()
        self._add_trace(1)
        return True

    def extract_unsecured_from(self, target):
        """
        If target.rig is broken and attacker has a Removable Drive in their rig (consumed),
        move all UNENCRYPTED assets from target rig into this hacker's inventory.
        """
        if not self._rig or not target.rig or not target.rig.broken:
            return False
        if not self._risky_allowed():
            return False

        # consume Removable Drive from attacker's rig storage
        drive = _take_first_by_name(self._rig.storage, "Removable Drive")
        if not drive:
            return False

        movable = target.rig.release(name=None)  # unencrypted only
        for a in movable:
            self._inventory.append(a)

        if movable:
            self._add_trace(1)
            return True
        return False

    # ----- Storage transfers -----
    def store_to_rig(self, asset_name=None, all_items=False):
        """Store one or all inventory items into the rig (if present and capacity allows)."""
        if not self._rig:
            return False
        if all_items:
            moved = False
            for a in list(self._inventory):
                if self._rig.can_store(a):
                    self._inventory.remove(a)
                    self._rig.store(a)
                    moved = True
            return moved

        if asset_name is None:
            return False
        asset = _take_first_by_name(self._inventory, asset_name)
        if not asset:
            return False
        if self._rig.store(asset):
            return True
        # put it back if store failed
        self._inventory.append(asset)
        return False

    def retrieve_from_rig(self, asset_name=None, all_items=False):
        """
        Retrieve one or all UNENCRYPTED assets from the rig into inventory.
        Adds +1 trace if any 'sensitive' assets moved.
        """
        if not self._rig:
            return False
        released = self._rig.release(None if all_items else asset_name)
        if not released:
            return False
        for a in released:
            self._inventory.append(a)

        # basic 'sensitive' rule (tweak as needed for your spec)
        if any(a.name not in {"CryptoToken", "Data Spike", "Removable Drive", "Security Chip", "Hardware Patch"}
               for a in released):
            if self._risky_allowed():
                self._add_trace(1)
        return True

    # ----- Encryption (consumes a Security Chip if available) -----
    def _consume_security_chip(self):
        # try inventory first, then rig storage
        chip = _take_first_by_name(self._inventory, "Security Chip")
        if chip:
            return True, "inventory"
        if self._rig:
            chip = _take_first_by_name(self._rig.storage, "Security Chip")
            if chip:
                return True, "rig"
        return False, ""

    def encrypt_asset(self, name, location="inventory"):
        ok, _ = self._consume_security_chip()
        if not ok:
            return False
        if location == "inventory":
            target_list = self._inventory
        elif location == "rig" and self._rig:
            target_list = self._rig.storage
        else:
            return False
        asset = _find_asset(target_list, name)
        if not asset or asset.encrypted:
            return False
        asset.encrypted = True
        return True

    def decrypt_asset(self, name, location="inventory"):
        ok, _ = self._consume_security_chip()
        if not ok:
            return False
        if location == "inventory":
            target_list = self._inventory
        elif location == "rig" and self._rig:
            target_list = self._rig.storage
        else:
            return False
        asset = _find_asset(target_list, name)
        if not asset or not asset.encrypted:
            return False
        asset.encrypted = False
        return True

    # ----- Wrappers for rig upgrade/repair -----
    def upgrade_rig(self):
        if not self._rig:
            return False
        patch = _take_first_by_name(self._inventory, "Hardware Patch")
        if not patch:
            return False
        return self._rig.upgrade(has_patch=True)

    def repair_rig(self):
        if not self._rig:
            return False
        token = _take_first_by_name(self._inventory, "CryptoToken")
        if not token:
            return False
        return self._rig.repair(token_available=True)

    # ----- Utility -----
    def scan_inventory(self, name):
        """Remove and return the first matching asset from inventory, or None."""
        for i, a in enumerate(self._inventory):
            if a.name.lower() == name.lower():
                return self._inventory.pop(i)
        return None
