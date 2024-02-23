"""
Cryptographic operations.

For password hashing uses bcrypt, which has the salt saved into the hash
itself.

See password hashing https://stackoverflow.com/a/23768422/14748231
"""
import bcrypt


class CryptoUtils:
    @classmethod
    def hash_password(
        cls,
        plain_password_bytes: bytes,
    ) -> bytes:
        return bcrypt.hashpw(
            plain_password_bytes,
            bcrypt.gensalt(12),
        )

    @classmethod
    def check_password(
        cls,
        plain_password_bytes: bytes,
        hashed_password_bytes: bytes,
    ) -> bool:
        return bcrypt.checkpw(
            plain_password_bytes,
            hashed_password_bytes,
        )
