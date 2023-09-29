import sys
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)
print(f"I2c device found: {[hex(i) for i in i2c.scan()]}")
