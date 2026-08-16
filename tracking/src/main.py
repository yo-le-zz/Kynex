from __future__ import annotations

import subprocess
import time
from pathlib import Path

from calibration import Calibration
from hand_angles import (
    AngleFilter,
    HandAngles,
    calculate_angles,
    flatten_angles,
)
from hand_tracker import HandTracker
from pico import PicoConnection


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "hand_landmarker.task"


def clear_terminal() -> None:
    subprocess.run(
        ["clear"],
        check=False,
    )


def print_header(pico: PicoConnection) -> None:
    print("Kynex Hand Tracking")
    print("===================")
    print()
    print("Target hand: RIGHT")
    print()

    if pico.connected:
        print("Pico: CONNECTED")
    else:
        print("Pico: NOT CONNECTED")

    print()


def print_finger(
    name: str,
    mcp: float,
    pip: float,
    dip: float,
) -> None:
    print(f"{name}:")
    print(f"  MCP: {mcp:6.2f}°")
    print(f"  PIP: {pip:6.2f}°")
    print(f"  DIP: {dip:6.2f}°")
    print()


def print_hand(hand: HandAngles) -> None:
    print_finger(
        "Thumb",
        hand.thumb.mcp,
        hand.thumb.pip,
        hand.thumb.dip,
    )

    print_finger(
        "Index",
        hand.index.mcp,
        hand.index.pip,
        hand.index.dip,
    )

    print_finger(
        "Middle",
        hand.middle.mcp,
        hand.middle.pip,
        hand.middle.dip,
    )

    print_finger(
        "Ring",
        hand.ring.mcp,
        hand.ring.pip,
        hand.ring.dip,
    )

    print_finger(
        "Pinky",
        hand.pinky.mcp,
        hand.pinky.pip,
        hand.pinky.dip,
    )


def ask_calibration() -> bool:
    while True:
        answer = input(
            "Calibrate hand at startup? [Y/n]: "
        ).strip().lower()

        if answer in ("", "y", "yes", "o", "oui"):
            return True

        if answer in ("n", "no", "non"):
            return False

        print("Please answer Y or N.")


def calibrate(
    tracker: HandTracker,
    pico: PicoConnection,
) -> Calibration | None:
    print()
    print("Calibration")
    print("===========")
    print()
    print("Place your hand in the neutral position.")
    print("Keep it still...")
    print()

    samples: list[list[float]] = []

    start = time.monotonic()

    while time.monotonic() - start < 3.0:
        hand = tracker.get_right_hand()

        if hand is not None:
            angles = calculate_angles(hand)
            samples.append(flatten_angles(angles))

        time.sleep(0.01)

    if not samples:
        print("Calibration failed: right hand not detected.")
        return None

    count = len(samples)

    average = [
        sum(sample[index] for sample in samples) / count
        for index in range(len(samples[0]))
    ]

    calibration = Calibration(
        neutral=average
    )

    print("Calibration complete.")

    time.sleep(1)

    return calibration


def main() -> None:
    tracker = HandTracker(
        model_path=MODEL_PATH,
        camera_id=0,
    )

    pico = PicoConnection()

    angle_filter = AngleFilter(
        smoothing=0.25,
        deadzone=0.8,
        max_change=8.0,
    )

    try:
        tracker.start()

        clear_terminal()

        print("Kynex Hand Tracking")
        print("===================")
        print()
        print("Target hand: RIGHT")
        print()

        calibration_enabled = ask_calibration()

        calibration = None

        if calibration_enabled:
            calibration = calibrate(
                tracker,
                pico,
            )

        clear_terminal()

        while True:
            hand_landmarks = tracker.get_right_hand()

            # On tente régulièrement de connecter le Pico.
            pico.try_connect()

            if hand_landmarks is None:
                clear_terminal()

                print_header(pico)
                print("Right hand not detected.")

                time.sleep(0.03)
                continue

            raw_angles = calculate_angles(
                hand_landmarks
            )

            filtered_values = angle_filter.update(
                flatten_angles(raw_angles)
            )

            filtered_angles = HandAngles(
                thumb=raw_angles.thumb,
                index=raw_angles.index,
                middle=raw_angles.middle,
                ring=raw_angles.ring,
                pinky=raw_angles.pinky,
            )

            # Reconstruit les angles filtrés.
            from hand_angles import rebuild_angles

            filtered_angles = rebuild_angles(
                filtered_values
            )

            if calibration is not None:
                filtered_angles = calibration.apply(
                    filtered_angles
                )

            pico_values = flatten_angles(
                filtered_angles
            )

            pico.send(pico_values)

            clear_terminal()

            print_header(pico)

            print("Right hand detected.")
            print()

            print_hand(filtered_angles)

            time.sleep(0.01)

    except KeyboardInterrupt:
        print()
        print("Stopping Kynex...")

    finally:
        tracker.stop()
        pico.disconnect()


if __name__ == "__main__":
    main()