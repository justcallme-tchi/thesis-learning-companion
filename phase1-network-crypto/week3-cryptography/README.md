# W3 — Cryptography Fundamentals
**Jul 10 – Jul 16**

## Study topics
- AES: block cipher, ECB vs CBC vs GCM modes — why ECB leaks structure visually
- RSA: key pair generation, modular exponentiation, digital signatures
- SHA-256 + salts: rainbow tables, bcrypt/Argon2 vs plain SHA
- TLS 1.3 handshake: ClientHello → certificate → ECDHE → session key
- Pass-the-hash (PTH): NTLM capture, lateral movement via SMB
- SSL stripping / HSTS bypass

## Lab deliverables
- [ ] Python crypto lab: hashlib.sha256 + salt → `scripts/hash_demo.py`
- [ ] ECB penguin demo: AES-ECB vs AES-CBC on bitmap → `lab-outputs/ecb_vs_cbc.png`
- [ ] Wireshark TLS capture → `lab-outputs/tls_handshake.png`
- [ ] Weak hash detector script → `scripts/hash_cracker.py`

## Key insight for thesis
The ECB penguin experiment is the theoretical basis for MalImg:
data structure is preserved in naive encryption AND in raw byte layout.
This is why malware binary visualization works as a classification method.

## Resources
- CryptoHack: https://cryptohack.org
- TLS 1.3 illustrated: https://tls13.xargs.org
- PyCryptodome: https://pycryptodome.readthedocs.io
