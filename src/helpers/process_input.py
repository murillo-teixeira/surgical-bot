def process_input(axes, buttons, robot_bisturi, robot_camera):
    threshold = 0.9

    if buttons[0]:
        print(" show camera option menu") # Risk of pressing the button after

    elif buttons[1]:
        print("nothing")
    elif buttons[2]:
        robot_bisturi.move_automatic(robot_bisturi.ROBOT_INITIAL_POSITION)
        print("reposition robot") # Should we do a verification before? Like press twice with message on the first time
    elif buttons[3]:
        print("nothing")

    if buttons[5]:
        print('move camera pitch down')
        # robot_camera.move_manual('p', 'decrease')
    elif buttons[7]:
        print('move camera pitch up')
        # robot_camera.move_manual('p', 'increase')
        

    if buttons[4] and not buttons[6]:
        robot_bisturi.move_manual('z', 'decrease')
        print("Decrease z")
    elif not buttons[4] and buttons[6]:
        robot_bisturi.move_manual('z', 'increase')
        print("Increase z")

    if axes[0] >= threshold:
        robot_bisturi.move_manual('y', 'increase')
        print("Increase y")
    elif axes[0] <= -threshold:
        robot_bisturi.move_manual('y', 'decrease')
        print("Decrease y")

    if axes[1] >= threshold:
        robot_bisturi.move_manual('x', 'decrease')
        print("Decrease x")
    elif axes[1] <= -threshold:
        robot_bisturi.move_manual('x', 'increase')
        print("Increase x")

    if axes[2] >= threshold:
        robot_bisturi.move_manual('r', 'increase')
        print("Increase roll")
    elif axes[2] <= -threshold:
        robot_bisturi.move_manual('r', 'decrease')
        print("Decrease roll")

    if axes[3] >= threshold:
        robot_bisturi.move_manual('p', 'decrease')
        print("Decrease pitch")
    elif axes[3] <= -threshold:
        robot_bisturi.move_manual('p', 'increase')
        print("Increase pitch")

