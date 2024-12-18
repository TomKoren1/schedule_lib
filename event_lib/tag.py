from dataclasses import dataclass

@dataclass
class Tag:
    id: str
    title: str
    description: str
    color: str
    background_color: str