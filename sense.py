from sense_hat import SenseHat

sense = SenseHat()

# Define some colours
g = (0, 255, 0) # Green
# Define some colours
B = (102, 51, 0)
b = (0, 0, 255)
S = (205,133,63)
P = (214, 34, 166)
W = (0, 0, 0)

# Set up where each colour will display
happy_plant = [
    W, W, W, W, W, W, W, W,
    W, W, W, P, W, W, W, W,
    W, W, P, S, P, W, W, W,
    W, W, W, P, W, W, W, W,
    W, W, W, g, W, W, W, W,
    W, B, B, B, B, B, W, W,
    W, W, B, B, B, W, W, W,
    W, W, B, B, B, W, W, W
]

# Display these colours on the LED matrix
sense.set_pixels(happy_plant)