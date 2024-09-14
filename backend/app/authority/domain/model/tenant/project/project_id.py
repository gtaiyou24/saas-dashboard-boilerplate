from dataclasses import dataclass


@dataclass(init=False, unsafe_hash=True, frozen=True)
class ProjectId:
    value: str

    def __init__(self, value: str):
        assert value, "プロジェクトIDは必須です。"
        super().__setattr__("value", value)
