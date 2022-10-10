# testen der vorhandenen auto modelle

import sys
import pygame

try:
    sys.path.append("C:\\Users\\Stephan\\Desktop\\CARLA_0.9.11\\WindowsNoEditor\\PythonAPI\\carla\\dist\\carla-0.9.11-py3.7-win-amd64.egg")
except IndexError:
 pass

import carla

import random
import time
import queue
import numpy as np


def draw_image(surface, image, blend=False):
    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]
    array = array[:, :, ::-1]
    image_surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
    if blend:
        image_surface.set_alpha(100)
    surface.blit(image_surface, (0, 0))

_SLEEP_TIME_ = 2

def main():

    list_pkw = ['vehicle.chevrolet.impala', 'vehicle.mercedesccc.mercedesccc', 'vehicle.audi.a2', 'vehicle.nissan.micra',
            'vehicle.audi.tt', 'vehicle.bmw.grandtourer', 'vehicle.bmw.isetta', 'vehicle.chargercop2020.chargercop2020',
            'vehicle.citroen.c3', 'vehicle.dodge_charger.police', 'vehicle.mercedes-benz.coupe',
            'vehicle.mini.cooperst', 'vehicle.seat.leon', 'vehicle.toyota.prius', 'vehicle.tesla.model3',
            'vehicle.audi.etron', 'vehicle.lincoln.mkz2017', 'vehicle.mustang.mustang', 'vehicle.lincoln2020.mkz2020',
            'vehicle.charger2020.charger2020',
                'vehicle.jeep.wrangler_rubicon', 'vehicle.nissan.patrol',
                'vehicle.tesla.cybertruck'
                ]

    list_bike = ['vehicle.harley-davidson.low_rider', 'vehicle.yamaha.yzf', 'vehicle.kawasaki.ninja']

    list_lkw = ['vehicle.carlamotors.carlacola', ]

    list_other = ['vehicle.bh.crossbike', 'vehicle.gazelle.omafiets', 'vehicle.diamondback.century', 'vehicle.volkswagen.t2']

    counter_car = len(list_pkw)
    counter_car-=1
    counter_bike = len(list_bike)
    counter_bike -= 1
    counter_lkw = len(list_lkw)
    counter_lkw -= 1

    counter_other = len(list_other)
    counter_other -= 1



    try:

        client = carla.Client("localhost", 2000)
        client.set_timeout(10.0)
        world = client.get_world()
        print(client.get_available_maps())
        world = client.load_world('Town03')

        camera_list_images = queue.Queue()
        blueprint_library = world.get_blueprint_library()
        box = blueprint_library.filter("box01")[0]
        box_spawnPoint =  carla.Transform(carla.Location(x=34.599998, y=8.200003, z=9.597998), carla.Rotation(pitch=-25.499878, yaw=-91.499443, roll=0.000023))
        b1 = world.spawn_actor(box, box_spawnPoint)

        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', str(460))
        camera_bp.set_attribute('image_size_y', str(460))
        camera_bp.set_attribute('fov', '60')

        cam_transform = carla.Transform(carla.Location(x=1.0, z=0))
        camera = world.spawn_actor(camera_bp, cam_transform, attach_to=b1)

        camera.listen(camera_list_images.put)

        blueprints = [bp for bp in world.get_blueprint_library().filter('vehicle.*')]
        for blueprint in blueprints:
            print("\"" + blueprint.id + "\",")
        for attr in blueprint:
            print(' - {}'.format(attr))

        pygame.init()

        display = pygame.display.set_mode(
            (460, 460),
            pygame.HWSURFACE | pygame.DOUBLEBUF)

        actor = b1
        vehicle=None

        change=False

        while (True):
            data = camera_list_images.get()

            if data is not None:
                draw_image(display, data)
                pygame.display.flip()
                pygame.event.pump()

            keys = pygame.key.get_pressed()
            transform = actor.get_transform()
            if keys[pygame.constants.K_w]:
                transform.location.x += 1
                change = True
            if keys[pygame.constants.K_s]:
                transform.location.x -= 1
                change = True
            if keys[pygame.constants.K_d]:
                transform.location.y += 1
                change = True
            if keys[pygame.constants.K_a]:
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

            if keys[pygame.constants.K_1]:
                if vehicle is not None:
                    vehicle.destroy()
                if counter_car>=0:
                    blueprint= world.get_blueprint_library().filter(list_pkw[counter_car])[0]
                    counter_car -=1
                    spawn_point = carla.Transform(carla.Location(x=34.6, y=-5.8, z=5.598))
                    vehicle = world.spawn_actor(blueprint, spawn_point)
                    print(blueprint.id)
                    time.sleep(0.3)
                else:
                    counter_car = len(list_pkw) -1

            if keys[pygame.constants.K_2]:
                if vehicle is not None:
                    vehicle.destroy()
                if counter_bike >= 0:
                    blueprint =world.get_blueprint_library().filter(list_bike[counter_bike])[0]
                    counter_bike -= 1
                    spawn_point = carla.Transform(carla.Location(x=34.6, y=-5.8, z=5.598))
                    vehicle = world.spawn_actor(blueprint, spawn_point)
                    print(blueprint.id)
                    time.sleep(0.3)
                else:
                    counter_bike = len(list_bike) - 1

            if keys[pygame.constants.K_3]:
                if vehicle is not None:
                    vehicle.destroy()
                if counter_lkw >= 0:
                    blueprint = world.get_blueprint_library().filter(list_lkw[counter_lkw])[0]
                    counter_lkw -= 1
                    spawn_point = carla.Transform(carla.Location(x=34.6, y=-5.8, z=5.598))
                    vehicle = world.spawn_actor(blueprint, spawn_point)
                    print(blueprint.id)
                    time.sleep(0.3)
                else:
                    counter_lkw = len(list_lkw) - 1

            if keys[pygame.constants.K_4]:
                if vehicle is not None:
                    vehicle.destroy()
                if counter_other >= 0:
                    blueprint = world.get_blueprint_library().filter(list_other[counter_other])[0]
                    counter_other -= 1
                    spawn_point = carla.Transform(carla.Location(x=34.6, y=-5.8, z=5.598))
                    vehicle = world.spawn_actor(blueprint, spawn_point)
                    print(blueprint.id)
                    time.sleep(0.3)
                else:
                    counter_other = len(list_other) - 1

            if keys[pygame.constants.K_5]:
                print(list_pkw)
                print("----")
                print(list_bike)
                print("----")
                print(list_lkw)
                print("----")
                print_cars=True

            if keys[pygame.constants.K_0]:
                break

            if change == True:
                print(transform)
                change = False
                actor.set_transform(transform)


    finally:
        if vehicle is not None:
            vehicle.destroy()
        b1.destroy()
        print('ENDE!')

if __name__ == '__main__':
    main()








