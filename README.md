# Interface

- Joystick 1: Control XY movement 
- L/R: Control Z
- Joystick 2: Control roll & pitch
- Jowstick 2 button: Open Menu to preset Camera positions
- Circle: Change controlled robot



# Methods
- Pose (data type)
    - Position: [x, y, z]
    - Orientation: [pitch, roll]

- Robot
    - Initialize and Calibrate
    - Update position

- Joystick and Robot:
    - move_to_desired_pose()

- Joystick only:
    - update_desired_pose()
    - open_menu()
    - select_menu(option)
        - just update_desired_pose() to known positions
    - change_robot()
    

# Metrics to evaluate the work
- Counting how many times each button was used
- Time to do a slice
- Google Forms

# Separate work
- Joysticks: create a class that calls the functions
- Control the robot using the keyboard with the same functions

# Ideas
- Collision between robots
- Camera zoom
- Control speed
- Estimate distance from body
- Use a simulator

# Final code sketch
```python
robot1 = Robot(PORT1)

robot2 = Robot(PORT2)

joystick = Joystick(PORT3)

# 1 second timer
def timer():
    robot1.move_to_desired_pose(())
    robot2.move_to_desired_pose(joystick.robot2_pos)

def main():
	try:
		while True:
            joytick.process_inputs()
	except KeyboardInterrupt:
		pass
		
```