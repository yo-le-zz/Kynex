from __future__ import annotations

import math
from dataclasses import dataclass


def distance(a, b) -> float:
    return math.sqrt(
        (a.x - b.x) ** 2
        + (a.y - b.y) ** 2
        + (a.z - b.z) ** 2
    )


def angle(a, b, c) -> float:
    """
    Angle ABC en degrés.
    """

    ba = (
        a.x - b.x,
        a.y - b.y,
        a.z - b.z,
    )

    bc = (
        c.x - b.x,
        c.y - b.y,
        c.z - b.z,
    )

    dot = (
        ba[0] * bc[0]
        + ba[1] * bc[1]
        + ba[2] * bc[2]
    )

    magnitude_ba = math.sqrt(
        ba[0] ** 2
        + ba[1] ** 2
        + ba[2] ** 2
    )

    magnitude_bc = math.sqrt(
        bc[0] ** 2
        + bc[1] ** 2
        + bc[2] ** 2
    )

    if magnitude_ba == 0 or magnitude_bc == 0:
        return 180.0

    cosine = dot / (magnitude_ba * magnitude_bc)

    cosine = max(-1.0, min(1.0, cosine))

    return math.degrees(math.acos(cosine))


@dataclass
class FingerAngles:
    mcp: float
    pip: float
    dip: float


@dataclass
class HandAngles:
    thumb: FingerAngles
    index: FingerAngles
    middle: FingerAngles
    ring: FingerAngles
    pinky: FingerAngles


def calculate_angles(landmarks) -> HandAngles:
    """
    MediaPipe landmarks:

    Thumb:
        1, 2, 3, 4

    Index:
        5, 6, 7, 8

    Middle:
        9, 10, 11, 12

    Ring:
        13, 14, 15, 16

    Pinky:
        17, 18, 19, 20
    """

    # Pour les doigts classiques :
    #
    # MCP = articulation proche de la main
    # PIP = articulation centrale
    # DIP = articulation proche du bout du doigt

    index = FingerAngles(
        mcp=angle(0, 5, 6),
        pip=angle(5, 6, 7),
        dip=angle(6, 7, 8),
    )

    middle = FingerAngles(
        mcp=angle(0, 9, 10),
        pip=angle(9, 10, 11),
        dip=angle(10, 11, 12),
    )

    ring = FingerAngles(
        mcp=angle(0, 13, 14),
        pip=angle(13, 14, 15),
        dip=angle(14, 15, 16),
    )

    pinky = FingerAngles(
        mcp=angle(0, 17, 18),
        pip=angle(17, 18, 19),
        dip=angle(18, 19, 20),
    )

    # Le pouce n'a pas réellement MCP/PIP/DIP comme les autres doigts.
    #
    # On conserve néanmoins trois valeurs pour notre architecture
    # robotique actuelle.
    #
    # Elles représentent trois degrés de flexion utiles au modèle
    # robotique du pouce.

    thumb = FingerAngles(
        mcp=angle(0, 1, 2),
        pip=angle(1, 2, 3),
        dip=angle(2, 3, 4),
    )

    return HandAngles(
        thumb=thumb,
        index=index,
        middle=middle,
        ring=ring,
        pinky=pinky,
    )


def flatten_angles(hand: HandAngles) -> list[float]:
    return [
        hand.thumb.mcp,
        hand.thumb.pip,
        hand.thumb.dip,

        hand.index.mcp,
        hand.index.pip,
        hand.index.dip,

        hand.middle.mcp,
        hand.middle.pip,
        hand.middle.dip,

        hand.ring.mcp,
        hand.ring.pip,
        hand.ring.dip,

        hand.pinky.mcp,
        hand.pinky.pip,
        hand.pinky.dip,
    ]


def rebuild_angles(values: list[float]) -> HandAngles:
    return HandAngles(
        thumb=FingerAngles(*values[0:3]),
        index=FingerAngles(*values[3:6]),
        middle=FingerAngles(*values[6:9]),
        ring=FingerAngles(*values[9:12]),
        pinky=FingerAngles(*values[12:15]),
    )


class AngleFilter:
    def __init__(
        self,
        smoothing: float = 0.25,
        deadzone: float = 1.0,
        max_change: float = 8.0,
    ):
        self.smoothing = smoothing
        self.deadzone = deadzone
        self.max_change = max_change

        self.previous: list[float] | None = None

    def update(self, values: list[float]) -> list[float]:
        if self.previous is None:
            self.previous = values.copy()
            return values.copy()

        result = []

        for old, new in zip(self.previous, values):
            difference = new - old

            # Ignore les micros variations.
            if abs(difference) < self.deadzone:
                new = old

            # Limite la vitesse à laquelle une articulation
            # peut changer entre deux images.
            difference = new - old

            if difference > self.max_change:
                new = old + self.max_change

            elif difference < -self.max_change:
                new = old - self.max_change

            # Filtre exponentiel.
            filtered = (
                old * (1.0 - self.smoothing)
                + new * self.smoothing
            )

            result.append(filtered)

        self.previous = result

        return result