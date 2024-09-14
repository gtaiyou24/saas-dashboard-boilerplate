from dataclasses import dataclass


@dataclass(init=False, unsafe_hash=True, frozen=True)
class TenantId:
    value: str

    def __init__(self, value: str):
        assert value, "テナントIDは必須です。"
        super().__setattr__("value", value)
