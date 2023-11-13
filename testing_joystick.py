#
# code from
# https://stackoverflow.com/questions/49352561/sending-joystick-input-to-program-using-python/57962941#57962941
#

# the leftpad only works in digital mode
# the trigger buttons only work in analog mode
# the axis only gives continuous values in analog mode; otherwise they
# operate as digital
#

import pygame
import re

pygame.init()

clock = pygame.time.Clock()
pygame.joystick.init()
done = False

# -------- Main Program Loop -----------
while not done:
    try:
        
        for event in pygame.event.get(): # User did something.
            if event.type == pygame.QUIT: # If user clicked close.
                done = True # Flag that we are done so we exit this loop.
                
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        
        axis0 = joystick.get_axis(0)
        print("Axis 0:", round(axis0, 0), end=' | ')
        axis1 = joystick.get_axis(1)
        print("Axis 1:", round(axis1, 0))

        ser.write(b"HERE P1 \r")
        time.sleep(1)
        ser.write(b"LISTPV P1 \r")
        time.sleep(1)
        thing = ser.read_all()
        pattern = "X:([\s-]\d+)\s*Y:([\s-]\d+)\s*Z:([\s-]\d+)"
        match = re.search(pattern, thing.decode('ascii'))
        current_x = int(match.group(1))
        current_y = int(match.group(2))
        current_z = int(match.group(3))
        
        # Move the robot to (x, y, z) + pvect

        clock.tick(20)
    except Exception as e:
        print(e)
        break

pygame.quit()
