# skript zum ermitteln von guten positionen für autos und kamera

import sys
import queue
import time
import threading

import numpy as np
import pygame
from pygame.locals import K_a
from pygame.locals import K_d
from pygame.locals import K_s
from pygame.locals import K_w
import cv2
import argparse

import central_data as central
from central_data import carla

# import carla
from carla import Transform, Location, Rotation


def get_font():
    fonts = [x for x in pygame.font.get_fonts()]
    default_font = 'ubuntumono'
    font = default_font if default_font in fonts else fonts[0]
    font = pygame.font.match_font(font)
    return pygame.font.Font(font, 14)


def draw_image(surface, image, blend=False):

    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]
    array = array[:, :, ::-1]
    image_surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
    if blend:
        image_surface.set_alpha(100)
    surface.blit(image_surface, (0, 0))


picture_size = central.picture_size

BB_COLOR = (248, 64, 24)

change = False
fine_control = False


def task():
    global change
    # time.sleep(0.3)
    change = False


def get_image_point(loc, K, w2c):
    # Calculate 2D projection of 3D coordinate

    # Format the input coordinate (loc is a carla.Position object)
    point = np.array([loc.x, loc.y, loc.z, 1])
    # transform to camera coordinates
    point_camera = np.dot(w2c, point)

    # New we must change from UE4's coordinate system to an "standard"
    # (x, y ,z) -> (y, -z, x)
    # and we remove the fourth componebonent also
    point_camera = [point_camera[1], -point_camera[2], point_camera[0]]

    # now project 3D->2D using the camera matrix
    point_img = np.dot(K, point_camera)
    # normalize
    point_img[0] /= point_img[2]
    point_img[1] /= point_img[2]

    return point_img[0:2]


def build_projection_matrix(w, h, fov):
    fov = int(fov)
    focal = w / (2.0 * np.tan(fov * np.pi / 360.0))
    K = np.identity(3)
    K[0, 0] = K[1, 1] = focal
    K[0, 2] = w / 2.0
    K[1, 2] = h / 2.0
    return K

count_bikes = 0
count_lkw = 0

def main(client,ttc):
    cam_pos_num = 0

    # TRAINDATEN TESTDATEN   Town03  Town01  3  1
    type_town_command = ttc
    town_map = "Town03"
    world = None

    list_use_car_location = central.car_pos_targets_t1
    list_use_cam_location = central.cam_pos_t1_c

    #  list_use_car_translate = central.car_pos_translate_t1
    type_te_tr = "train"

    saved_bb_type2 = []
    list_cars_this = []

    intra_counter = 0
    list_counter  = 0
    target_counter = 0

    if type_town_command == 3:
        list_use_car_location = central.car_pos_targets_t3
        list_use_cam_location = central.cam_pos_t3_c
        #   list_use_car_translate = central.car_pos_translate_t3
        list_cars_this = central.list_cars_this_train
        type_te_tr = "train"
        town_map = "Town03"
    else:
        list_use_car_location = central.car_pos_targets_t1
        list_use_cam_location = central.cam_pos_t1_c
        #    list_use_car_translate = central.car_pos_translate_t1
        list_cars_this = central.list_cars_this_test
        type_te_tr = "test"
        town_map = "Town01"

    world = client.load_world(town_map)

    settings = world.get_settings()

    settings_new = carla.WorldSettings(
        no_rendering_mode=False,
        synchronous_mode=True,
        fixed_delta_seconds=1.0 / 40
    )
    world.apply_settings(settings_new)

    camera_list_images = queue.Queue()

    blueprint_library = world.get_blueprint_library()
    # create object and camera
    box = blueprint_library.filter("box01")[0]
    # box_spawnPoint = Transform(Location(x=226.709335, y=7.780001, z=12.089998), Rotation(pitch=-21.999239, yaw=-44.000908, roll=0.000047)) # location_town03[0]
    box_spawnPoint = list_use_cam_location[0][0]

    box_spawnPoint = Transform(
        Location(x=box_spawnPoint.location.x, y=box_spawnPoint.location.y, z=box_spawnPoint.location.z),
        Rotation(pitch=box_spawnPoint.rotation.pitch, yaw=box_spawnPoint.rotation.yaw,
                 roll=box_spawnPoint.rotation.roll))

    b1 = world.spawn_actor(box, box_spawnPoint)

    camera_bp = blueprint_library.find('sensor.camera.rgb')
    camera_bp.set_attribute('image_size_x', str(picture_size[0]))
    camera_bp.set_attribute('image_size_y', str(picture_size[1]))
    camera_bp.set_attribute('fov', str(central.fov_list_train[0]))

    fov_value = str(central.fov_list_train[0])

    use_this_fov = ["5", "10", "15","20","30"]



    cam_transform = carla.Transform(carla.Location(x=1.0, z=0))
    camera = world.spawn_actor(camera_bp, cam_transform, attach_to=b1)

    # b1.set_transform(Transform(Location(x=27.000000, y=-2.000000, z=8.000000), Rotation(pitch=-19.497799, yaw=-6.501043, roll=0.000004)))

    camera.listen(camera_list_images.put)
    car_actor = None
    car_transform = Transform(Location(x=27.000000, y=-2.000000, z=65.000000), Rotation(pitch=0, yaw=0, roll=0.0))

    # vehicle.set_simulate_physics(False)
    mode_control = 1

    pygame.init()

    display = pygame.display.set_mode(
        (picture_size[0], picture_size[1]),
        pygame.HWSURFACE | pygame.DOUBLEBUF)
    clock = pygame.time.Clock()

    font = get_font()

    weather = world.get_weather()

    weather.cloudiness = 0
    weather.precipitation = 0
    weather.precipitation_deposits = 0
    weather.wind_intensity = 0
    weather.fog_density = 0
    weather.fog_distance = 0
    weather.fog_falloff = 0
    weather.wetness = 0
    weather.scattering_intensity = 0
    weather.mie_scattering_scale = 0
    weather.rayleigh_scattering_scale = 0
    weather.sun_altitude_angle = 60

    world.set_weather(weather)

    k = 0
    values = [0, 10, 40, 75, 100]

    camera_list_images.queue.clear()

    # primary_bb_temp = actor_active.bounding_box.get_world_vertices( actor_active.get_transform())
    # bb_extent = primary_bb_temp.extent
    # bb_extent.x *2

    list_actor_group = []

    count_id = 0

    list_new_actors = []


    while (True):

        clock.tick()
        world.tick()

        data = camera_list_images.get()
        img = np.reshape(np.copy(data.raw_data), (data.height, data.width, 4))

     #   array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
     #   array = np.reshape(array, (image.height, image.width, 4))
#        array = array[:, :, :3]
 #       array = array[:, :, ::-1]

        img = img[80:,0:640]
        cv2.imshow("", img)

        fps = round(1.0 / data.timestamp)
        # time.sleep(3)

        # Draw the display.
        draw_image(display, data)
        display.blit(
            font.render('% 5d FPS (real)' % clock.get_fps(), True, (255, 255, 255)),
            (8, 10))
        display.blit(
            font.render('% 5d FPS (simulated)' % fps, True, (255, 255, 255)),
            (8, 28))

        # Get the camera matrix
        world_2_camera = np.array(camera.get_transform().get_inverse_matrix())
        # Get the attributes from the camera
        image_w = camera_bp.get_attribute("image_size_x").as_int()
        image_h = camera_bp.get_attribute("image_size_y").as_int()

        # Calculate the camera projection matrix to project from 3D -> 2D
        K = build_projection_matrix(image_w, image_h, fov_value)

        frame_path = "data\\" + "p1"

        # data.save_to_disk(frame_path+'p1.png') # ,compress_level=1)
        # result = cv2.imwrite(frame_path+".png", img)
        # result = cv2.imwrite(frame_path + ".jpeg", img)
        # Save the image

        # Initialize the exporter
        #   writer = Writer(frame_path +"dd" +'.png', image_w, image_h)

        # box x estend is length  extent.x * 2

        def dot(vec1, vec2):
            return vec1.x * vec2.x + vec1.y * vec2.y + vec1.z * vec2.z

        if car_actor is not None:
            bb = car_actor.bounding_box
            forward_vec = b1.get_transform().get_forward_vector()

            ray = car_actor.get_transform().location - b1.get_transform().location
            if dot(forward_vec, ray) > 1:
                p1 = get_image_point(bb.location, K, world_2_camera)
                verts = [v for v in bb.get_world_vertices(car_actor.get_transform())]
                x_max = -10000
                x_min = 10000
                y_max = -10000
                y_min = 10000
                for vert in verts:
                    p = get_image_point(vert, K, world_2_camera)
                    # Find the rightmost vertex
                    if p[0] > x_max:
                        x_max = p[0]
                    # Find the leftmost vertex
                    if p[0] < x_min:
                        x_min = p[0]
                    # Find the highest vertex
                    if p[1] > y_max:
                        y_max = p[1]
                    # Find the lowest  vertex
                    if p[1] < y_min:
                        y_min = p[1]


                #        writer.addObject('vehicle', x_min, y_min, x_max, y_max)
                #       writer.save(frame_path +"xxxmm"+ '.xml')

                bb_surface = pygame.Surface((picture_size[0], picture_size[1]))
                bb_surface.set_colorkey((0, 0, 0))
          #      print(str(x_min) + " "+ str(x_max) + " "+ str(y_min ) + " "+ str(y_max) )
                # draw lines  bounding box
                pygame.draw.line(bb_surface, BB_COLOR, (int(x_min), int(y_min)), (int(x_max), int(y_min)))
                pygame.draw.line(bb_surface, BB_COLOR, (int(x_min), int(y_max)), (int(x_max), int(y_max)))
                pygame.draw.line(bb_surface, BB_COLOR, (int(x_min), int(y_min)), (int(x_min), int(y_max)))
                pygame.draw.line(bb_surface, BB_COLOR, (int(x_max), int(y_min)), (int(x_max), int(y_max)))
                #   print((int(x_min), int(y_min)), (int(x_max), int(y_min)))

                display.blit(bb_surface, (0, 0))

        if len(list_actor_group) != 0:
            # letzter actor wird genommen, von diesem wird die bounding box gezeichnet
            temp_loc_actor = list_actor_group[-1]
            bb = temp_loc_actor.bounding_box
            forward_vec = b1.get_transform().get_forward_vector()

            ray = temp_loc_actor.get_transform().location - b1.get_transform().location
            if dot(forward_vec, ray) > 1:
                p1 = get_image_point(bb.location, K, world_2_camera)
                verts = [v for v in bb.get_world_vertices(temp_loc_actor.get_transform())]
                x_max = -10000
                x_min = 10000
                y_max = -10000
                y_min = 10000
                for vert in verts:
                    p = get_image_point(vert, K, world_2_camera)
                    # Find the rightmost vertex
                    if p[0] > x_max:
                        x_max = p[0]
                    # Find the leftmost vertex
                    if p[0] < x_min:
                        x_min = p[0]
                    # Find the highest vertex
                    if p[1] > y_max:
                        y_max = p[1]
                    # Find the lowest  vertex
                    if p[1] < y_min:
                        y_min = p[1]

                bb_surface = pygame.Surface((picture_size[0], picture_size[1]))
                bb_surface.set_colorkey((0, 0, 0))
                # draw lines
                pygame.draw.line(bb_surface, BB_COLOR, (int(x_min), int(y_min)), (int(x_max), int(y_min)))
                pygame.draw.line(bb_surface, BB_COLOR, (int(x_min), int(y_max)), (int(x_max), int(y_max)))
                pygame.draw.line(bb_surface, BB_COLOR, (int(x_min), int(y_min)), (int(x_min), int(y_max)))
                pygame.draw.line(bb_surface, BB_COLOR, (int(x_max), int(y_min)), (int(x_max), int(y_max)))

                display.blit(bb_surface, (0, 0))

        pygame.display.flip()
        pygame.event.pump()

        def controls(transform, actor):
            global change
            global fine_control
            # change = False
            if change:
                return

            if keys[K_w]:
                transform.location.x += 1
                change = True
            if keys[K_s]:
                transform.location.x -= 1
                change = True
            if keys[K_d]:
                transform.location.y += 1
                change = True
            if keys[K_a]:
                transform.location.y -= 1
                change = True
            if keys[pygame.constants.K_q]:
                transform.location.z += 1
                change = True
            if keys[pygame.constants.K_e]:
                transform.location.z -= 1
                change = True

            if keys[pygame.constants.K_t]:
                transform.rotation.yaw += 0.5
                change = True
            if keys[pygame.constants.K_r]:
                transform.rotation.yaw -= 0.5
                change = True

            if keys[pygame.constants.K_z]:
                transform.rotation.pitch += 0.5
                change = True
            if keys[pygame.constants.K_u]:
                transform.rotation.pitch -= 0.5
                change = True
            if keys[pygame.constants.K_f]:
                print(actor.get_transform())
                primary_bb_temp = actor.bounding_box
                bb_extent = primary_bb_temp.extent
                print(bb_extent.x)
                bb_extent = bb_extent.x

                if mode_control==2: # car
                    yaw = actor.get_transform().rotation.yaw


                    new_tra = carla.Transform(actor.get_transform().location,actor.get_transform().rotation)
                    yaw_value = int(round(new_tra.rotation.yaw, -1))
                    new_loc = carla.Location(0,0,0)
                    print(yaw_value)

                    if yaw_value == 180 or yaw_value == -180:
                        new_tra.location.x -= bb_extent
                        new_loc.x = 1
                    elif yaw_value==0:
                        new_tra.location.x += bb_extent
                        new_loc.x = -1
                    elif yaw_value==90 or yaw_value==270:
                        new_loc.y = -1
                        new_tra.location.y += bb_extent
                    elif yaw_value==-90 or yaw_value==-270:
                        new_tra.location.y -= bb_extent
                        new_loc.y = 1
                    else:
                        print("error rounding wrong "+str(yaw_value))

                    print( "[" + str(new_tra)+","+ str(new_loc) +"]," )


            if keys[pygame.constants.K_0]:
                fine_control = not fine_control

            nonlocal camera_list_images
            nonlocal camera
            nonlocal camera_bp
            nonlocal fov_value
            nonlocal K
            if keys[pygame.constants.K_y]:
                camera_list_images = queue.Queue()
                camera.destroy()
                fov_value = use_this_fov[0]
                camera_bp.set_attribute('fov', fov_value)
                camera = world.spawn_actor(camera_bp, cam_transform, attach_to=b1)
                camera.listen(camera_list_images.put)

            if keys[pygame.constants.K_x]:
                camera_list_images = queue.Queue()
                camera.destroy()
                fov_value = use_this_fov[1]
                camera_bp.set_attribute('fov', fov_value)
                camera = world.spawn_actor(camera_bp, cam_transform, attach_to=b1)
                camera.listen(camera_list_images.put)

            if keys[pygame.constants.K_c]:
                camera_list_images = queue.Queue()
                camera.destroy()
                fov_value = use_this_fov[2]
                camera_bp.set_attribute('fov', fov_value)
                camera = world.spawn_actor(camera_bp, cam_transform, attach_to=b1)
                camera.listen(camera_list_images.put)

            if keys[pygame.constants.K_v]:
                camera_list_images = queue.Queue()
                camera.destroy()
                fov_value = use_this_fov[3]
                camera_bp.set_attribute('fov', fov_value)
                camera = world.spawn_actor(camera_bp, cam_transform, attach_to=b1)
                camera.listen(camera_list_images.put)

            if keys[pygame.constants.K_b]:
                camera_list_images = queue.Queue()
                camera.destroy()
                fov_value = use_this_fov[4]
                camera_bp.set_attribute('fov', fov_value)
                camera = world.spawn_actor(camera_bp, cam_transform, attach_to=b1)
                camera.listen(camera_list_images.put)

            if change == True:
                print(str(transform) + " " + "end")
                if fine_control:
                    t = threading.Timer(0.3, task)
                    t.start()
                else:
                    change = False
                actor.set_transform(transform)

        keys = pygame.key.get_pressed()

        if keys[pygame.constants.K_1]:
            mode_control = 1

        if keys[pygame.constants.K_2]:
            mode_control = 2

        if mode_control == 2:
            if (car_actor is not None):
                controls(car_actor.get_transform(), car_actor)  # car
        elif mode_control == 1:
            controls(b1.get_transform(), b1)  # box
        elif mode_control == 3:
            if (car_actor is not None):
                controls(car_actor.get_transform(), car_actor)  # car

        if keys[pygame.constants.K_3] or keys[pygame.constants.K_4] or keys[pygame.constants.K_5] or keys[
            pygame.constants.K_6]:
            actor_spawn_element = ""
            if keys[pygame.constants.K_3]:
                actor_spawn_element = "carlacola"
            if keys[pygame.constants.K_4]:
                actor_spawn_element = "yamaha"
            if keys[pygame.constants.K_5]:
                actor_spawn_element = "model3"
            if keys[pygame.constants.K_6]:
                actor_spawn_element = "mustang"

            if True:
                carr = blueprint_library.filter(actor_spawn_element)[0]
                fov_index = 0
                if fov_value == use_this_fov[0]:
                    fov_index = 0
                elif fov_value == use_this_fov[1]:
                    fov_index = 1
                elif fov_value == use_this_fov[2]:
                    fov_index = 2

                active_car_pos_place = list_use_car_location[target_counter][fov_index]
                active_car_pos = active_car_pos_place[0]
                dir_vector = active_car_pos_place[1]
                temp_transform = carla.Transform(
                    Location(active_car_pos.location.x, active_car_pos.location.y, active_car_pos.location.z + 40),
                    Rotation(active_car_pos.rotation.pitch, active_car_pos.rotation.yaw, active_car_pos.rotation.roll))
                local_car_actor = world.spawn_actor(carr, temp_transform)
                local_car_actor.set_light_state(
                    carla.VehicleLightState(carla.VehicleLightState.NONE | carla.VehicleLightState.LowBeam))
                local_car_actor.set_simulate_physics(False)

                # do not use list_use_car_translate
                offset_vec = carla.Location(0, 0, 0)
                for ele in list_actor_group:
                    ext2 = ele.bounding_box.extent.x * 2
                    ext2 += 2  # 2 meter abstand
                    offset_vec.x +=  (dir_vector.x * ext2)
                    offset_vec.y +=  (dir_vector.y * ext2)
                    offset_vec.z +=  (dir_vector.z * ext2)

                ext1 = local_car_actor.bounding_box.extent.x
                temp_transform = carla.Transform(
                    Location(active_car_pos.location.x + offset_vec.x + (dir_vector.x * ext1),
                             active_car_pos.location.y + offset_vec.y+ (dir_vector.y * ext1),
                             active_car_pos.location.z ),
                    Rotation(active_car_pos.rotation.pitch, active_car_pos.rotation.yaw, active_car_pos.rotation.roll))

                local_car_actor.set_transform(temp_transform)
                list_actor_group.append(local_car_actor)
                print("yes")
                print(temp_transform)
             #   print(b1.get_transform())
            time.sleep(0.3)

        if keys[pygame.constants.K_COMMA]:
            if len(list_actor_group) != 0:
                temp_loc_actor = list_actor_group[-1]
                bb = temp_loc_actor.bounding_box
                forward_vec = b1.get_transform().get_forward_vector()

                ray = temp_loc_actor.get_transform().location - b1.get_transform().location
                if dot(forward_vec, ray) > 1:
                    p1 = get_image_point(bb.location, K, world_2_camera)
                    verts = [v for v in bb.get_world_vertices(temp_loc_actor.get_transform())]
                    x_max = -10000
                    x_min = 10000
                    y_max = -10000
                    y_min = 10000
                    for vert in verts:
                        p = get_image_point(vert, K, world_2_camera)
                        # Find the rightmost vertex
                        if p[0] > x_max:
                            x_max = p[0]
                        # Find the leftmost vertex
                        if p[0] < x_min:
                            x_min = p[0]
                        # Find the highest vertex
                        if p[1] > y_max:
                            y_max = p[1]
                        # Find the lowest  vertex
                        if p[1] < y_min:
                            y_min = p[1]

                    val_x = " " + str((x_max - x_min) / float(image_w))
                    val_y = " " + str((y_max - y_min) / float(image_h))
                    print(val_x + "   " + val_y)

        if keys[pygame.constants.K_m]:
            for ele in list_actor_group:
                ele.destroy()
            list_actor_group = []

        if keys[pygame.constants.K_o]:
            if (car_actor is not None):
                car_actor.destroy()
            carr = blueprint_library.filter("yamaha")[0] # model3

            fov_index = 0
            if fov_value == use_this_fov[0]:
                fov_index = 0
            elif fov_value == use_this_fov[1]:
                fov_index = 1
            elif fov_value == use_this_fov[2]:
                fov_index = 2

            active_car_pos_place = list_use_car_location[target_counter][fov_index]

            active_car_pos = active_car_pos_place[0]

            dir_vector = active_car_pos_place[1]

            #   active_car_pos = list_use_car_location[total_car_id]
            temp_transform = carla.Transform(
                Location(active_car_pos.location.x, active_car_pos.location.y, active_car_pos.location.z + 8),
                Rotation(active_car_pos.rotation.pitch, active_car_pos.rotation.yaw, active_car_pos.rotation.roll))
            car_actor = world.spawn_actor(carr, temp_transform)

            car_actor.set_light_state(
                carla.VehicleLightState(carla.VehicleLightState.NONE | carla.VehicleLightState.LowBeam))
            # car_actor.set_light_state(carla.VehicleLightState.Position | carla.VehicleLightState.LowBeam) # HighBeam  Fog

            # car_actor.set_light_state(carla.VehicleLightState(carla.VehicleLightState.Position | carla.VehicleLightState.LowBeam))
            car_actor.set_simulate_physics(False)
            offset_vec = carla.Location(dir_vector.x, dir_vector.y, dir_vector.z)
            ext1 = car_actor.bounding_box.extent.x
            temp_transform = carla.Transform(
                Location(active_car_pos.location.x + (dir_vector.x * ext1),
                         active_car_pos.location.y  + (dir_vector.y * ext1),
                         active_car_pos.location.z + offset_vec.z),
                Rotation(active_car_pos.rotation.pitch, active_car_pos.rotation.yaw, active_car_pos.rotation.roll))
            car_actor.set_transform(temp_transform)
            print(active_car_pos)
            print(temp_transform)

        if keys[pygame.constants.K_i]:
            if (car_actor is not None):
                car_actor.destroy()
            carr = blueprint_library.filter("model3")[0]
            print(car_transform)
            car_transform = carla.Transform()
            car_transform.location.x = b1.get_transform().location.x
            car_transform.location.y = b1.get_transform().location.y
            car_transform.location.z = b1.get_transform().location.z + 20

            car_actor = world.spawn_actor(carr, car_transform)

            car_actor.set_light_state(
                carla.VehicleLightState(carla.VehicleLightState.NONE | carla.VehicleLightState.LowBeam))
            # car_actor.set_light_state(carla.VehicleLightState.Position | carla.VehicleLightState.LowBeam) # HighBeam  Fog

            # car_actor.set_light_state(carla.VehicleLightState(carla.VehicleLightState.Position | carla.VehicleLightState.LowBeam))
            car_actor.set_simulate_physics(False)

        if keys[pygame.constants.K_n]:
            if (car_actor is not None):
                car_actor.set_simulate_physics(True)

        if keys[pygame.constants.K_p]:
            name_pic = town_map + "C" + str(list_counter) + " "+ str(intra_counter)+ "F" + fov_value
            result = cv2.imwrite("vehicle_data2\\" + str(count_id) + name_pic + ".jpeg", img,
                                 [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            count_id += 1
            time.sleep(0.3)

        if keys[pygame.constants.K_l]:
            if (car_actor is not None):

                get_tr = car_actor.get_transform()
                car_trans = carla.Transform(carla.Location(get_tr.location.x, get_tr.location.y, get_tr.location.z),
                                            carla.Rotation(get_tr.rotation.pitch, get_tr.rotation.yaw,
                                                           get_tr.rotation.roll))

                yaw_value = int(round(car_trans.rotation.yaw, -1))
                ext1 = car_actor.bounding_box.extent.x
                dir_vec = carla.Location(0, 0, 0)
                if yaw_value == 0:
                    dir_vec.x = -1
                elif yaw_value == 180 or yaw_value == -180:
                    dir_vec.x = 1
                elif yaw_value == 90 or yaw_value == -270:
                    dir_vec.y = -1
                elif yaw_value == -90 or yaw_value == 270:
                    dir_vec.y = 1

                car_trans.location.x += dir_vec.x * -ext1
                car_trans.location.y += dir_vec.y * -ext1

                print("[" + str(car_trans) + "," + str(dir_vec) + "],")

                time.sleep(0.3)


        if keys[pygame.constants.K_7]:
            if car_actor is not None:
                car_actor.destroy()
            carr = blueprint_library.filter("walker.pedestrian.0025")[0]

            fov_index = 0
            if fov_value == use_this_fov[0]:
                fov_index = 0
            elif fov_value == use_this_fov[1]:
                fov_index = 1
            elif fov_value == use_this_fov[2]:
                fov_index = 2

            active_car_pos = list_use_car_location[target_counter][fov_index]
            active_car_pos = active_car_pos[0]

            #   active_car_pos = list_use_car_location[total_car_id]
            temp_transform = carla.Transform(
                Location(active_car_pos.location.x, active_car_pos.location.y, active_car_pos.location.z + 40),
                Rotation(active_car_pos.rotation.pitch, active_car_pos.rotation.yaw, active_car_pos.rotation.roll))
            car_actor = world.spawn_actor(carr, temp_transform)
            car_actor.set_simulate_physics(False)
            temp_transform.location.z -= 40
            car_actor.set_transform(temp_transform)
            mode_control = 3

        if keys[pygame.constants.K_8]:

            intra_counter -= 1
            target_counter -= 1
            if intra_counter < 0:
                list_counter -= 1
                if list_counter < 0:
                    list_counter = 0
                    intra_counter = 0
                    target_counter += 1
                else:
                    intra_counter = len(list_use_cam_location[list_counter])-1

            b1.set_transform(list_use_cam_location[list_counter][intra_counter])
            time.sleep(0.3)

        if keys[pygame.constants.K_9]:

            intra_counter+=1
            target_counter += 1
            if intra_counter >= len(list_use_cam_location[list_counter]):
                list_counter+=1
                if list_counter >= len(list_use_cam_location):
                    list_counter-=1
                    intra_counter-=1
                    target_counter-=1
                else:
                    intra_counter=0

            b1.set_transform(list_use_cam_location[list_counter][intra_counter])

            """

            cam_loc_temp_here =  list_use_cam_location[list_counter][intra_counter]
            cam_x = cam_loc_temp_here.location.x
            cam_y = cam_loc_temp_here.location.x

            stuff = world.get_environment_objects()

            for ele in stuff:
                if ele.transform.location.x> cam_x-10 and  ele.transform.location.x < cam_x +10:
                    if ele.transform.location.y > cam_y - 10 and ele.transform.location.y < cam_y + 10:
                        print(ele)
                        print(str(ele.id))
                        print(ele.name)
                        print(ele.type)
                        print(ele.transform)
                        
            # 15654913596427552062
            """

            time.sleep(0.3)

        def set_wea_op(weather):
            nonlocal cam_pos_num
            nonlocal camera_list_images
            nonlocal camera
            nonlocal camera_bp
            nonlocal car_transform
            if keys[pygame.constants.K_KP1]:
                weather.sun_altitude_angle = -10
            if keys[pygame.constants.K_KP2]:
                weather.sun_altitude_angle = 50
            if keys[pygame.constants.K_KP3]:
                weather.fog_density = 40
            if keys[pygame.constants.K_KP4]:
                weather.fog_density = 60
            if keys[pygame.constants.K_KP5]:
                weather.fog_density = 100
            if keys[pygame.constants.K_KP6]:
                weather.precipitation = 100

            if keys[pygame.constants.K_KP7]:
                weather.dust_storm = 30
            if keys[pygame.constants.K_KP8]:
                weather.dust_storm = 60
            if keys[pygame.constants.K_KP9]:
                weather.dust_storm = 100
            if keys[pygame.constants.K_KP0]:
                weather.dust_storm = 0
            if keys[pygame.constants.K_KP_MULTIPLY]:
                pass

        weather = world.get_weather()
        set_wea_op(weather)
        world.set_weather(weather)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', type=str, default="train", help='test train  für town01 town03')

    opt = parser.parse_args()
    task = opt.task
    print(opt)
    ttc=3

    if task=="train":
        ttc=3
    elif task=="test":
        ttc=1

    try:
        address = "localhost"
        address_network = "192.168.1.110"
        client = carla.Client(address, 2000)
        client.set_timeout(15.0)
        print(client.get_available_maps())
        main(client,ttc)
    finally:
        print("exit")
        world = client.load_world('Town03')
