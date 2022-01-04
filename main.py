from ursina import *
import random as r

GROUND_LEVEL = -7
GRAVITY = 0.5
ENEMY_START_SPEED = 15
MAX_FALL_SPEED = 10
JUMP_STRENGTH = -15
ENEMY_SPAWN_RATE = 100

app = Ursina()

bg = Animation('assets/background', scale=(50,25), position=(7, -0.5), z=10)
scooter = Animation('assets/jumpman', collider='box', scale=(2,3,2), y=GROUND_LEVEL)
pointsText = Text("Points: 0", scale=(2,2,2), color=color.black, position=(-0.85,0.45,0))

window.borderless = False
window.exit_button.visible = False
window.fps_counter.visible =False
camera.orthographic = True
camera.fov = 20

fallSpeed = MAX_FALL_SPEED
enemySpeed = ENEMY_START_SPEED
points = 0
stopped = False
lastEnemySpawn = 0

def update():
    global fallSpeed, points, stopped, lastEnemySpawn
    if stopped:
        return
    
    points += 1
    pointsText.text = f"Points: {points}"

    if scooter.y > GROUND_LEVEL or fallSpeed < MAX_FALL_SPEED:
        scooter.y -= fallSpeed*time.dt
        fallSpeed += GRAVITY
    else:
        scooter.y = GROUND_LEVEL
        fallSpeed = MAX_FALL_SPEED
        scooter.rotation = (0,0,0)
    
    lastEnemySpawn += 1
    if (lastEnemySpawn > 100 and r.randint(1, 1000) < ENEMY_SPAWN_RATE) or lastEnemySpawn > 300:
        newEnemy()
    
    for enemy in enemies:
        enemy.x -= enemySpeed*time.dt
    
    touch = scooter.intersects()
    if touch.hit:
        stopped = True
        bg.color = color.red
        scooter.rotation = (0,0,-170)


def input(key):
    global fallSpeed, stopped
    if key == 'space' and scooter.y == GROUND_LEVEL:
        fallSpeed = JUMP_STRENGTH
        scooter.rotation = (0,0,-15)
    if key == 'r':
        stopped = False

enemies = []
enemy = Entity(model='quad', texture='assets/ninja', position=(20,20), scale=(1,3,100), collider='box')

def newEnemy():
    global enemySpeed, lastEnemySpawn
    new = duplicate(enemy, y=GROUND_LEVEL)
    enemies.append(new)
    enemySpeed += 0.5
    lastEnemySpawn = 0

app.run()