# Interface

- Joystick 1: Control XY movement 
- L/R: Control Z
- Joystick 2: Control roll & pitch
- Jowstick 2 button: Open Menu to preset Camera positions
- Circle: Change controlled robot

# Methods
- Joystick and Robot:
    - move_x(value)
    - move_y(value)
    - move_z(value)
    - rotate_roll(value)
    - rotate_pitch(value)

- Joystick only:
    - open_menu()
    - select_menu(option)
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