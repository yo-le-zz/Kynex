from __future__ import annotations

from dataclasses import dataclass

from hand_angles import (
    HandAngles,
    flatten_angles,
    rebuild_angles,
)


@dataclass
class Calibration:
    neutral: list[float]

    @classmethod
    def from_hand(cls, hand: HandAngles) -> "Calibration":
        return cls(
            neutral=flatten_angles(hand)
        )

    def apply(self, hand: HandAngles) -> HandAngles:
        current = flatten_angles(hand)

        # Pour l'instant on conserve les angles absolus.
        #
        # La calibration sert principalement de référence.
        #
        # La conversion exacte vers les servos sera affinée
        # lorsque nous aurons le mécanisme physique du doigt.

        calibrated = []

        for value, neutral in zip(current, self.neutral):
            difference = value - neutral

            # On transforme la différence en une valeur
            # exploitable pour la main robotique.
            calibrated.append(
                max(0.0, min(180.0, 90.0 + difference))
            )

        return rebuild_angles(calibrated)