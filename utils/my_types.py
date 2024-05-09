from dataclasses import dataclass


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
