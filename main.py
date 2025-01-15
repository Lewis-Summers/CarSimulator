import pygame as pg
import math


def positionUpdates2(currentSpeed, frontAxleRotation, carRotation):
    # TODO: next step is figure out how speed and front axle rotation effects car rotation
    print(player_pos.y)
    print(player_pos.x)
    frontAxlePosition, rearAxlePosition = calculateAxlePosition(carRotation)
    if frontAxleRotation != 0:
        turningRadius = carWidth / math.sin(frontAxleRotation)
        angularVelocity = currentSpeed / turningRadius
    else:
        angularVelocity = 0

    carRotation += angularVelocity * dt
    displacement = currentSpeed * dt
    translation = (
        math.cos(carRotation) * displacement,
        math.sin(carRotation) * displacement
    )
    player_pos.x = player_pos.x + translation[0]
    player_pos.y = player_pos.y + translation[1]
    # if currentSpeed != 0:
    #     distance = currentSpeed * dt
    #     player_pos.y += distance * math.sin(carRotation)
    #     player_pos.x += distance * math.cos(carRotation)
    print(player_pos.y)
    print(player_pos.x)
    return player_pos, carRotation


def positionUpdates3(currentSpeed, frontAxleRotation, carRotation):
    # TODO: next step is figure out how speed and front axle rotation effects car rotation
    print(player_pos.y)
    print(player_pos.x)
    frontAxlePosition, rearAxlePosition = calculateAxlePosition(carRotation)
    heading_angle = math.atan2(frontAxlePosition[1] - rearAxlePosition[1],
                               frontAxlePosition[0] - rearAxlePosition[0])

    # Update rear axle to follow front axle
    rearAxlePosition[0] += currentSpeed * dt * math.cos(heading_angle)
    rearAxlePosition[1] += currentSpeed * dt * math.sin(heading_angle)

    angularForce = 0
    turningRadius = None

    # Update front axle based on steering angle
    if frontAxleRotation != 0:
        turningRadius = carWidth / math.sin(frontAxleRotation)
        frontAxlePosition[0] += currentSpeed * dt * math.cos(heading_angle + frontAxleRotation)
        frontAxlePosition[1] += currentSpeed * dt * math.sin(heading_angle + frontAxleRotation)
    # if frontAxleRotation != 0:
    #     turningRadius = carWidth / math.sin(frontAxleRotation)
    #     # angleChange = turningRadius*dt
    #     # angularVelocity = currentSpeed / turningRadius
    #     player_pos.x += currentSpeed * dt * math.cos(frontAxleRotation)
    #     player_pos.y += currentSpeed * dt * math.sin(frontAxleRotation)

    else:
        distance = currentSpeed * dt
        player_pos.y += distance * math.sin(carRotation)
        player_pos.x += distance * math.cos(carRotation)

    print(carRotation)
    return player_pos, carRotation, frontAxleRotation


def positionUpdates4(currentSpeed, frontAxleRotation, carRotation, carMass):
    # Example mass for the car, if not passed
    carMass = carMass or 1200  # Default car mass in kg
    print(player_pos.y)
    print(player_pos.x)
    frontAxlePosition, rearAxlePosition = calculateAxlePosition(carRotation)
    heading_angle = math.atan2(frontAxlePosition[1] - rearAxlePosition[1],
                               frontAxlePosition[0] - rearAxlePosition[0])

    # Update rear axle to follow front axle
    rearAxlePosition[0] += currentSpeed * dt * math.cos(heading_angle)
    rearAxlePosition[1] += currentSpeed * dt * math.sin(heading_angle)

    angularForce = 0
    turningRadius = None
    # Update front axle based on steering angle
    if frontAxleRotation != 0:
        turningRadius = carWidth / math.sin(frontAxleRotation)
        frontAxlePosition[0] += currentSpeed * dt * math.cos(heading_angle + frontAxleRotation)
        frontAxlePosition[1] += currentSpeed * dt * math.sin(heading_angle + frontAxleRotation)

        # Calculate angular force
        angularForce = calculateAngularForce(currentSpeed, turningRadius, carMass)

    else:
        distance = currentSpeed * dt
        player_pos.y += distance * math.sin(carRotation)
        player_pos.x += distance * math.cos(carRotation)

    # print(carRotation)
    # print(f"Angular Force: {angularForce} N")  # Debug output for angular force
    return player_pos, carRotation, frontAxleRotation, angularForce


def positionUpdates(currentSpeed, frontAxleRotationRadians, carRotationRadians, carMass=1200):
    # Example mass for the car, if not passed
    carMass = carMass or 1200  # Default car mass in kg
    frontAxle, rearAxle = calculateAxlePosition(carRotationRadians)

    angularForce = 0
    turningRadius = None
    # Update the front axle based on steering angle
    if frontAxleRotationRadians != 0:
        turningRadius = 50 / math.sin(frontAxleRotationRadians)  # Adjust for car width
        frontAxle = (
            frontAxle[0] + currentSpeed * dt * math.cos(carRotationRadians + frontAxleRotationRadians),
            frontAxle[1] + currentSpeed * dt * math.sin(carRotationRadians + frontAxleRotationRadians)
        )

        # Calculate angular force
        angularForce = calculateAngularForce(currentSpeed, turningRadius, carMass)

    # Calculate heading angle (car rotation) based on front and rear axle positions
    carRotationRadians = math.atan2(frontAxle[1] - rearAxle[1], frontAxle[0] - rearAxle[0])

    # Update rear axle to follow the front axle
    rearAxle = (
        rearAxle[0] + currentSpeed * dt * math.cos(carRotationRadians),
        rearAxle[1] + currentSpeed * dt * math.sin(carRotationRadians)
    )

    # Update player position to be between the two axles
    player_pos.x = (frontAxle[0] + rearAxle[0]) / 2
    player_pos.y = (frontAxle[1] + rearAxle[1]) / 2

    # print(f"Angular Force: {angularForce} N")  # Debug output for angular force
    return player_pos, math.degrees(carRotationRadians), carRotationRadians, angularForce


def positionUpdates2(currentSpeed, frontAxleRotationRadians, carRotationRadians):
    # Calculate front and rear axle positions
    frontAxle, rearAxle = calculateAxlePosition(carRotationRadians)

    # Update the front axle based on steering angle
    if frontAxleRotationRadians != 0:
        turningRadius = 50 / math.sin(frontAxleRotationRadians)  # Adjust for car width
        frontAxle = (
            frontAxle[0] + currentSpeed * dt * math.cos(carRotationRadians + frontAxleRotationRadians),
            frontAxle[1] + currentSpeed * dt * math.sin(carRotationRadians + frontAxleRotationRadians)
        )

    # Calculate heading angle (car rotation) based on front and rear axle positions
    carRotationRadians = math.atan2(frontAxle[1] - rearAxle[1], frontAxle[0] - rearAxle[0])

    # Update rear axle to follow the front axle
    rearAxle = (
        rearAxle[0] + currentSpeed * dt * math.cos(carRotationRadians),
        rearAxle[1] + currentSpeed * dt * math.sin(carRotationRadians)
    )

    # Update player position to be between the two axles
    player_pos.x = (frontAxle[0] + rearAxle[0]) / 2
    player_pos.y = (frontAxle[1] + rearAxle[1]) / 2

    return player_pos, math.degrees(carRotationRadians), carRotationRadians


def calculateAngularForce(currentSpeed, turningRadius, carMass=1200):
    currentSpeed2=currentSpeed/300
    if turningRadius == 0:
        return 0
    angularForce = (carMass * (currentSpeed2 ** 2)) / turningRadius
    # print(angularForce)
    return angularForce


def calculateAxlePosition(carRotationRadians):
    axle_offset = carWidth * -0.2  # Assuming carHeight is the full height of the car
    frontAxleLocation = (
        player_pos.x + (carWidth / 2) * math.cos(carRotationRadians),  # half of height to center
        player_pos.y + (carWidth / 2) * math.sin(carRotationRadians)  # half of height to center
    )
    frontAxleLocation = (
        frontAxleLocation[0] + axle_offset * math.cos(carRotationRadians),
        frontAxleLocation[1] + axle_offset * math.sin(carRotationRadians)
    )
    rearAxleLocation = (
        player_pos.x - (carWidth / 2) * math.cos(carRotationRadians),  # half of height to center
        player_pos.y - (carWidth / 2) * math.sin(carRotationRadians)  # half of height to center
    )
    rearAxleLocation = (
        rearAxleLocation[0] - axle_offset * math.cos(carRotationRadians),
        rearAxleLocation[1] - axle_offset * math.sin(carRotationRadians)
    )
    return frontAxleLocation, rearAxleLocation


pg.init()
screen = pg.display.set_mode((1280, 720))
running = True
clock = pg.time.Clock()

# CAR VARIABLES
acceleration = 500
coastingDeceleration = 50
brakingDeceleration = 500
topSpeed = 500
turningTopSpeed = 500
straightTopSpeed = 500
axleOffset = 0.25
tireRotation = 55
turningSpeed = 55
# PG VARIABLES
carRotation = 270
frontAxleRotation = 0
speed_history = [0] * 20

currentSpeed = 0
player_pos = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)

carImage = pg.image.load('assests/red-sports-car.png').convert_alpha()  # Ensure the image has transparency (PNG)
imgWidth, imgHeight = carImage.get_size()
carWidth = 160
carHeight = int(carWidth * (imgHeight/imgWidth))
carImage = pg.transform.scale(carImage, (carWidth, carHeight))
carImage = pg.transform.flip(carImage, True, False)


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    dt = clock.tick(60) / 1000

    screen.fill('black')

    keys = pg.key.get_pressed()

    if keys[pg.K_d] or keys[pg.K_a]:
        topSpeed = turningTopSpeed

    else:
        topSpeed = straightTopSpeed
    # print(currentSpeed)
    if keys[pg.K_w]:
        currentSpeed += acceleration * dt
        if currentSpeed > topSpeed:
            currentSpeed = topSpeed
    else:  # if not actively accelerating
        currentSpeed -= coastingDeceleration * dt
        if currentSpeed < 0:
            currentSpeed = 0

    if keys[pg.K_s]:  # if braking
        currentSpeed -= brakingDeceleration * dt
        if currentSpeed < 0:
            currentSpeed = 0

    if keys[pg.K_a]:
        if frontAxleRotation < -tireRotation:
            frontAxleRotation = -tireRotation
        else:
            frontAxleRotation -= turningSpeed * dt
    if keys[pg.K_d]:
        if frontAxleRotation > tireRotation:
            frontAxleRotation = tireRotation
        else:
            frontAxleRotation += turningSpeed * dt
    if keys[pg.K_d] and keys[pg.K_a]:
        if frontAxleRotation > 0:
            frontAxleRotation -= turningSpeed
        elif frontAxleRotation < 0:
            frontAxleRotation += turningSpeed
    elif not keys[pg.K_d] and not keys[pg.K_a]:  # No input
        if frontAxleRotation > 0:
            frontAxleRotation = max(0, frontAxleRotation - 5)  # Gradually reduce to 0
        elif frontAxleRotation < 0:
            frontAxleRotation = min(0, frontAxleRotation + 5)  # Gradually increase to 0

    carRotation %= 360

    carRotationRadians = math.radians(carRotation)
    frontAxleRotationRadians = math.radians(frontAxleRotation)

    player_pos, carRotation, carRotationRadians, angularForce = positionUpdates(currentSpeed, frontAxleRotationRadians,
                                                                  carRotationRadians)
    # Rotate and display the car image
    rotatedCarImage = pg.transform.rotate(carImage, -carRotation)
    rotatedCar = rotatedCarImage.get_rect(center=(player_pos.x, player_pos.y))
    screen.blit(rotatedCarImage, rotatedCar.topleft)

    # Draw circles at the front and rear axle positions
    frontAxleLocation, rearAxleLocation = calculateAxlePosition(carRotationRadians)
    pg.draw.circle(screen, 'blue', (int(frontAxleLocation[0]), int(frontAxleLocation[1])), 5)
    pg.draw.circle(screen, 'blue', (int(rearAxleLocation[0]), int(rearAxleLocation[1])), 5)

    # Visualize the direction of the front axle
    # pg.draw.circle(screen, 'red', (
    #     int(frontAxleLocation[0] + 50 * math.sin(frontAxleRotationRadians)),
    #     int(frontAxleLocation[1] + 50 * math.cos(frontAxleRotationRadians))
    # ), 5)
    force_scale = 0.5  # Adjust to fit your screen size

    # Calculate the arrow's direction and length
    if angularForce != 0:  # Only draw if there's an angular force
        # Direction is perpendicular to the heading angle (car rotation)
        force_angle = (carRotationRadians + math.pi / 2)  # Perpendicular to car's heading
        arrow_length = -angularForce * force_scale  # Scale the force for visualization

        # Start position of the arrow (center of the car)
        arrow_start = (player_pos.x, player_pos.y)

        # End position of the arrow based on direction and length
        arrow_end = (
            player_pos.x + arrow_length * math.cos(force_angle),
            player_pos.y + arrow_length * math.sin(force_angle)
        )

        # Draw the arrow (line with a circle at the tip for better visibility)
        pg.draw.line(screen, 'red', arrow_start, arrow_end, 3)  # Red arrow line
        pg.draw.circle(screen, 'red', (int(arrow_end[0]), int(arrow_end[1])), 5)

    # Update the speed history
    acceleration_scale = 0.1
    speed_history.pop(0)  # Remove the oldest value
    speed_history.append(currentSpeed)  # Add the current speed

    # Calculate smoothed acceleration
    average_delta_speed = (speed_history[-1] - speed_history[0]) / len(speed_history)
    smoothed_acceleration = average_delta_speed / dt  # a = Δv / Δt

    # Scale the arrow length
    arrow_length = abs(smoothed_acceleration) * acceleration_scale  # Always positive for length

    # Adjust the arrow direction
    if smoothed_acceleration >= 0:
        # Positive acceleration: Arrow points backward
        arrow_direction = carRotationRadians + math.pi
    else:
        # Negative acceleration: Arrow points forward
        arrow_direction = carRotationRadians

    # Calculate arrow positions
    arrow_start = (player_pos.x, player_pos.y)
    arrow_end = (
        player_pos.x + arrow_length * math.cos(arrow_direction),
        player_pos.y + arrow_length * math.sin(arrow_direction)
    )

    # Draw the arrow
    if smoothed_acceleration > 0:
        arrow_color = 'red'
    elif smoothed_acceleration == 0:
        arrow_color = 'green'
    else:
        arrow_color = 'red'
    pg.draw.line(screen, arrow_color, arrow_start, arrow_end, 3)  # Line
    pg.draw.circle(screen, arrow_color, (int(arrow_end[0]), int(arrow_end[1])), 5)  # Arrow tip

    font = pg.font.Font(None, 24)  # Default font, size 24

    # Text to display
    acceleration_text = f"Acceleration: {smoothed_acceleration/3:.2f} mf/s²"
    speed_text = f"Speed: {currentSpeed/3:.2f} ft/s"
    angular_force_text = f"Angular Force: {angularForce/3:.2f} N·m"

    # Render the text
    acceleration_surface = font.render(acceleration_text, True, 'white')
    speed_surface = font.render(speed_text, True, 'white')
    angular_force_surface = font.render(angular_force_text, True, 'white')

    # Position the text surfaces on the screen
    screen.blit(acceleration_surface, (10, 10))  # Top-left corner
    screen.blit(speed_surface, (10, 40))  # Below acceleration
    screen.blit(angular_force_surface, (10, 70))  # Below speed

    pg.display.flip()

pg.quit()
