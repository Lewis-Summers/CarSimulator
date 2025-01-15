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


def positionUpdates(currentSpeed, frontAxleRotationRadians, carRotationRadians):
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
    if turningRadius == 0:
        return 0
    angularForce = (carMass * (currentSpeed ** 2)) / turningRadius
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
acceleration = 250
coastingDeceleration = 50
brakingDeceleration = 500
topSpeed = 500
axleOffset = 0.25
tireRotation = 55

# PG VARIABLES
carRotation = 270
frontAxleRotation = 0

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
            frontAxleRotation -= 25 * dt
    if keys[pg.K_d]:
        if frontAxleRotation > tireRotation:
            frontAxleRotation = tireRotation
        else:
            frontAxleRotation += 25 * dt
    if keys[pg.K_d] and keys[pg.K_a]:
        if frontAxleRotation > 0:
            frontAxleRotation -= 25
        elif frontAxleRotation < 0:
            frontAxleRotation += 25
    elif not keys[pg.K_d] and not keys[pg.K_a]:  # No input
        if frontAxleRotation > 0:
            frontAxleRotation = max(0, frontAxleRotation - 5)  # Gradually reduce to 0
        elif frontAxleRotation < 0:
            frontAxleRotation = min(0, frontAxleRotation + 5)  # Gradually increase to 0

    carRotation %= 360

    carRotationRadians = math.radians(carRotation)
    frontAxleRotationRadians = math.radians(frontAxleRotation)

    player_pos, carRotation, carRotationRadians = positionUpdates(currentSpeed, frontAxleRotationRadians,
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

    pg.display.flip()

pg.quit()
