def process_input(axes, buttons, robot_bisturi, robot_camera):
    threshold = 0.9
    a = 0
    b = 0
    c = 0

    if buttons[2]:
        robot_bisturi.move_automatic(robot_bisturi.ROBOT_INITIAL_POSITION)
        print("reposition robot") # Should we do a verification before? Like press twice with message on the first time\

    if buttons[5]:
        print('move camera pitch down')
        robot_camera.move_manual('p', 'decrease')
    elif buttons[7]:
        print('move camera pitch up')
        robot_camera.move_manual('p', 'increase')
        

    if buttons[4] and not buttons[6]:
        robot_bisturi.move_manual('z', 'decrease')
        print("Decrease z")
        c = -1
    elif not buttons[4] and buttons[6]:
        robot_bisturi.move_manual('z', 'increase')
        print("Increase z")
        c = 1

    if axes[0] >= threshold:
        robot_bisturi.move_manual('y', 'increase')
        print("Increase y")
        b = 1
    elif axes[0] <= -threshold:
        robot_bisturi.move_manual('y', 'decrease')
        print("Decrease y")
        b = -1

    if axes[1] >= threshold:
        robot_bisturi.move_manual('x', 'decrease')
        print("Decrease x")
        a = -1

    elif axes[1] <= -threshold:
        robot_bisturi.move_manual('x', 'increase')
        print("Increase x")
        a = 1

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

    return a, b, c
