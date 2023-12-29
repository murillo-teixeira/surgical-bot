def process_input(axes, buttons, robot_bisturi, robot_camera):
    threshold = 0.9

    movement_in_progress = False

    if buttons[5]:
        print('move camera pitch down')
        # robot_camera.move_manual('p', 'decrease')
    elif buttons[7]:
        print('move camera pitch up')
        # robot_camera.move_manual('p', 'increase')
        

    if buttons[4] and not buttons[6]:
        robot_bisturi.move_manual('z', 'decrease')
        # print("Decrease z")
        movement_in_progress = True
    elif not buttons[4] and buttons[6]:
        robot_bisturi.move_manual('z', 'increase')
        # print("Increase z")
        movement_in_progress = True

    if axes[0] >= threshold:
        robot_bisturi.move_manual('y', 'increase')
        # print("Increase y")
        movement_in_progress = True
    elif axes[0] <= -threshold:
        robot_bisturi.move_manual('y', 'decrease')
        # print("Decrease y")
        movement_in_progress = True

    if axes[1] >= threshold:
        robot_bisturi.move_manual('x', 'decrease')
        # print("Decrease x")
        movement_in_progress = True

    elif axes[1] <= -threshold:
        robot_bisturi.move_manual('x', 'increase')
        # print("Increase x")
        movement_in_progress = True

    if axes[2] >= threshold:
        robot_bisturi.move_manual('r', 'increase')
        # print("Increase roll")
        movement_in_progress = True
    elif axes[2] <= -threshold:
        robot_bisturi.move_manual('r', 'decrease')
        # print("Decrease roll")
        movement_in_progress = True

    if axes[3] >= threshold:
        robot_bisturi.move_manual('p', 'decrease')
        # print("Decrease pitch")
        movement_in_progress = True
    elif axes[3] <= -threshold:
        robot_bisturi.move_manual('p', 'increase')
        # print("Increase pitch")
        movement_in_progress = True

    return movement_in_progress
