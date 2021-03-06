import numpy as np


# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):

    if Rover.nav_angles is not None:
        # To pick up the rock found
        if Rover.mode == 'rock_pickup':
            Rover.steer = Rover.samples_ang * 180/np.pi
            Rover.throttle = 0.2
            Rover.brake = 0
            # Check if the rock is near enough to pick up the rock
            if Rover.near_sample == 1:
                Rover.throttle = 0
                Rover.brake = 10
                # Send pick-up command
                Rover.send_pickup = True
                Rover.mode = 'forward'
            # Vel < 1 for better approaching
            else:
                if Rover.vel > 1:
                    Rover.throttle = 0
            # Check if the rover is stuck
            if Rover.vel < 0.1:
                if Rover.stuck_interval == -1.0:
                    Rover.stuck_time = Rover.total_time
                    Rover.stuck_interval = 0.0
                else:
                    Rover.stuck_interval += (Rover.total_time - Rover.stuck_time)
                    Rover.stuck_time = Rover.total_time
                    if Rover.stuck_interval > 5:
                        # Record current state for coming back to the same mode
                        Rover.recover_state = 'rock_pickup'
                        Rover.ori_steer = Rover.steer
                        Rover.mode = 'stuck'
                        Rover.stuck_interval = -1.0
            else:
                Rover.stuck_interval = -1.0


        # Check for Rover.mode status
        elif Rover.mode == 'forward': 
            # Check whether the rover is stuck
            if Rover.vel < 0.1 and Rover.picking_up == 0:
                if Rover.stuck_interval == -1.0:
                    Rover.stuck_time = Rover.total_time
                    Rover.stuck_interval = 0.0
                else:
                    Rover.stuck_interval += (Rover.total_time - Rover.stuck_time)
                    Rover.stuck_time = Rover.total_time
                    if Rover.stuck_interval > 5:
                        Rover.mode = 'stuck'
                        # Record current state for coming back to the same mode
                        Rover.recover_state = 'forward'
                        Rover.ori_steer = Rover.steer
                        Rover.stuck_interval = -1.0
            else:
                Rover.stuck_interval = -1.0
            # Check the extent of navigable terrain
            if len(Rover.nav_angles) >= Rover.stop_forward:  
                # If mode is forward, navigable terrain looks good 
                # and velocity is below max, then throttle 
                if Rover.vel < Rover.max_vel:
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                else: # Else coast
                    Rover.throttle = 0
                Rover.brake = 0
                # Set steering to average angle clipped to the range +/- 15
                Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            elif len(Rover.nav_angles) < Rover.stop_forward:
                    # Set mode to "stop" and hit the brakes!
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = Rover.brake_set
                    Rover.ori_steer = Rover.steer
                    Rover.mode = 'stop'

        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                if len(Rover.nav_angles) < Rover.go_forward:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    if Rover.ori_steer == 0:
                        Rover.steer = -15
                    else:
                        Rover.steer = -np.sign(Rover.ori_steer)*15 # Could be more clever here about which way to turn
                # If we're stopped but see sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward:
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                    Rover.mode = 'forward'
        # Stuck mode
        elif Rover.mode == 'stuck':
            Rover.brake =0
            # If backward vel enough, go back to original mode 
            if Rover.vel < -0.5:
                Rover.mode = Rover.recover_state
            else:
                # Move the rover backwards
                Rover.throttle = -1
                if Rover.ori_steer == 0:
                    Rover.steer = -15
                else:
                    # Turn the rover in opposite direction
                    Rover.steer = -np.sign(Rover.ori_steer)*15

    # Just to make the rover do something 
    # even if no modifications have been made to the code
    else:
        Rover.throttle = 0
        Rover.steer = -15
        Rover.brake = 0
        
    # If in a state where want to pickup a rock send pickup command
    
    #if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
    #    Rover.send_pickup = True
    #    Rover.mode = 'forward'
    return Rover

