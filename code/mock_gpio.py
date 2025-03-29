from typing import Dict, Optional

class MockGPIO:
    # Constants
    BCM: str = "BCM"
    BOARD: str = "BOARD"
    IN: str = "IN"
    OUT: str = "OUT"
    PUD_UP: str = "PUD_UP"
    PUD_DOWN: str = "PUD_DOWN"

    # Class-level attributes
    mode: Optional[str] = None
    pins: Dict[int, Dict[str, Optional[bool]]] = {}

    @classmethod
    def setmode(cls, mode: str) -> None:
        """Set the pin numbering mode."""
        cls.mode = mode
        print(f"GPIO mode set to {mode}")

    @classmethod
    def setup(cls, pin: int, mode: str, pull_up_down: Optional[str] = None) -> None:
        """Configure a pin as input or output."""
        cls.pins[pin] = {"mode": mode, "state": True, "pull": pull_up_down}
        print(f"Pin {pin} set up as {mode} with pull {pull_up_down}")

    @classmethod
    def input(cls, pin: int) -> bool:
        """Read the state of an input pin."""
        return cls.pins.get(pin, {}).get("state", True)

    @classmethod
    def output(cls, pin: int, state: bool) -> None:
        """Set the state of an output pin."""
        if pin in cls.pins and cls.pins[pin]["mode"] == cls.OUT:
            cls.pins[pin]["state"] = state
        else:
            print(f"Error: Pin {pin} is not configured as output")

    @classmethod
    def cleanup(cls) -> None:
        """Reset all GPIO pins."""
        cls.pins.clear()
        print("GPIO cleanup complete")
