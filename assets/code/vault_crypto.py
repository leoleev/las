#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vault_crypto.py - 加密保险库辅助脚本（可选项，默认不启用）

加密算法：
- 对称加密：AES-256-GCM（保密 + 完整性）
- 密钥派生：PBKDF2-HMAC-SHA256（由用户 passphrase 派生密钥，不可逆）
- 凭证：用户掌握的「钥匙包」(passphrase / .keybag)，沙箱内不留存

依赖：pip install cryptography

重要：
- 本脚本仅用于离线生成/解密密文条目，方便把明文变成附录 C 的密文格式。
- AI 读取密钥时，按附录 C.3 协议：必须现场向用户索取 passphrase，仅本次会话内存使用，
  用完即弃，不得写入 memory/日志/任何持久文件，也不得后续复述。
- 钥匙包丢失 = 数据永久不可恢复，务必本地备份。
"""
import argparse
import base64
import json
import os
import sys

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
except ImportError:
    sys.stderr.write("[错误] 缺少依赖 cryptography，请先运行: pip install cryptography\n")
    sys.exit(2)

KDF_ITER = 600_000
SALT_BYTES = 16
NONCE_BYTES = 12


def _derive_key(passphrase: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=KDF_ITER)
    return kdf.derive(passphrase.encode("utf-8"))


def encrypt_secret(passphrase: str, plaintext: str) -> dict:
    salt = os.urandom(SALT_BYTES)
    key = _derive_key(passphrase, salt)
    nonce = os.urandom(NONCE_BYTES)
    ct = AESGCM(key).encrypt(nonce, plaintext.encode("utf-8"), None)
    return {
        "algo": "AES-256-GCM+PBKDF2",
        "kdf_iter": KDF_ITER,
        "salt": base64.b64encode(salt).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "cipher": base64.b64encode(ct).decode(),
    }


def decrypt_secret(passphrase: str, entry: dict) -> str:
    salt = base64.b64decode(entry["salt"])
    nonce = base64.b64decode(entry["nonce"])
    ct = base64.b64decode(entry["cipher"])
    key = _derive_key(passphrase, salt)
    pt = AESGCM(key).decrypt(nonce, ct, None)
    return pt.decode("utf-8")


def entry_to_markdown(entry_id: str, key_ref: str, entry: dict) -> str:
    return (
        f"## {entry_id}\n"
        f"- algo: {entry['algo']}\n"
        f"- kdf_iter: {entry['kdf_iter']}\n"
        f"- salt: {entry['salt']}\n"
        f"- nonce: {entry['nonce']}\n"
        f"- cipher: {entry['cipher']}\n"
        f"- key_ref: {key_ref}\n"
    )


def main():
    ap = argparse.ArgumentParser(description="加密保险库辅助（AES-256-GCM+PBKDF2）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_enc = sub.add_parser("encrypt", help="加密一条明文，输出密文条目（JSON / Markdown）")
    p_enc.add_argument("--id", required=True, help="条目名，如 github_token")
    p_enc.add_argument("--key-ref", required=True, help="钥匙包标识，如 keybag_main")
    p_enc.add_argument("--passphrase", required=True, help="用户钥匙包 passphrase（现场提供，勿留痕）")
    p_enc.add_argument("--plaintext", required=True, help="要加密的明文")
    p_enc.add_argument("--format", choices=["json", "md"], default="md")

    p_dec = sub.add_parser("decrypt", help="解密一条密文条目（需现场提供 passphrase）")
    p_dec.add_argument("--passphrase", required=True, help="用户钥匙包 passphrase")
    p_dec.add_argument("--json", required=True, help="密文条目 JSON 字符串")

    args = ap.parse_args()

    if args.cmd == "encrypt":
        entry = encrypt_secret(args.passphrase, args.plaintext)
        if args.format == "json":
            print(json.dumps({"id": args.id, "key_ref": args.key_ref, **entry}, ensure_ascii=False, indent=2))
        else:
            print(entry_to_markdown(args.id, args.key_ref, entry), end="")
    elif args.cmd == "decrypt":
        entry = json.loads(args.json)
        try:
            print(decrypt_secret(args.passphrase, entry))
        except Exception:
            sys.stderr.write("[失败] 解密错误：passphrase 错误或数据损坏\n")
            sys.exit(1)


if __name__ == "__main__":
    main()
