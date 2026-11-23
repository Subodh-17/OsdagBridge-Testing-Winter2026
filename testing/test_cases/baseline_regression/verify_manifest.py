"""
Independent Manifest and Seal Verifier for OsdagBridge Evidence Trees
Workspace: F:\\FOSSEE internship

Fails closed if the external seal is missing, corrupted, forged, or inapplicable.
Verifies:
1. Trust anchor and HMAC-SHA256 signing key are present and accessible outside the workspace.
2. Trusted run seal exists in external storage and HMAC signature is mathematically valid.
3. Disk manifest matches seal SHA-256 with 100% parity.
4. Complete directory walk: flags unlisted files (S8), missing files (S9), and byte/hash mismatches (S1-S3).

Returns exit code 0 if 100% authentic, 1 on any discrepancy, tamper, or missing seal.
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evidence_guard import verify_manifest_integrity, sha256_file, get_trust_dir, PINNED_TRUST_DIR


def main():
    parser = argparse.ArgumentParser(description="Independent Evidence Manifest & Seal Verifier")
    parser.add_argument("evidence_dir", help="Path to evidence directory containing manifest_hashes.json")
    parser.add_argument("--trust-dir", default=None, help="Path to external trust store directory")
    parser.add_argument("--allow-unpinned-trust-dir", action="store_true", default=False,
                        help="Explicit flag required to use an unpinned trust store override")
    args = parser.parse_args()

    evidence_dir = os.path.realpath(os.path.abspath(args.evidence_dir))
    trust_override = args.trust_dir or os.environ.get("OSDAGBRIDGE_TRUST_DIR")

    if trust_override:
        norm_override = os.path.realpath(os.path.abspath(str(trust_override).strip()))
        if norm_override != PINNED_TRUST_DIR and not args.allow_unpinned_trust_dir:
            print(f"\n[CRITICAL FAILURE] TRUST ANCHOR PINNING VIOLATION (FAIL-CLOSED):")
            print(f"  Unpinned trust directory requested: {norm_override}")
            print(f"  Pinned official trust directory:    {PINNED_TRUST_DIR}")
            print(f"  To use an unpinned directory for isolated testing, pass --allow-unpinned-trust-dir.")
            sys.exit(1)
        if norm_override != PINNED_TRUST_DIR:
            print(f"[SECURITY WARNING] Running with UNPINNED trust directory override: {norm_override}")

    trust_dir = args.trust_dir or get_trust_dir(allow_override=args.allow_unpinned_trust_dir)

    print("=" * 80)
    print("INDEPENDENT EVIDENCE MANIFEST & CRYPTOGRAPHIC SEAL VERIFICATION")
    print(f"Target Directory: {evidence_dir}")
    print(f"Trust Store:      {trust_dir}")
    print("=" * 80)

    success, mismatches, details = verify_manifest_integrity(
        evidence_dir,
        trust_dir=trust_dir,
        allow_trust_override=args.allow_unpinned_trust_dir
    )

    if not success:
        print("\n[CRITICAL FAILURE] VERIFICATION REJECTED (FAIL-CLOSED):")
        for m in mismatches:
            print(f"  - {m}")
        print(f"\nDetails: {details}")
        sys.exit(1)

    print(f"\n[PASS] External Cryptographic Run Seal: VALID")
    print(f"[SUCCESS] {details}")
    print("Zero drift detected. All evidence is authentic, tamper-free, and cryptographically verified.")
    sys.exit(0)


if __name__ == "__main__":
    main()
