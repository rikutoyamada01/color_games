class PixelStrip:
    def __init__(self, num_leds, pin, freq_hz=800000, dma=10, invert=False, brightness=255, channel=0):
        """
        Mock implementation of the PixelStrip class.
        :param num_leds: Number of LEDs in the strip.
        :param pin: GPIO pin connected to the strip.
        :param freq_hz: LED signal frequency (default 800kHz).
        :param dma: DMA channel to use (default 10).
        :param invert: Invert the signal (default False).
        :param brightness: Brightness level (0-255).
        :param channel: PWM channel (default 0).
        """
        self.num_leds = num_leds
        self.pin = pin
        self.leds = [(0, 0, 0)] * num_leds  # Store LED colors as RGB tuples
        self.brightness = brightness
        print(f"Mock PixelStrip initialized with {num_leds} LEDs on pin {pin}.")

    def begin(self):
        """Mock method to initialize the LED strip."""
        print("Mock PixelStrip: begin() called.")

    def setPixelColor(self, n, color):
        """
        Mock method to set the color of a specific LED.
        :param n: LED index.
        :param color: Color as an integer (converted from RGB).
        """
        if 0 <= n < self.num_leds:
            self.leds[n] = color
            """print(f"Mock PixelStrip: LED {n} set to color {color}.")"""
        else:
            print(f"Mock PixelStrip: Invalid LED index {n}.")

    def show(self):
        """Mock method to display the current LED colors."""
        """print("Mock PixelStrip: show() called. Current LED states:")"""
        for i, color in enumerate(self.leds):
            """print(f"  LED {i}: {color}")"""
            pass

    def setBrightness(self, brightness):
        """
        Mock method to set the brightness of the strip.
        :param brightness: Brightness level (0-255).
        """
        self.brightness = brightness
        """print(f"Mock PixelStrip: Brightness set to {brightness}.")"""

    def getBrightness(self):
        """Mock method to get the current brightness level."""
        return self.brightness


def Color(red, green, blue):
    """
    Mock function to convert RGB values to a single integer.
    :param red: Red component (0-255).
    :param green: Green component (0-255).
    :param blue: Blue component (0-255).
    :return: A tuple representing the RGB color.
    """
    """print(f"Mock Color: ({red}, {green}, {blue}) created.")"""
    return (red, green, blue)
