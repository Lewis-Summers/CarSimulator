import pygame as pg
import math

pg.init()
screen = pg.display.set_mode((1280, 720))
running = True
clock = pg.time.Clock()

# CAR VARIABLES
acceleration = 50
coastingDeceleration = 50
brakingDeceleration = 150
topSpeed = 300


# PG VARIABLES
rotation = 270
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

    rotatedCarImage = pg.transform.rotate(carImage, -rotation)
    rotatedCar = rotatedCarImage.get_rect(center=(player_pos.x, player_pos.y))
    screen.blit(rotatedCarImage, rotatedCar.topleft)

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

    if currentSpeed != 0:
        distance = currentSpeed * dt
        rotationRadians = math.radians(rotation)
        player_pos.y += distance * math.sin(rotationRadians)
        player_pos.x += distance * math.cos(rotationRadians)

    if keys[pg.K_a]:
        rotation += 120 * dt
    if keys[pg.K_d]:
        rotation -= 120 * dt
    rotation %= 360

    pg.display.flip()

pg.quit()
