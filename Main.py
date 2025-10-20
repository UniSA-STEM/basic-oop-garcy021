"""
File: Main.py
Description: Runs the main simulation showcasing hacker interactions, encryption, upgrades, and edge.
Author: CHIRAG GARG
ID: 110395864
Username: GARCY021
This is my own work as defined by the University's Academic Misconduct Policy.
"""

from Hacker import Hacker
from Rig import Rig
from Asset import Asset


def divider(title):
    print("\n" + "=" * 10 + f" {title} " + "=" * 10)


def main():
    divider("Create hackers")
    neo = Hacker("NeoShade")
    trinity = Hacker("Trinity-404")
    print(neo)
    print(trinity)

    divider("Acquire rigs (consume CryptoToken)")
    neo.acquire_rig(Rig("Onyx-Frame"))
    trinity.inventory.append(Asset("CryptoToken", "Currency for rigs and repairs"))
    trinity.acquire_rig(Rig("Vanta-Node"))
    print(neo)
    print(trinity)

    divider("Rig storage & auto assets")
    print("Neo rig:", neo.rig)
    print("Trinity rig:", trinity.rig)

    #  Upgrade Neo's rig using Hardware Patch
    divider("Upgrade Neo's rig using Hardware Patch")
    neo.inventory.append(Asset("Hardware Patch", "Rig upgrade"))
    print("Upgrade success:", neo.upgrade_rig())
    print(neo.rig)

    # Store secret in Neo's rig and encrypt it
    divider("Store secret in Neo's rig and encrypt it")
    neo.inventory.append(Asset("Access Key", "Privileged credential"))
    neo.store_to_rig("Access Key")
    neo.inventory.append(Asset("Security Chip", "Encrypt/decrypt controller"))
    print("Encrypt in rig:", neo.encrypt_asset("Access Key", location="rig"))
    print(neo.rig)

    # Combat: Neo attacks Trinity until broken or trace threshold
    divider("Combat: Neo attacks Trinity until broken or trace threshold")
    while not trinity.rig.broken and neo.trace_level < 5:
        # replenish spikes as needed
        if not any(a.name == "Data Spike" for a in neo.rig.storage):
            neo.rig.store(Asset("Data Spike", "Offensive payload"))
        neo.launch_data_spike(trinity)
    print("Neo trace:", neo.trace_level)
    print("Trinity rig:", trinity.rig)

    # Extraction attempt (requires Trinity broken + Removable Drive)
    divider("Extraction attempt (requires Trinity broken + Removable Drive)")
    if not any(a.name == "Removable Drive" for a in neo.rig.storage):
        neo.rig.store(Asset("Removable Drive", "Portable extraction media"))
    print("Extraction success:", neo.extract_unsecured_from(trinity))
    print("Neo inventory after extraction:", ", ".join(a.name + ("[E]" if a.encrypted else "") for a in neo.inventory))

    # Repair Trinity's rig (consume CryptoToken)
    divider("Repair Trinity's rig (consume CryptoToken)")
    trinity.inventory.append(Asset("CryptoToken", "Currency"))
    print("Repair success:", trinity.repair_rig())
    print(trinity.rig)

    # Decrypt the Access Key in Neo's rig
    divider("Decrypt the Access Key in Neo's rig")
    neo.inventory.append(Asset("Security Chip", "Encrypt/decrypt controller"))
    print("Decrypt success:", neo.decrypt_asset("Access Key", location="rig"))
    print(neo.rig)

    divider("Edge cases from spec")

    # Try to upgrade without a rig
    no_rig_user = Hacker("NoRig")
    print("Upgrade without rig (expect False):", no_rig_user.upgrade_rig())

    # Encrypt without a Security Chip
    chipless = Hacker("Chipless")
    chipless.acquire_rig(Rig("BareRig"))
    chipless.inventory.append(Asset("Access Key", "Credential"))
    print("Encrypt without chip (expect False):", chipless.encrypt_asset("Access Key", location="inventory"))

    # Block risky action at high trace
    risky = Hacker("Risky")
    risky.acquire_rig(Rig("RiskRig"))
    victim = Hacker("Victim")
    victim.inventory.append(Asset("CryptoToken", "x"))
    victim.acquire_rig(Rig("VicRig"))
    # drive trace up
    while risky.trace_level < 5:
        risky.inventory.append(Asset("Sensitive Doc", "s"))
        risky.store_to_rig("Sensitive Doc")
        risky.retrieve_from_rig("Sensitive Doc")
    print("Risky exposed?", risky.exposed)
    print("Attack at high trace (expect False):", risky.launch_data_spike(victim))


if __name__ == "__main__":
    main()