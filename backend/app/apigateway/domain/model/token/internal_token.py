from dataclasses import dataclass


@dataclass(init=True, unsafe_hash=True, frozen=True)
class InternalToken:
    """内部通信用トークン

    詳細は、doc/INTERNAL_TOKEN.md を参照してください。
    """
    jwt: str
