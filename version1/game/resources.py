import pyglet

pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

background_image = pyglet.resource.image('space-1.jpg')
background_image.width = 800
background_image.height = 600

asteroid_image = pyglet.resource.image('pixelated-asteroid-1.png')
asteroid_image.width = 50
asteroid_image.height = 50

player_image = pyglet.resource.image('blue_rocket.png')
player_image.width = 30
player_image.height = 30

engine_image1 = pyglet.resource.image('engine_flame1.png')
engine_image1.width = 35
engine_image1.height = 25

engine_image2 = pyglet.resource.image('engine_flame2.png')
engine_image2.width = 35
engine_image2.height = 25

engine_image3 = pyglet.resource.image('engine_flame3.png')
engine_image3.width = 35
engine_image3.height = 25

engine_image4 = pyglet.resource.image('engine_flame4.png')
engine_image4.width = 35
engine_image4.height = 25

bullet_image = pyglet.resource.image('bullet.png')

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

center_image(player_image)
center_image(asteroid_image)
center_image(bullet_image)
engine_image1.anchor_x = engine_image1.width * 1.5
engine_image1.anchor_y = engine_image1.height / 2

engine_image2.anchor_x = engine_image2.width * 1.5
engine_image2.anchor_y = engine_image2.height / 2

engine_image3.anchor_x = engine_image3.width * 1.5
engine_image3.anchor_y = engine_image3.height / 2

engine_image4.anchor_x = engine_image4.width * 1.5
engine_image4.anchor_y = engine_image4.height / 2
