from __future__ import annotations

import time

import serial
from serial.tools import list_ports


class PicoConnection:
    def __init__(self, baudrate: int = 115200):
        self.baudrate = baudrate
        self.serial: serial.Serial | None = None

        self.last_values: list[int] | None = None

        self.last_scan = 0.0
        self.scan_interval = 1.0

    @property
    def connected(self) -> bool:
        return (
            self.serial is not None
            and self.serial.is_open
        )

    def find_pico(self) -> str | None:
        for port in list_ports.comports():
            description = (
                f"{port.description} "
                f"{port.manufacturer or ''} "
                f"{port.product or ''}"
            ).lower()

            if any(
                keyword in description
                for keyword in (
                    "pico",
                    "rp2040",
                    "raspberry",
                    "usb serial",
                )
            ):
                return port.device

        return None

    def try_connect(self) -> bool:
        if self.connected:
            return True

        now = time.monotonic()

        if now - self.last_scan < self.scan_interval:
            return False

        self.last_scan = now

        port = self.find_pico()

        if port is None:
            return False

        try:
            self.serial = serial.Serial(
                port=port,
                baudrate=self.baudrate,
                timeout=0.1,
            )

            print(f"Pico connected: {port}")

            # Force le premier envoi.
            self.last_values = None

            return True

        except serial.SerialException:
            self.serial = None
            return False

    def send(self, values: list[float]) -> None:
        if not self.connected:
            self.try_connect()

        if not self.connected:
            return

        integer_values = [
            max(0, min(180, round(value)))
            for value in values
        ]

        # Évite de spammer le Pico.
        if self.last_values == integer_values:
            return

        message = ",".join(
            str(value)
            for value in integer_values
        )

        message += "\n"

        try:
            self.serial.write(
                message.encode("ascii")
            )

            self.last_values = integer_values

        except serial.SerialException:
            self.disconnect()

    def disconnect(self) -> None:
        if self.serial is not None:
            try:
                self.serial.close()
            except Exception:
                pass

        self.serial = None