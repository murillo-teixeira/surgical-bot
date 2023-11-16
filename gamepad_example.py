import pygame
import sys
import math

def main():
	# Counter 
	count = 0
	
	# Initialize Pygame
	pygame.init()
	
	# Initialize the gamepad
	pygame.joystick.init()
	
	# Check if any joystick/gamepad is connected
	if pygame.joystick.get_count() == 0:
		print("No gamepad found.")
		return

    # Initialize the first gamepad
	joystick = pygame.joystick.Joystick(0)
	joystick.init()
	
	print(f"Gamepad Name: {joystick.get_name()}")
	
	try:
		while True:
		# Handle events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return
					
				# Get gamepad input
				axes = [round(joystick.get_axis(i),3) for i in range(joystick.get_numaxes())]
				buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
				
				# Counting
				count += 1
				print(count)
				# Process input
				print(f"Axes: {axes}")
				print(f"Buttons: {buttons}")
	
	except KeyboardInterrupt:
		pass
		
	finally:
		# Clean up
		pygame.quit()

if __name__ == "__main__":
    main()
