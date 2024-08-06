"""
Rust-like trait system.
"""
from typing import Self, TypeGuard


class Trait:
    @classmethod
    def is_(cls, obj: object) -> TypeGuard[Self]:
        raise NotImplementedError
