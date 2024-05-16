from dataclasses import dataclass
from typing import TypedDict


@dataclass
class Page:
    number: str
    content: list[str]


@dataclass
class Book:
    id: str
    author: str
    title: str
    pages: list[Page]


@dataclass(frozen=True)
class Model:
    name: str
    provider: str
    id: str
    input_cost: float
    output_cost: float


class Message(TypedDict):
    role: str
    content: str
