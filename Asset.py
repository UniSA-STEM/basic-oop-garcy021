"""
File: Asset.py
Description: <A brief description of this Python module.>
Author: <full name>
ID: <student_id>
Username: <username>
This is my own work as defined by the University's Academic Misconduct Policy.
"""

from dataclasses import dataclass

@dataclass
class Asset:
    name: str
    description: str
    encrypted: bool = False

    def __str__(self) -> str:
        base = f"{self.name}: {self.description}"
        return f"{base} [Encrypted]" if self.encrypted else base
