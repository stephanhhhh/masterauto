# to generate test and training data

import queue
import numpy as np
import time
import random
from random import randint
import cv2
import argparse
import central_data as central
from central_data import carla
# import carla
from carla import Transform, Location, Rotation


def task(name, img, file_name, content):
    result = cv2.imwrite(name, img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    with open(file_name, 'w') as f:
        f.write(content)

def calculate_bounding_box_2d(car_type, the_car, the_camera, K, alternate_bb_verts, alternate_car_transform):
    world_2_camera = np.array(the_camera.get_transform().get_inverse_matrix())
    parent = the_camera.parent

    x_max = -10000
    x_min = 10000
    y_max = -10000
    y_min = 10000

    # betrachte nur autos vor der kamera. ist immer gegeben.
    forward_vec = parent.get_transform().get_forward_vector()
    ray = the_car.get_transform().location - parent.get_transform().location
    if central.dot(forward_vec, ray) > 1:
        # p1 = central.get_image_point(bb.location, K, world_2_camera)

        error_verts = False
        bb = the_car.bounding_box
        verts = [v for v in
                 bb.get_world_vertices(the_car.get_transform())]

        # ein bug in der simulation: gewisse objekte, fast nur 2 räder haben falsche bounding boxes höhe 0 manchmal

        test_vert33 = verts[0]
        for vert_index, vert in enumerate(verts):
            if vert_index == 0:
                continue
            if test_vert33.x == vert.x and test_vert33.y == vert.y and test_vert33.z == vert.z:
                #   print("error in verts detected  use alternative "+str(frame_count_num) )
                error_verts = True
                break

        if error_verts:
            if car_type != "1":  # this si label based. 0 =cars 1 = bikes
                print("deep error. different type verts off " + str(car_type))
            car_act_1_loc = alternate_car_transform.location  # pre calculated car
            car_act_2_loc = the_car.get_location()  # the car
            directed_vector = carla.Location(x=car_act_2_loc.x - car_act_1_loc.x,
                                             y=car_act_2_loc.y - car_act_1_loc.y,
                                             z=car_act_2_loc.z - car_act_1_loc.z)

            verts = [carla.Location(x=v.x + directed_vector.x,
                                    y=v.y + directed_vector.y,
                                    z=v.z + directed_vector.z)
                     for v in alternate_bb_verts]

            #    print(car_act_1_loc)
            #    print(car_act_2_loc)
            #    print(directed_vector)

            test_vert33 = verts[0]
            for vert_index, vert in enumerate(verts):
                if vert_index == 0:
                    continue
                if test_vert33.x == vert.x and test_vert33.y == vert.y and test_vert33.z == vert.z:
                    print("error in verts detected  Big No")
                    break

        for vert in verts:
            #  print(vert)
            p = central.get_image_point(vert, K, world_2_camera)
            #  print(p)
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

        return [x_min, x_max, y_min, y_max]
    return None

def main(client,ttc,path):
    print(client.get_available_maps())
    base_path = central.main_path  # rel_path
    all_cars_list_in_use = central.all_cars_lists_true  # all_cars_lists_old

    base_path = path

    if central.new_version == "1":   # falls alte carla version genutzt wird
        all_cars_list_in_use = central.all_cars_lists_old
        #base_path = central.rel_path

    print(base_path)

    # testdaten oder trainings daten erzeugen auswahl
    type_town_command = ttc ## 1 oder 3 für test und train town01 und town03

    file_ending_image = ".jpeg"

    world = None
    if type_town_command == 3:
        random.seed(3781102)
        world = client.load_world('Town03')
        print("Town03 Training")
    else:
        random.seed(148280)
        world = client.load_world('Town01')
        print("Town01 Test")

    settings = world.get_settings()
    frame = world.apply_settings(carla.WorldSettings(
        no_rendering_mode=False,
        synchronous_mode=True,
        fixed_delta_seconds=0.1))  # 1.0 / 60))

    blueprint_library = world.get_blueprint_library()
    # create object and camera
    box = blueprint_library.filter("box01")[0]


    up_translate = 40

    camera_bp = blueprint_library.find('sensor.camera.rgb')
    camera_bp.set_attribute('image_size_x', str(central.picture_size[0]))
    camera_bp.set_attribute('image_size_y', str(central.picture_size[1]))
    camera_bp.set_attribute('fov', "40")
    cam_transform = carla.Transform(carla.Location(x=1.0, z=0))



    """

    the_box = world.spawn_actor(box, carla.Transform(carla.Location(x=246.709337, y=-13.22, z=0.09 + 100),
                                               carla.Rotation(pitch=0.0, yaw=-90.0, roll=0.000000)))

    camera_bp = blueprint_library.find('sensor.camera.rgb')
    camera_bp.set_attribute('image_size_x', str(central.picture_size[0]))
    camera_bp.set_attribute('image_size_y', str(central.picture_size[1]))
    camera_bp.set_attribute('fov', "40")
    cam_transform = carla.Transform(carla.Location(x=1.0, z=0))
    camera_element = world.spawn_actor(camera_bp, cam_transform, attach_to=the_box)
    camera_queue_images = queue.Queue()
    camera_element.listen(camera_queue_images.put)

    
    list_of_all_cameras = []
    camera_list_images = []

    camera_list_images.clear()
    list_of_all_cameras.clear()

    for i in central.fov_list:
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', str(central.picture_size[0]))
        camera_bp.set_attribute('image_size_y', str(central.picture_size[1]))
        camera_bp.set_attribute('fov', str(i))
        cam_transform = carla.Transform(carla.Location(x=1.0, z=0))
        camera2 = world.spawn_actor(camera_bp, cam_transform, attach_to=the_box)
        list_of_all_cameras.append(camera2)
        new_cam_queue = queue.Queue()
        camera2.listen(new_cam_queue.put)
        camera_list_images.append(new_cam_queue)
    """

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

    world.set_weather(weather)

    env_objs = world.get_environment_objects(carla.CityObjectLabel.Vehicles)
    list_env_del = [ele.id for ele in env_objs]
    world.enable_environment_objects(list_env_del, False)

    frame_count_num = 0

    rand_numbers_list = []
    rand_numbers_list = random.sample(range(0, 50000), 40000)
   # rand_numbers_list = random.sample(range(50000, 70000), 15000)

    list_use_car_location = central.car_pos_targets_t1
    list_use_cam_location = central.cam_pos_t1_c

    list_cars_opponent = central.car_pos_opposite_t3
    positions_walkers = central.positions_walkers_t3

    type_te_tr = "train"

    saved_bb_type2 = []

    list_cars_this = []

    second_test = False
    fov_list = []


    if type_town_command == 3:
        positions_walkers = central.positions_walkers_t3
        list_cars_opponent = central.car_pos_opposite_t3
        list_use_car_location = central.car_pos_targets_t3
        list_use_cam_location = central.cam_pos_t3_c
        list_cars_this = central.list_cars_this_train
        fov_list=central.fov_list_train
        type_te_tr = "train"
    else:
        positions_walkers = central.positions_walkers_t1
        list_cars_opponent = central.car_pos_opposite_t1
        list_use_car_location = central.car_pos_targets_t1
        list_use_cam_location = central.cam_pos_t1_c
        list_cars_this = central.list_cars_this_test
        fov_list = central.fov_list_test
        type_te_tr = "test"

        second_test = False  # vlt. second test data set with all cars

        if second_test:
            list_cars_this = all_cars_list_in_use

    if central.new_version == "1":
        list_cars_this = central.all_cars_lists_old
        if type_town_command == 3:
            list_cars_this = central.cars_old_train
        else:
            list_cars_this = central.cars_old_test

    height_offset = 40
    location_string=[]

    pro_mat_k = [
        central.build_projection_matrix(central.picture_size[0], central.picture_size[1], fov_list[0]),
        central.build_projection_matrix(central.picture_size[0], central.picture_size[1], fov_list[1]),
        central.build_projection_matrix(central.picture_size[0], central.picture_size[1], fov_list[2]),
    ]

    # boxen, welche die kameras halten, werden hier erzeugt
    boxes = []
    for index_cam_loc, ele in enumerate(list_use_cam_location):
        the_box = world.spawn_actor(box, carla.Transform(
            carla.Location(x=246.709337, y=-13.22, z=0.09 + (33 + (index_cam_loc * 20))),
            carla.Rotation(pitch=0.0, yaw=-90.0, roll=0.000000)))
        boxes.append(the_box)

    list_actors_target = []
    list_all_actors = []

    alternate_car = carla.Transform(Location(0, 0, 120), Rotation(0, 0, 0))  # always same place
    saved_bb_type2_cars_transform = []

    # wegen bug in simulation werden hier die werte für die motorräder gespeichert
    for bikes in list_cars_this[2]:
        new_list_bb = []
        new_list_bb_cars = []
        bb_rotations = [0, 90, 180, -90]
        for bb_rota in bb_rotations:
            this_bp = blueprint_library.filter(bikes)[0]
            this_actor = world.spawn_actor(this_bp, carla.Transform(Location(0, 0, 120), Rotation(0, bb_rota, 0)))
            this_actor.set_light_state(
                carla.VehicleLightState(carla.VehicleLightState.NONE | carla.VehicleLightState.LowBeam))
            this_actor.set_simulate_physics(False)

            try:
                world.tick(2)
                world.tick(2)
            except:
                print("WARNING: tick not received w")

            this_bb = this_actor.bounding_box
            new_list_bb.append(this_bb)
            new_list_bb_cars.append(this_actor.get_transform())

            this_actor.destroy()
            try:
                world.tick(2)
            except:
                print("WARNING: tick not received w")

        saved_bb_type2.append(new_list_bb)
        saved_bb_type2_cars_transform.append(new_list_bb_cars)

    # erzeuge fußgänger
    for walker_list in positions_walkers:
        for walker in walker_list:
            temp_transform = carla.Transform(
                Location(walker.location.x, walker.location.y,
                         walker.location.z),
                Rotation(walker.rotation.pitch,
                         walker.rotation.yaw,
                         walker.rotation.roll))
            walker_bp = random.choice(world.get_blueprint_library().filter("walker.pedestrian.*"))
            #    walker_bp = blueprint_library.filter("walker.pedestrian.0025")[0]
            temp_transform.location.z += height_offset
            walker_actor = world.spawn_actor(walker_bp, temp_transform)
            walker_actor.set_simulate_physics(False)
            temp_transform.location.z -= height_offset
            walker_actor.set_transform(temp_transform)

    list_cameras = []
    list_images = []

    total_count_removed = 0
    total_count_cars_labeled = 0
    total_count_bike_labeled = 0
    total_count_lkw_labeled = 0


    while (True):
        start_total = time.time()

        # weather fist
        for c_w, weather_data in enumerate(central.weather_settings):

            if type_town_command==1 and ( c_w==6 or c_w==7):
                continue  # weniger daten für test daten
            count_removed=0
            count_cars_labeled=0
            count_bike_labeled=0
            count_lkw_labeled=0
         #   if c_w<4:
         #       continue
            start_w = time.time()
            string_weather = "W" + str(c_w) + "_"

            print("Progress: " + str(c_w + 1) + "|" + str(len(central.weather_settings)))

            #rand_numbers_list = random.sample(range(c_w *10000, ((c_w+1)*10000) ), 9000)

            world.set_weather(central.weather_reset)
            world.set_weather(weather_data)
            for i_counter in range(0, 50):
                try:
                    world.tick(2)
                except:
                    print("WARNING: tick not received w")

            for fov_index, fov_this in enumerate(fov_list):
                camera_string = "C" + str(fov_this) + "_"

                for cam in list_cameras:
                    if cam is not None:
                        try:
                            cam.destroy()
                        finally:
                            pass
                list_cameras = []
                list_images = []
                #if fov_index == 2:
                #    continue

                for index_cam_loc, ele in enumerate(list_use_cam_location):
                    camera_bp.set_attribute('fov', str(fov_this))
                    camera_element = world.spawn_actor(camera_bp, cam_transform, attach_to=boxes[index_cam_loc])
                    camera_queue_images = queue.Queue()
                    camera_element.listen(camera_queue_images.put)

                    list_cameras.append(camera_element)
                    list_images.append(camera_queue_images)

                # to give cameras time to get good image quality
                for i_counter in range(0, 19):
                    try:
                        world.tick(2)
                    except:
                        print("WARNING: tick not received w")

                # cameras und positionen werden vorbereitet und asugewählt
                for cccc in range(0, 100):
                    list_pos_targets_opposite = []
                    sum_lists = 0
                    for total_car_id, cam_lists in enumerate(list_use_cam_location):

                        if cccc < len(cam_lists):
                            list_pos_targets_opposite.append(
                                [cam_lists[cccc],
                                 list_use_car_location[sum_lists + cccc][fov_index],
                                 list_cars_opponent[sum_lists + cccc]])
                        else:
                            list_pos_targets_opposite.append(None)
                        sum_lists += len(cam_lists)

                    ende = True
                    for d_ele in list_pos_targets_opposite:
                        if d_ele is not None:
                            ende = False
                            break
                    if ende:
                        break

                    # fix cams:
                    for d_ele_index, d_ele in enumerate(list_pos_targets_opposite):
                        if d_ele is None:
                            if list_cameras[d_ele_index] is not None:
                                try:
                                    list_cameras[d_ele_index].destroy()
                                    list_cameras[d_ele_index] = None
                                    list_images[d_ele_index] = None
                                finally:
                                    pass

                    for index_class_list, class_list in enumerate(list_cars_this):

                        string_car_type = "T" + str(index_class_list - 1) + "_"
                        if index_class_list == 0:
                            string_car_type = "T9_"  # this means empty no labels
                        if index_class_list == 4:
                            string_car_type = "T8_"  # this means empty no labels

                        if False  and index_class_list==4:  # optional falls farräder raus sollen
                            continue

                        if (c_w == 1 or c_w ==4  or c_w ==6) and (index_class_list !=0 ):
                            continue # we want here more empty images these weather opitons only exsit for empty images. so keep this

                        for index_car_names, actor_name in enumerate(class_list):
                            for i in range(0, 5):  # variation loop

                                for act in list_all_actors:
                                    act.destroy()

                                list_all_actors = []

                                target_labels = []
                                alternatives = []
                                list_actor_targets = []

                                # Reduktion der Bilder, falls alle Fahrzeuge benutzt werden sollten
                                if second_test and i == 2 and index_class_list == 1:
                                    continue

                                if (index_class_list == 0 and i > 0  and not (c_w == 1 or c_w ==4  or c_w ==6) )  or  ( index_class_list == 0 and i>2 ):
                                    break

                                if index_class_list == 4 and i > 1:
                                    break

                                if index_class_list == 1 and i >= 3:
                                    break

                                for d_ele_index, d_ele in enumerate(list_pos_targets_opposite):
                                    target_labels.append([])
                                    alternatives.append([])
                                    list_actor_targets.append([])

                                location_string = []


                                for d_ele_index, d_ele in enumerate(list_pos_targets_opposite):
                                    locs = "L" + str(d_ele_index) + "_"

                                    location_string.append(locs)

                                    if d_ele is None:
                                        continue

                                    this_pos_box = d_ele[0]

                                    opposite_traffic = d_ele[2]
                                    opposite_traffic_spawn = opposite_traffic[0]
                                    opposite_traffic_dir = opposite_traffic[1]

                                    car_pos_list_unit = d_ele[1]
                                    car_position_spawn = car_pos_list_unit[0]
                                    car_vector = car_pos_list_unit[1]

                                    temp_transform = carla.Transform(
                                        Location(car_position_spawn.location.x, car_position_spawn.location.y,
                                                 car_position_spawn.location.z),
                                        Rotation(car_position_spawn.rotation.pitch,
                                                 car_position_spawn.rotation.yaw,
                                                 car_position_spawn.rotation.roll))

                                    # set box camrea location but with added randomnes
                                    modified_cam_location = Transform(
                                        Location(this_pos_box.location.x, this_pos_box.location.y,
                                                 this_pos_box.location.z),
                                        Rotation(this_pos_box.rotation.pitch, this_pos_box.rotation.yaw,
                                                 this_pos_box.rotation.roll))

                                    # camera wiggle. autos sind immer ncoh alle gut sichtbar
                                    modified_cam_location.rotation.roll += random.uniform(-3, 3)
                                    modified_cam_location.rotation.pitch += random.uniform(-1.2, 1.2)

                                    if d_ele_index != 5 and type_town_command==3:
                                        modified_cam_location.rotation.yaw += random.uniform(-0.8, 0.8)
                                        modified_cam_location.location.x += random.uniform(-0.2, 0.2)
                                        modified_cam_location.location.y += random.uniform(-0.2, 0.2)
                                        modified_cam_location.location.z += random.uniform(-0.2, 0.2)

                                    boxes[d_ele_index].set_transform(modified_cam_location)
                                    # list_cameras[d_ele_index].set_transform(modified_cam_location)

                                    yes_counter_traffic = (randint(1, 100) > 5)
                                    if index_class_list == 0 and (index_car_names < len(class_list) - 1):
                                        yes_counter_traffic = False

                                    # no counter traffic
                                    yes_counter_traffic = False

                                    modify_trucks = -1
                                    empties = 0

                                    last_int_val=-1
                                    for i2 in range(0, 4):  # 4 car positions extra

                                        next_car = actor_name
                                        next_car_id_value = index_car_names

                                #        if index_class_list == 0 and i2 > 0:
                                #            break
                                        int_val = index_class_list

                                        if i2 != 0:
                                            int_val = randint(0, 4)


                                            if index_class_list==0:
                                                int_val = index_class_list

                                            if index_class_list!=0 and int_val == 4:  # weniger farräder
                                                int_val = randint(0, 4)


                                            if index_class_list!=0 and (empties == 1 or i2 == 3):  # die letzte Position sollte nie leer sein.
                                                int_val = randint(1, 2)
                                                if int_val == 2: # letzte Position keine Farräder oder Motorräder
                                                    int_val = 3

                                            if int_val==4 and i2==2 and index_class_list!=0: # keine farräder an position 3
                                                int_val= randint(1,3)

                                            # todo or: we say variation loop 1 gets  1 class only and 2 3 4 get form ahc class one instnance to get mroe equal field always?


                                            if not (int_val==2 and i2==2 and (last_int_val==2 or last_int_val==4)):
                                                pass # TODO vlt. motorräder an position 3 verbieten, oder nur erlauben wenn vorher ein motorrad oder farrad war


                                            if int_val==1 and i2==1:
                                                roll_prob = randint(1,5) # 20% chance für motorrad anstelle von auto
                                                if roll_prob == 1:
                                                    int_val=2

                                            # extra motorräder, aber nicht in den speziellen wetter kategorien, da diese nur für komplett leere bilder da sind
                                            if not (c_w == 1 or c_w == 4 or c_w == 6) and index_class_list==0 and i2 == 2  and type_town_command == 3:
                                                int_val = randint(0, 4)  # 20% chance to be motorrad at pos 3
                                                int_val = 2* int((int_val//4))

                                            if i2==3 and int_val==2 or int_val==4: # letze position ist im normalfall kein motorrad
                                                int_val = randint(1, 2)
                                                if int_val==2:
                                                    int_val=3



                                            if modify_trucks == -1 and int_val == 3 and i2 != 3:
                                                modify_trucks = 1
                                                int_val = randint(1, 2)

                                            if modify_trucks == 1 and i2 == 3: # letzte position ein lwk teilweise
                                                int_val = 3

                                            if i==3:
                                                int_val = index_class_list
                                                if i2==3 and index_class_list==2:
                                                    int_val = randint(2,3)
                                                    if int_val==2:
                                                        int_val=1

                                            next_car_list = list_cars_this[int_val]
                                            if int_val == 0 and index_class_list!=0:
                                                empties = 1
                                                temp_transform.location.x += (car_vector.x * 4)
                                                temp_transform.location.y += (car_vector.y * 4)
                                                continue
                                            next_car_id_value = randint(0, len(next_car_list) - 1)
                                            next_car = next_car_list[next_car_id_value]

                                        car_bp = blueprint_library.filter(next_car)[0]

                                        if next_car.__contains__("walker"):
                                            temp_transform.location.z += 1

                                        temp_transform.location.z += height_offset

                                        temp_transform.rotation.yaw +=  random.uniform(-1.6, 1.6)

                                        local_car_actor = world.spawn_actor(car_bp, temp_transform)
                                        local_car_actor.set_simulate_physics(False)

                                        list_all_actors.append(local_car_actor)

                                        ext1 = local_car_actor.bounding_box.extent.x

                                        # behebe schlechte bounding box
                                        if int_val == 2:
                                            some_yaw_val = local_car_actor.get_transform().rotation.yaw / 90
                                            int_index = int(round(some_yaw_val))
                                            if int_index < 0:
                                                if int_index == -1:
                                                    int_index = 3
                                                elif int_index == -2:
                                                    int_index = 2
                                                elif int_index == -3:
                                                    int_index = 1
                                                else:
                                                    print("error never happens 3422112")
                                            primary_bb = saved_bb_type2[next_car_id_value][int_index]
                                            ext1 = primary_bb.extent.x

                                            alternate_car_transform = saved_bb_type2_cars_transform[next_car_id_value][
                                                int_index]

                                            primary_bb_verts = primary_bb.get_world_vertices(alternate_car_transform)
                                            alternate_bb = primary_bb_verts

                                            alternatives[d_ele_index].append([alternate_car_transform, alternate_bb])

                                        if int_val != 4 and int_val != 0:

                                            if int_val != 2:
                                                alternatives[d_ele_index].append([None, None])

                                            target_labels[d_ele_index].append(str(int_val - 1))
                                            list_actor_targets[d_ele_index].append(local_car_actor)

                                            local_car_actor.set_light_state(carla.VehicleLightState(
                                                carla.VehicleLightState.NONE | carla.VehicleLightState.LowBeam))

                                        temp_transform.location.z -= height_offset
                                        temp_transform.location.x += (car_vector.x * ext1)
                                        temp_transform.location.y += (car_vector.y * ext1)

                                        local_car_actor.set_transform(temp_transform)

                                        temp_transform.rotation.yaw = car_position_spawn.rotation.yaw

                                        # Fußgänger z Wert ist andes als bei Autos
                                        if next_car.__contains__("walker"):
                                            temp_transform.location.z -= 1

                                        # offset car  spawn
                                        temp_transform.location.x += (car_vector.x * ext1)
                                        temp_transform.location.y += (car_vector.y * ext1)
                                        # 4 to high mabye. extend is half. so 2 emtres effctively. and test htis out maybe. extract to function amybe? TODO
                                        temp_transform.location.x += (4 * car_vector.x)
                                        temp_transform.location.y += (4 * car_vector.y)


                                    # then opoosite
                                    prepare_opposite(yes_counter_traffic, list_cars_this, opposite_traffic_spawn,
                                                     blueprint_library, height_offset, opposite_traffic_dir,
                                                     saved_bb_type2, list_all_actors)

                                try:
                                    world.tick(2)
                                    world.tick(2)
                                    world.tick(2)

                                except:
                                    print("WARNING: tick not received w")

                                for cam_index, cam_valie in enumerate(list_cameras):
                                    camera = cam_valie
                                    if camera is None or list_pos_targets_opposite[cam_index] is None:
                                        continue

                                    image_queue = list_images[cam_index]
                                    while image_queue.qsize() != 0:
                                        image_queue.get()

                                    # verdeckte autos löschen
                                    targets = list_actor_targets[cam_index]
                                    labels = target_labels[cam_index]
                                    alternates = alternatives[cam_index]

                                   # print("---")
                                   # print(str( len(targets) )  +  str( len(labels) )  + str( len(alternates) ))
                                   # for ele in labels:
                                   #     print(str(ele))


                                    list_to_mod = save_labels(True,"", "", labels, targets, camera, fov_index, alternates,
                                                pro_mat_k)

                                    count_removed+=len(list_to_mod[0])
                                    for act in list_to_mod[0]:
                                        act.destroy()
                                        list_all_actors.remove(act)

                                    target_labels[cam_index] = list_to_mod[1]
                                    alternatives[cam_index] = list_to_mod[2]

                                    targets = list_actor_targets[cam_index]
                                    labels = target_labels[cam_index]
                                    alternates = alternatives[cam_index]

                                try:
                                    world.tick(2)
                                    world.tick(2)
                                    world.tick(2)

                                except:
                                    print("WARNING: tick not received w")


                                for cam_index, cam_valie in enumerate(list_cameras):
                                    camera = cam_valie

                                    if camera is None or list_pos_targets_opposite[cam_index] is None:
                                        continue

                                    image_queue = list_images[cam_index]
                                    data = None
                                    # get latest image
                                    while image_queue.qsize() != 0:
                                        data = image_queue.get()

                                    img = np.reshape(np.copy(data.raw_data), (data.height, data.width, 4))
                                    # mofiziere bildgröße. schneide bereich aus
                                    img = img[80:, 0:640]

                                    label_path = base_path + "labels\\" + type_te_tr + "\\"
                                    frame_path = base_path + "images\\" + type_te_tr + "\\"
                                    frame_count_num += 1

                                    frame_c_n_str = str(rand_numbers_list[frame_count_num])  # str(frame_count_num)
                                    add_zeroes = ""
                                    for kk in range(0, 6 - len(frame_c_n_str)):
                                        add_zeroes += "0"

                                    file_name = add_zeroes + frame_c_n_str + "_" + string_weather + string_car_type + location_string[cam_index] + camera_string
                                    result = cv2.imwrite(frame_path + file_name + file_ending_image, img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

                                    targets = list_actor_targets[cam_index]
                                    labels = target_labels[cam_index]
                                    alternates = alternatives[cam_index]



                                    log_data = save_labels(False,label_path, file_name, labels, targets, camera, fov_index, alternates,pro_mat_k)

                                    count_cars_labeled += log_data[0]
                                    count_bike_labeled += log_data[1]
                                    count_lkw_labeled += log_data[2]

            # logging
            end_w = time.time()
            total_count_removed += count_removed
            total_count_cars_labeled += count_cars_labeled
            total_count_bike_labeled += count_bike_labeled
            total_count_lkw_labeled += count_lkw_labeled
            print("images: " + str(frame_count_num))
            print("Removed: "+str(count_removed))
            print("Auto: " + str(count_cars_labeled) + " Motorrad: " + str(count_bike_labeled) + " LKW: " + str(count_lkw_labeled) )
            print("Time: " + str(end_w - start_w))

        # cleanup
        for cam in list_cameras:
            if cam is not None:
                try:
                    cam.destroy()
                finally:
                    pass
        # final log data
        print("Removed: " + str(total_count_removed))
        print("Auto: " + str(total_count_cars_labeled) + " Motorrad: " + str(total_count_bike_labeled) + " LKW: " + str(total_count_lkw_labeled))
        break


def save_labels(delete_cars,label_path, file_name, labels, targets, camera, fov_index, alternates,pro_mat_k):
    all_target_bb = []
    # prepare bounding boxes
    pos_str = ""

    log_list=[0,0,0]

    finalised_indexes=[]

    start_end_image_size = [0,central.cutoffs[0],central.cutoffs[1],central.picture_size[1]-1]  # x_min x_max y_min y_max

    for targets_index, target in enumerate(targets):
        label = labels[targets_index]
        alternate_car_transform = alternates[targets_index][0]
        alternate_bb_verts = alternates[targets_index][1]

        if True:
            bb_2d = calculate_bounding_box_2d(label, target, camera,
                                              pro_mat_k[fov_index],
                                              alternate_bb_verts, alternate_car_transform)
            if bb_2d == None:
                print("NONE bb")
                continue

            # x x y y label
            bb_2d = [bb_2d[0], bb_2d[1], bb_2d[2], bb_2d[3], label]

            # set bounding box to fit picture frame and compare how much is visible, too little and it is a continue
            if bb_2d[0] >= start_end_image_size[1]  or bb_2d[1] <= start_end_image_size[0] or \
                    bb_2d[2] >= start_end_image_size[3]  or bb_2d[3] <= start_end_image_size[2] :
                finalised_indexes.append(targets_index)
                continue


            bb_x_length = bb_2d[1] - bb_2d[0]
            bb_y_length = bb_2d[3] - bb_2d[2]
            total_area = bb_x_length * bb_y_length

            x_length = min(bb_2d[1], start_end_image_size[1] ) - max(bb_2d[0], start_end_image_size[0] )
            y_length = min(bb_2d[3], start_end_image_size[3] ) - max(bb_2d[2], start_end_image_size[2] )

            overlap_area = x_length * y_length
            overlap_percentage = overlap_area / total_area

            # erstes auto immer sichtbar

            # entferne nicht sichtbares, also was außerhalb des bildes liegt

            # 18% or more visible means do include
            #  mehr overlap für motorräder

            if targets_index == 0 or  (label!="1" and overlap_percentage > 0.24) or  (label=="1" and overlap_percentage > 0.40):
                # now cut bb to size
                bb_2d[0] = max(bb_2d[0], start_end_image_size[0] )
                bb_2d[1] = min(bb_2d[1], start_end_image_size[1] )

                bb_2d[2] = max(bb_2d[2], start_end_image_size[2] )
                bb_2d[3] = min(bb_2d[3], start_end_image_size[3] )

                all_target_bb.append([bb_2d,targets_index])
            else:
                finalised_indexes.append(targets_index)

    for car_act_tar_index, primary_bb_list in enumerate(all_target_bb):
        breaker = False
        local_primary_bb = []
        primary_bb=primary_bb_list[0]

        for i_counter in range(0, car_act_tar_index):
            second_bb = all_target_bb[i_counter][0]
            if primary_bb[0] >= second_bb[1] or primary_bb[1] <= second_bb[0] or \
                    primary_bb[2] >= second_bb[3] or primary_bb[3] <= second_bb[2]:
                continue

            bb_x_length = primary_bb[1] - primary_bb[0]
            bb_y_length = primary_bb[3] - primary_bb[2]
            total_area = bb_x_length * bb_y_length

            x_length = min(primary_bb[1], second_bb[1]) - max(primary_bb[0],
                                                              second_bb[0])
            y_length = min(primary_bb[3], second_bb[3]) - max(primary_bb[2],
                                                              second_bb[2])

            overlap_area = x_length * y_length
            overlap_percentage = overlap_area / total_area

            # motorräder sind kleiner
            if ( primary_bb[4] != "1" and overlap_percentage > 0.78 )  or ( primary_bb[4]=="1" and overlap_percentage > 0.64 ):
                breaker = True
                break
        # weil wir ja sagen, das auto ist zu stark verdekct. von daher ist es raus
        if breaker:
            finalised_indexes.append(primary_bb_list[1])
            continue

        if car_act_tar_index > 0:
            pos_str += "\n"

        # in case bounding box is bigger than screen
        if primary_bb[0] < start_end_image_size[0] :
            primary_bb[0] = start_end_image_size[0]
        if primary_bb[1] > start_end_image_size[1] :
            primary_bb[1] = start_end_image_size[1]
        if primary_bb[2] < start_end_image_size[2] :
            primary_bb[2] = start_end_image_size[2]
        if primary_bb[3] > start_end_image_size[3] :
            primary_bb[3] = start_end_image_size[3]

        new_image_w=640
        new_image_h=640

        pos_str += primary_bb[4]
        # logging labels
        if pos_str == "0":
            log_list[0]+=1
        elif pos_str == "1":
            log_list[1]+=1
        elif pos_str == "2":
            log_list[2]+=1

        core_x = ((primary_bb[1] + primary_bb[0]) / 2)

        core_y = (primary_bb[3] + primary_bb[2])
        # nur für y, weil x rehcs abgeshcniten wrid. und   y ist immer zu tief weil oebn abgeshcniten wird

        core_y /= 2
        core_y -= central.cutoffs[1]

        pos_str += " " + str(core_x / float(new_image_w))
        pos_str += " " + str(core_y / float(new_image_h))
        pos_str += " " + str((primary_bb[1] - primary_bb[0]) / float(new_image_w))
        pos_str += " " + str((primary_bb[3] - primary_bb[2]) / float(new_image_h))

    # if car_type_index != 0:
    # new_thread = Thread(target=task, args=(frame_path + file_name + file_ending_image, img, label_path+file_name + '.txt',label_str + pos_str ))
    # new_thread.start()

    if delete_cars:
        get_cars=[]
        for ele in finalised_indexes:
            get_cars.append(targets[ele])

        for ele in get_cars:
            targets.remove(ele)

        new_labels = []
        for ind_alt, ele in enumerate(labels):
            if ind_alt not in finalised_indexes:
                new_labels.append(ele)
        labels = new_labels

        new_alternates = []
        for ind_alt, ele in enumerate(alternates):
            if ind_alt not in finalised_indexes:
                new_alternates.append(ele)
        alternates = new_alternates

        return [get_cars,labels,alternates]

    with open(label_path + file_name + '.txt', 'w') as f:
        f.write(pos_str)

    return log_list


def prepare_opposite(yes_counter_traffic,list_cars_this,opposite_traffic_spawn,blueprint_library,height_offset,opposite_traffic_dir,saved_bb_type2,list_all_actors):
    truck_counter_max = 3  # to limit trucks. as they are big
    last_val = -1
    last_val_rep = 0

    temp_opposite_transform = carla.Transform(
        Location(opposite_traffic_spawn.location.x, opposite_traffic_spawn.location.y,
                 opposite_traffic_spawn.location.z),
        Rotation(opposite_traffic_spawn.rotation.pitch,
                 opposite_traffic_spawn.rotation.yaw,
                 opposite_traffic_spawn.rotation.roll))

    if yes_counter_traffic:
        for i3 in range(0, 10):
            int_val = randint(0, 4)
            if int_val == 4:
                int_val = randint(0, 4)

            if int_val == 3:
                truck_counter_max -= 1
            if truck_counter_max < 0:
                while int_val == 3:
                    int_val = randint(0, 4)

            if int_val == last_val:
                last_val_rep += 1
            else:
                last_val_rep = 0

            if last_val_rep == 2:
                while int_val == last_val:
                    int_val = randint(0, 4)
                last_val_rep = 0
            last_val = int_val

            next_car_list = list_cars_this[int_val]
            if int_val == 0:
                temp_opposite_transform.location.x += (opposite_traffic_dir.x * 4)
                temp_opposite_transform.location.y += (opposite_traffic_dir.y * 4)
                continue
            next_car_id_value = randint(0, len(next_car_list) - 1)
            next_car = next_car_list[next_car_id_value]

            car_bp = blueprint_library.filter(next_car)[0]
            temp_opposite_transform.location.z += height_offset
            local_car_actor = world.spawn_actor(car_bp, temp_opposite_transform)
            ext1 = local_car_actor.bounding_box.extent.x

            # to fix bad bounding box
            if int_val == 2:
                some_yaw_val = local_car_actor.get_transform().rotation.yaw / 90
                int_index = int(round(some_yaw_val))
                if int_index < 0:
                    if int_index == -1:
                        int_index = 3
                    elif int_index == -2:
                        int_index = 2
                    elif int_index == -3:
                        int_index = 1
                    else:
                        print("error never happens 3422112")
                primary_bb = saved_bb_type2[next_car_id_value][int_index]
                ext1 = primary_bb.extent.x

            temp_opposite_transform.location.z -= height_offset
            temp_opposite_transform.location.x += (opposite_traffic_dir.x * ext1)
            temp_opposite_transform.location.y += (opposite_traffic_dir.y * ext1)

            if int_val != 4:
                local_car_actor.set_light_state(
                    carla.VehicleLightState(
                        carla.VehicleLightState.NONE | carla.VehicleLightState.LowBeam))

            local_car_actor.set_simulate_physics(False)
            local_car_actor.set_transform(temp_opposite_transform)

            list_all_actors.append(local_car_actor)

            # offset car  spawn
            temp_opposite_transform.location.x += (opposite_traffic_dir.x * ext1)
            temp_opposite_transform.location.y += (opposite_traffic_dir.y * ext1)
            temp_opposite_transform.location.x += (4 * opposite_traffic_dir.x)
            temp_opposite_transform.location.y += (4 * opposite_traffic_dir.y)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', type=str, default="train", help='test train')
    parser.add_argument('--path', type=str, default="vehicle_data\\", help='pfad zu vehicle_data. also  c:\\my_p_data\\vehicle_data\\')

    opt = parser.parse_args()
    task = opt.task
    print(opt)
    ttc=3

    if task=="train":
        ttc=3
    elif task=="test":
        ttc=1
    client = None
    try:
        address = "localhost"
        address_network = "192.168.1.110"
        client = carla.Client(address, 2000)
        client.set_timeout(10.0)
        main(client,ttc,opt.path)
    finally:
        print("exit")
        world = client.load_world('Town03')

