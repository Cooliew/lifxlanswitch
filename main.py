# LIFX LAN Switch Project
# Written by Cooliew and Noxx

from lifxlan import LifxLAN
from gpiozero import RotaryEncoder, Button

rotor = RotaryEncoder(17, 18, wrap=False, max_steps=15)
lifx = LifxLAN()
devices = lifx.get_lights()

def main():
	for device in devices:
		print(device.get_label())
		if device.get_label() == "Terrarium Lamp":
			light = device
	else:
		print('List finished')
		print(light.get_label(), ' selected.')
	colour = list(light.get_color())
	currentSteps = int((((colour[2]/65535)*2)-1)*30)
	while True:
		rotor.steps = currentSteps
		rotor.wait_for_rotate(30)
		rotor.when_rotated = changeColour

def changeColour():
	colour[2] = int(((rotor.value+1)/2)*65535)
	print(rotor.steps)
	currentSteps = rotor.steps
	light.set_color(colour, 0, True)

def dim(amount, light):
	colour = list(light.get_color())
	brightness = colour[2]
	brightness += amount
	if brightness < 0:
		brightness = 0
	elif brightness > 65535:
		brightness = 65535
	colour[2] = brightness
	light.set_color(colour, 0, True)

if __name__ == "__main__":
	main()
