"""Moduel for shared graphics xml elements."""

from pydantic_xml import attr, element

from transformer.utility.utility import BaseModel


class Coordinates(BaseModel):
    """Coordinate extension of BaseModel (+x and y)."""

    x: float = attr(default=20.0)
    y: float = attr(default=20.0)


class PositionGraphics(BaseModel, tag="graphics"):
    """Placeholder graphics for position."""

    dimension: Coordinates = element("dimension", default=Coordinates())
    position: Coordinates = element("position", default=Coordinates())


class OffsetGraphics(BaseModel, tag="graphics"):
    """Graphics extension of BaseModel (+offset, dimension, position)."""

    offset: Coordinates = element("offset", default=Coordinates())
