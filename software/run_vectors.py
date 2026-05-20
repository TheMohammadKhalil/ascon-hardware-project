import ascon
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CSV_PATH = BASE / "test_vectors" / "test_vectors.csv"

passed = 0
failed = 0

with CSV_PATH.open() as f:
    reader = csv.DictReader(f)

    for row in reader:
        key = bytes.fromhex(row["key_hex"])
        nonce = bytes.fromhex(row["nonce_hex"])
        ad = bytes.fromhex(row["ad_hex"])
        plaintext = bytes.fromhex(row["plaintext_hex"])
        expected_ct_tag = bytes.fromhex(row["ciphertext_tag_hex"])
        hash_msg = bytes.fromhex(row["hash_msg_hex"])
        expected_hash = bytes.fromhex(row["hash256_hex"])

        actual_ct_tag = ascon.encrypt(
            key,
            nonce,
            ad,
            plaintext,
            variant="Ascon-128"
        )

        actual_pt = ascon.decrypt(
            key,
            nonce,
            ad,
            actual_ct_tag,
            variant="Ascon-128"
        )

        actual_hash = ascon.hash(
            hash_msg,
            variant="Ascon-Hash",
            hashlength=32
        )

        enc_ok = actual_ct_tag == expected_ct_tag
        dec_ok = actual_pt == plaintext
        hash_ok = actual_hash == expected_hash

        print("=" * 70)
        print(f"Vector: {row['id']}")
        print(f"Encryption match: {enc_ok}")
        print(f"Decryption match: {dec_ok}")
        print(f"Hash match:       {hash_ok}")

        if enc_ok and dec_ok and hash_ok:
            print("RESULT: PASS")
            passed += 1
        else:
            print("RESULT: FAIL")
            failed += 1

print("=" * 70)
print(f"Total passed: {passed}")
print(f"Total failed: {failed}")

if failed != 0:
    raise SystemExit(1)
