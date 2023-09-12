# LIFX LAN Switch Project
# Written by Cooliew and Noxx

from lifxlan import LifxLAN
from gpiozero import RotaryEncoder, Button
from signal import pause
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1351

serial = spi(device=0, port=0)
device = ssd1351(serial)

rotor = RotaryEncoder(17, 18, wrap=True, max_steps=0)
button = Button(27)
lifx = LifxLAN()
light = None
colour = None
prevSteps = 0
devices = lifx.get_lights()
for device in devices:
	print(device.get_label())
	if device.get_label() == "Terrarium Lamp":
		light = device
print('List finished')
print(light.get_label(), 'selected.')


def main():
	controller()

def controller():
	with canvas(device) as draw:
		draw.rectangle(device.bounding_box, outline="white", fill="black")
		draw.text((30, 40), "Hello World", fill="white")
	button.when_pressed = switchMode
	rotor.when_rotated = setBrightness
	pause()

def test():
	print(rotor.steps)

dimMode = True
def switchMode():
	global dimMode
	dimMode = not dimMode
	if dimMode:
		rotor.when_rotated = setBrightness
		print("Switching to brightness...")
	else:
		rotor.when_rotated = setColour
		print("Switching to hue...")

def setBrightness():
	global prevSteps, colour
	steps = rotor.steps - prevSteps
	prevSteps = rotor.steps
	try:
		amount = 6000 * steps
		if colour is None:
			colour = list(light.get_color())
		brightness = colour[2]
		brightness += amount
		if brightness < 0:
			brightness = 0
		elif brightness > 65535:
			brightness = 65535
		colour[2] = brightness
		print(str(round((brightness / 65535) * 100)) + "%")
		light.set_color(colour, 500, True)
	except Exception as error:
		print("An exception occurred:", error)

def setColour():
	global prevSteps, colour
	steps = rotor.steps - prevSteps
	prevSteps = rotor.steps
	try:
		amount = 2000 * steps
		if colour is None:
			colour = list(light.get_color())
		hue = colour[0]
		hue += amount
		if hue < 0:
			hue += 65535
		elif hue > 65535:
			hue -= 65535
		colour[0] = hue
		print(str(round((hue / 65535) * 360)) + "°")
		light.set_color(colour, 500, True)
	except Exception as error:
		print("An exception occurred:", error)

if __name__ == "__main__":
	main()
