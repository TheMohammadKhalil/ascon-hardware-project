import ascon
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT_DIR = BASE / "test_vectors"
OUT_DIR.mkdir(exist_ok=True)

vectors = [
    {
        "id": "V1",
        "key": bytes.fromhex("000102030405060708090a0b0c0d0e0f"),
        "nonce": bytes.fromhex("101112131415161718191a1b1c1d1e1f"),
        "ad": b"",
        "plaintext": b"",
        "hash_msg": b""
    },
    {
        "id": "V2",
        "key": bytes.fromhex("000102030405060708090a0b0c0d0e0f"),
        "nonce": bytes.fromhex("101112131415161718191a1b1c1d1e1f"),
        "ad": b"AD",
        "plaintext": b"Hello",
        "hash_msg": b"Hello"
    },
    {
        "id": "V3",
        "key": bytes.fromhex("00112233445566778899aabbccddeeff"),
        "nonce": bytes.fromhex("ffeeddccbbaa99887766554433221100"),
        "ad": b"header",
        "plaintext": b"ASCON hardware test",
        "hash_msg": b"ASCON hardware test"
    },
    {
        "id": "V4",
        "key": bytes.fromhex("0f0e0d0c0b0a09080706050403020100"),
        "nonce": bytes.fromhex("00102030405060708090a0b0c0d0e0f0"),
        "ad": b"course",
        "plaintext": b"hardware security project",
        "hash_msg": b"hardware security project"
    },
    {
        "id": "V5",
        "key": bytes.fromhex("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"),
        "nonce": bytes.fromhex("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"),
        "ad": b"associated data",
        "plaintext": b"test vector number five",
        "hash_msg": b"test vector number five"
    }
]

rows = []

for v in vectors:
    ciphertext = ascon.encrypt(
    v["key"],
    v["nonce"],
    v["ad"],
    v["plaintext"],
    variant="Ascon-128"
)

    decrypted = ascon.decrypt(
    v["key"],
    v["nonce"],
    v["ad"],
    ciphertext,
    variant="Ascon-128"
)

    digest = ascon.hash(
    v["hash_msg"],
    variant="Ascon-Hash",
    hashlength=32
)

    if decrypted != v["plaintext"]:
        raise RuntimeError(f"Decryption failed for {v['id']}")

    rows.append({
        "id": v["id"],
        "key_hex": v["key"].hex(),
        "nonce_hex": v["nonce"].hex(),
        "ad_hex": v["ad"].hex(),
        "plaintext_hex": v["plaintext"].hex(),
        "ciphertext_tag_hex": ciphertext.hex(),
        "decrypted_hex": decrypted.hex(),
        "hash_msg_hex": v["hash_msg"].hex(),
        "hash256_hex": digest.hex()
    })

txt_path = OUT_DIR / "test_vectors.txt"
csv_path = OUT_DIR / "test_vectors.csv"
hex_path = OUT_DIR / "test_vectors_for_tb.hex"

with txt_path.open("w") as f:
    for r in rows:
        f.write(
            f"{r['id']}: "
            f"KEY={r['key_hex']}, "
            f"NONCE={r['nonce_hex']}, "
            f"AD={r['ad_hex']}, "
            f"PT={r['plaintext_hex']}, "
            f"CT_TAG={r['ciphertext_tag_hex']}, "
            f"HASH_IN={r['hash_msg_hex']}, "
            f"HASH256={r['hash256_hex']}\n"
        )

with csv_path.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

with hex_path.open("w") as f:
    for r in rows:
        f.write(f"{r['key_hex']} {r['nonce_hex']} {r['ad_hex']} {r['plaintext_hex']} {r['ciphertext_tag_hex']} {r['hash256_hex']}\n")

print(f"Generated: {txt_path}")
print(f"Generated: {csv_path}")
print(f"Generated: {hex_path}")
print()
for r in rows:
    print(r["id"])
    print("KEY:     ", r["key_hex"])
    print("NONCE:   ", r["nonce_hex"])
    print("AD:      ", r["ad_hex"])
    print("PT:      ", r["plaintext_hex"])
    print("CT+TAG:  ", r["ciphertext_tag_hex"])
    print("HASH256: ", r["hash256_hex"])
    print()
