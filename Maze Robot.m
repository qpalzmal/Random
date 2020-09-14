brick = ConnectBrick('GROUP7');

running = true;

ULTRASONIC_SENSOR_PORT = 2;
COLOR_SENSOR_PORT = 1;
DISTANCE_TO_WALL = 50;
TIME_TO_MOVE_ONE_BLOCK = 32;
TIME_TO_TURN_90_DEGREES = 13;
FORWARD_SPEED = 85;
TURN_SPEED = 60;
RED_PAUSE = 3;
LOCKOUT = 1;

time = 0;
red_lockout = 0;
% ---------------------------------
% Set to false for real run
% ---------------------------------
person_picked_up = false;

global key
InitKeyboard();

% Sensor is set to return a rgb color
brick.SetColorMode(COLOR_SENSOR_PORT, 4);

while running
    
    color = brick.ColorRGB(COLOR_SENSOR_PORT);
    % disp(color);
    red_lockout = red_lockout - 1;
    
    % Remote control section
    % BLUE
    if color(1) <= 50 && color(2) < color(3)
        pause(0.05);
        %disp(key);
        switch key
            % Drives forward
            case 'uparrow'
                brick.MoveMotor('AD', 100);
                
            % Drives backward
            case 'downarrow'
                brick.MoveMotor('AD', -100);
                
            % Turns left
            case 'leftarrow'
                brick.MoveMotor('A', 30);
                brick.MoveMotor('D', -30);
                
            % Turns right
            case 'rightarrow'
                brick.MoveMotor('A', -30);
                brick.MoveMotor('D', 30);
                
            % Slows to a stop if no keys are pressed
            case 0
                brick.StopAllMotors('Coast');
                
            % Opens the claw
            case 'z'
                brick.MoveMotor('C', 100);
                
            % Closes the claw
            case 'x'
                brick.MoveMotor('C', -100);
            
            % Robot will stop operating after reaching the end
            % Only use after picking up the person
            case 'c'
                disp(person_picked_up);
                person_picked_up = true;
        end % switch key
        key = 0;
        
    % Car stops at red
    % RED
    elseif color(1) >= 90 && color(2) <= 50 && red_lockout < 0
        pause(3);
        red_lockout = LOCKOUT;
       
    % Car reached end
    % GREEN
    elseif color(1) <= 50 && color(2) > color(3) && person_picked_up
        % Drops person off and stops running
        % ---------------------------------
        % UNCOMMENT OUT FOR REAL RUN
        % ---------------------------------
        brick.MoveMotor('C', 100);
        pause(1);
        brick.StopAllMotors('Coast');
        running = false;
        
    % Car is in autononomous mode
    % WHITE
    else
        time = 0;
        % Turn Left
        brick.MoveMotor('A', TURN_SPEED);
        brick.MoveMotor('D', -TURN_SPEED);
        
        % Moves for a set time and will stop on red
        while time < TIME_TO_TURN_90_DEGREES
            % disp(color);
            % disp(time);
            color = brick.ColorRGB(COLOR_SENSOR_PORT);
            time = time + 1;
            if color(1) >= 80 && color(2) <= 60 && red_lockout < 0
                brick.StopAllMotors('Brake');
                pause(RED_PAUSE);
                red_lockout = LOCKOUT;
            end % brake on red if statement
        end % moving if statement
        time = 0;
        brick.StopAllMotors('Brake');
        
        % Car is now facing left
        pause(1);
        distance = brick.UltrasonicDist(ULTRASONIC_SENSOR_PORT);
        disp(distance);
        
        % No Wall Detected
        if distance > DISTANCE_TO_WALL
            % Move Forward
            brick.MoveMotor('AD', FORWARD_SPEED);
            
            % Moves for a set time and will stop on red
            while time < TIME_TO_MOVE_ONE_BLOCK
                % disp(color);
                % disp(time);
                color = brick.ColorRGB(COLOR_SENSOR_PORT);
                time = time + 1;
                if color(1) >= 80 && color(2) <= 60 && red_lockout < 0
                    brick.StopAllMotors('Brake');
                    red_lockout = LOCKOUT;
                    pause(RED_PAUSE);
                end % brake on red if statement
            end % moving if statement
            time = 0;
            brick.StopAllMotors('Brake');
        else
            % Turn Right
            brick.MoveMotor('A', -TURN_SPEED);
            brick.MoveMotor('D', TURN_SPEED);
            
            % Moves for a set time and will stop on red
            while time < TIME_TO_TURN_90_DEGREES
                % disp(color);
                % disp(time);
                color = brick.ColorRGB(COLOR_SENSOR_PORT);
                time = time + 1;
                if color(1) >= 80 && color(2) <= 60 && red_lockout < 0
                    red_lockout = LOCKOUT;
                    pause(RED_PAUSE);
                end % brake on red if statement
            end % moving if statement
            time = 0;
            brick.StopAllMotors('Brake');
            
            % Car is now facing straight
            pause(1);
            distance = brick.UltrasonicDist(ULTRASONIC_SENSOR_PORT);
            disp(distance);
            
            % No Wall Detected
            if distance > DISTANCE_TO_WALL
                % Move Forward
                brick.MoveMotor('AD', FORWARD_SPEED);
                
                % Moves for a set time and will stop on red
                while time < TIME_TO_MOVE_ONE_BLOCK
                    % disp(color);
                    % disp(time);
                    color = brick.ColorRGB(COLOR_SENSOR_PORT);
                    time = time + 1;
                    if color(1) >= 80 && color(2) <= 60 && red_lockout < 0
                        brick.StopAllMotors('Brake');
                        red_lockout = LOCKOUT;
                        pause(RED_PAUSE);
                    end % brake on red if statement
                end % moving if statement
                time = 0;
                brick.StopAllMotors('Brake');
            else 
                % Turn Right
                brick.MoveMotor('A', -TURN_SPEED);
                brick.MoveMotor('D', TURN_SPEED);
                
                % Moves for a set time and will stop on red
                while time < TIME_TO_TURN_90_DEGREES
                    % disp(color);
                    % disp(time);
                    color = brick.ColorRGB(COLOR_SENSOR_PORT);
                    time = time + 1;
                    if color(1) >= 80 && color(2) <= 60 && red_lockout < 0
                        brick.StopAllMotors('Brake');
                        red_lockout = LOCKOUT;
                        pause(RED_PAUSE);
                    end % brake on red if statement
                end % moving if statement
                time = 0;
                brick.StopAllMotors('Brake');
                
                % Car is now facing right
                pause(1);
                distance = brick.UltrasonicDist(ULTRASONIC_SENSOR_PORT);
                disp(distance);
                
                % No Wall Detected
                if distance > DISTANCE_TO_WALL                 
                    % Move Forward
                    brick.MoveMotor('AD', FORWARD_SPEED);
                    
                    % Moves for a set time and will stop on red
                    while time < TIME_TO_MOVE_ONE_BLOCK
                        % disp(color);
                        % disp(time);
                        color = brick.ColorRGB(COLOR_SENSOR_PORT);
                        time = time + 1;
                        
                        if color(1) >= 80 && color(2) <= 60 && red_lockout < 0
                            brick.StopAllMotors('Brake');
                            red_lockout = LOCKOUT;
                            pause(RED_PAUSE);
                        end % brake on red if statement
                    end % moving if statement
                    time = 0;
                    brick.StopAllMotors('Brake');
                else
                    % Turn Right
                    brick.MoveMotor('A', -TURN_SPEED);
                    brick.MoveMotor('D', TURN_SPEED);
                    
                    % Moves for a set time and will stop on red
                    while time < TIME_TO_TURN_90_DEGREES
                        % disp(color);
                        % disp(time);
                        color = brick.ColorRGB(COLOR_SENSOR_PORT);
                        time = time + 1;
                        if color(1) >= 80 && color(2) <= 60 && red_lockout < 0
                            brick.StopAllMotors('Brake');
                            red_lockout = LOCKOUT;
                            pause(RED_PAUSE);
                        end % brake on red if statement
                    end % moving if statement
                    time = 0;
                    brick.StopAllMotors('Brake');
                    
                    % Car is now facing backwards
                    pause(1);
                    distance = brick.UltrasonicDist(ULTRASONIC_SENSOR_PORT);
                    disp(distance);
                    
                    % Move Forward
                    brick.MoveMotor('AD', FORWARD_SPEED);
                    
                    % Moves for a set time and will stop on red
                    while time < TIME_TO_MOVE_ONE_BLOCK
                        % disp(color);
                        % disp(time);
                        color = brick.ColorRGB(COLOR_SENSOR_PORT);
                        time = time + 1;
                        if color(1) >= 80 && color(2) <= 60 && red_lockout < 0
                            brick.StopAllMotors('Brake');
                            red_lockout = LOCKOUT;
                            pause(RED_PAUSE);
                        end % brake on red if statement
                    end % moving if statement
                    time = 0;
                    brick.StopAllMotors('Brake');     
                end % movement if statement
            end % movement if statement
        end % movement if statement
    end % color if statement
end % while loop

CloseKeyboard();
DisconnectBrick(brick);
