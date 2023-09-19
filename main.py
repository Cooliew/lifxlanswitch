# LIFX LAN Switch Project
# Written by Cooliew and Noxx

from lifxlan import LifxLAN
from gpiozero import RotaryEncoder, Button
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1351
from signal import pause
from time import sleep

serial = spi(device=0, port=0)
displayDevice = ssd1351(serial)

rotor = RotaryEncoder(17, 18, wrap=True, max_steps=0)
button = Button(27)
lifx = LifxLAN()
lightDevice = None
colour = None
prevSteps = 0
devices = lifx.get_lights()
for device in devices:
	print(device.get_label())
	if device.get_label() == "Terrarium Lamp":
		lightDevice = device

with canvas(displayDevice) as draw:
	draw.rectangle(displayDevice.bounding_box, outline=none, fill="black")
	draw.rectangle(displayDevice.bounding_box, outline="white", fill="black")
	draw.multiline_text((10, 10), "List finished/n" + lightDevice.get_label() + " selected.", fill="white")
sleep(2)

def main():
	controller()

def controller():
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
			colour = list(lightDevice.get_color())
		brightness = colour[2]
		brightness += amount
		if brightness < 0:
			brightness = 0
		elif brightness > 65535:
			brightness = 65535
		colour[2] = brightness
		lightDevice.set_color(colour, 500, True)
		canvas.clear()
		with canvas(displayDevice) as draw:
			draw.rounded_rectangle(displayDevice.bounding_box, radius=10, fill=draw.hsl(round((brightness / 65535) * 100),100,50),outline="white", width=2)
	except Exception as error:
		print("An exception occurred:", error)

def setColour():
	global prevSteps, colour
	steps = rotor.steps - prevSteps
	prevSteps = rotor.steps
	try:
		amount = 2000 * steps
		if colour is None:
			colour = list(lightDevice.get_color())
		hue = colour[0]
		hue += amount
		if hue < 0:
			hue += 65535
		elif hue > 65535:
			hue -= 65535
		colour[0] = hue
		print(str(round((hue / 65535) * 360)) + "°")
		lightDevice.set_color(colour, 500, True)
	except Exception as error:
		print("An exception occurred:", error)

if __name__ == "__main__":
	main()
