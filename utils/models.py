from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class Model:
    id: str
    input_cost: float
    output_cost: float


class CLAUDE(Enum):
    OPUS = Model(id="claude-3-opus-20240229", input_cost=15, output_cost=75)
    SONNET = Model(id="claude-3-sonnet-20240229", input_cost=3, output_cost=15)
    HAIKU = Model(id="claude-3-haiku-20240307", input_cost=0.25, output_cost=1.25)
