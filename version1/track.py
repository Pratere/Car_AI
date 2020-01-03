import pyglet
from game import resources, load, physicalobject, player, util, model
from pyglet.window import key
from shapely.geometry import LineString, Point

window_width = 800
window_height = 600
game_window = pyglet.window.Window(window_width, window_height)

main_batch = pyglet.graphics.Batch()

score_label = pyglet.text.Label(x=10, y=window_height-25, batch=main_batch)
level_label = pyglet.text.Label(text="My Amazing Game",
                                x=window_width//2, y=window_height-25, anchor_x='center', batch=main_batch)

frame_counter = 0

def create_objects():
    player_ship = player.Player(x=(window_width//2)-250, y=(window_height//2), batch=main_batch)
    game_window.push_handlers(player_ship)
    game_window.push_handlers(player_ship.key_handler)

    game_objects = [player_ship]

    return player_ship, game_objects

def get_distances():
    lines, lines_sight = trainer.player.sight()
    trainer.player.distances = []
    position = Point(trainer.player.x, trainer.player.y)
    _intersections = []
    for i in range(8):
        j = i * 4
        # print(i, j)
        line1 = LineString(((lines_sight[j],
                     lines_sight[j+1]),
                     (lines_sight[j+2],
                     lines_sight[j+3])))
        # print(((lines_sight[j],
        #              lines_sight[j+1]),
        #              (lines_sight[j+2],
        #              lines_sight[j+3])))
        for n in range(30):
            m = n * 2
            # print(n, m)
            if n == 29:
                line2 = LineString(((inner_circle_verts[m],
                                     inner_circle_verts[m+1]),
                                    (inner_circle_verts[0],
                                     inner_circle_verts[1])))
            else:
                line2 = LineString(((inner_circle_verts[m],
                                     inner_circle_verts[m+1]),
                                    (inner_circle_verts[m+2],
                                     inner_circle_verts[m+3])))

            intersect = line1.intersection(line2)
            if not isinstance(intersect, Point):
                if n == 29:
                    line2 = LineString(((outer_circle_verts[m],
                                         outer_circle_verts[m+1]),
                                        (outer_circle_verts[0],
                                         outer_circle_verts[1])))

                else:
                    line2 = LineString(((outer_circle_verts[m],
                                         outer_circle_verts[m+1]),
                                        (outer_circle_verts[m+2],
                                         outer_circle_verts[m+3])))
                intersect = line1.intersection(line2)

            if isinstance(intersect, Point):
                distance = position.distance(intersect)
                if len(trainer.player.distances) > i:
                    # print("Testing double")
                    if trainer.player.distances[i] > distance:
                        # print("Replacing")
                        trainer.player.distances[i] = distance
                        _intersections[-2:] = intersect.x, intersect.y
                    else:
                        pass
                else:
                    # print("Adding {}".format(i+1))
                    _intersections += intersect.x, intersect.y
                    trainer.player.distances += [distance]
            if n == 29 and len(trainer.player.distances) <= i:
                # print(
                #     "Failed to find intersect for {}".format(i+1)
                # )
                _intersections += trainer.player.x, trainer.player.y
                trainer.player.distances += [0]
    # print(trainer.player.distances)
    return _intersections

def update(dt):
    global player_ship
    global game_objects
    global frame_counter
    points.vertices = get_distances()
    if not all(i >= 15 for i in trainer.player.distances):
        trainer.player.color = (255, 0, 0)
        trainer.player.restart = True

    trainer.move()
    for i in range(len(game_objects)):
        for j in range(i+1, len(game_objects)):
            obj_1 = game_objects[i]
            obj_2 = game_objects[j]
            if not obj_1.dead and not obj_2.dead:
                if obj_1.collides_with(obj_2):
                    obj_1.handle_collision_with(obj_2)
                    obj_2.handle_collision_with(obj_1)
    score_label.text = "Score: {0}".format(player_ship.score)

    for obj in game_objects:
        obj.update(dt)

    if player_ship.restart:
        for object in game_objects:
            object.delete()
            game_objects.remove(object)
        player_ship, game_objects = create_objects()
        trainer.player = player_ship
        trainer.replay(True)

    reward = 0
    for i in range(15):
        j = i * 4
        if LineString(((rewards[j],
                      rewards[j+1]),
                      (rewards[j+2],
                      rewards[j+3]))).contains(Point(trainer.player.x,
                                                   trainer.player.y)):
            reward = 4

    get_distances()
    trainer.remember(reward)

    frame_counter += 1
    if frame_counter % 10 == 0:
        trainer.replay()

    q = frame_counter // 1000

    if frame_counter % (120 + q) == 0:
        trainer.player.restart = True

@game_window.event
def on_draw():
    game_window.clear()
    resources.background_image.blit(0,0)
    main_batch.draw()
    inner_circle.draw(pyglet.gl.GL_LINE_LOOP)
    outer_circle.draw(pyglet.gl.GL_LINE_LOOP)
    points.draw(pyglet.gl.GL_LINE_LOOP)
    reward_points.draw(pyglet.gl.GL_LINES)
    # lines, verts_ = player_ship.sight()
    # lines.draw(pyglet.gl.GL_LINES)

if __name__ == '__main__':
    inner_circle, inner_circle_verts = util.makeCircle(31, (window_width/2, window_height/2), 200)
    outer_circle, outer_circle_verts = util.makeCircle(31, (window_width/2, window_height/2), 300)
    rewards = []
    for i in range(15):
        j = i * 4
        rewards += (inner_circle_verts[j],
                    inner_circle_verts[j+1],
                    outer_circle_verts[j],
                    outer_circle_verts[j+1])
    player_ship, game_objects = create_objects()
    # print(inner_circle_verts)
    trainer = model.Agent(player_ship)
    vertexes = get_distances()
    point_num = len(vertexes)//2
    rewards_num = len(rewards)//2
    points = pyglet.graphics.vertex_list(point_num, ('v2f/stream', vertexes))
    reward_points = pyglet.graphics.vertex_list(rewards_num, ('v2f/static', rewards))
    # print(trainer.player.distances)
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()
