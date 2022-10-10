# testen der vorhandenen auto modelle

import sys
import threading
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

the_name=""


list_names = ["walker.pedestrian.0012","walker.pedestrian.0016", "static.prop.bench01", "static.prop.clothcontainer",
     "static.prop.vendingmachine"]

def thread_function(world):
    global the_name
    time.sleep(4)
    vehicle=None

    try:
        blueprints = [bp for bp in world.get_blueprint_library().filter('vehicle.*')]
        blueprints = [world.get_blueprint_library().filter(name)[0] for name in list_names]
        for blueprint in blueprints:
            spawn_point = carla.Transform(carla.Location(x=34.6, y=-5.8, z=5.598))
            vehicle = world.spawn_actor(blueprint, spawn_point)
            print(blueprint.id)
            the_name=blueprint.id
            time.sleep(3)
            vehicle.destroy()
    finally:
        if vehicle is not None:
            vehicle.destroy()
        print('Done, Actors cleaned-up successfully!')

def main():
    global the_name
    list_pkw =  []
    list_bike=[]
    list_lkw=[]
    list_other=[]
    try:

        address_network = "192.168.1.110"
        client = carla.Client(address_network, 2000)
        client.set_timeout(20.0)
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
        car_actor = None

        blueprint_library = world.get_blueprint_library()

        blueprints = [bp for bp in world.get_blueprint_library().filter('vehicle.*')]
        for blueprint in blueprints:
            print("\"" + blueprint.id + "\",")
        for attr in blueprint:
            print(' - {}'.format(attr))

        pygame.init()

        display = pygame.display.set_mode(
            (460, 460),
            pygame.HWSURFACE | pygame.DOUBLEBUF)
        clock = pygame.time.Clock()


        x = threading.Thread(target=thread_function, args=(world,))
        x.daemon = True
        x.start()

        # x.join()

        change = False

        actor = b1
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
                print("Car")
                list_pkw.append(the_name)
                time.sleep(0.2)
            if keys[pygame.constants.K_2]:
                print("Bike")
                list_bike.append(the_name)
                time.sleep(0.2)
            if keys[pygame.constants.K_3]:
                print("LKW")
                list_lkw.append(the_name)
                time.sleep(0.2)
            if keys[pygame.constants.K_4]:
                print("Other")
                list_other.append(the_name)
                time.sleep(0.2)
            if keys[pygame.constants.K_5]:
                print(list_pkw)
                print("----")
                print(list_bike)
                print("----")
                print(list_lkw)
                print("----")
                print(list_other)
                print("----")

            if keys[pygame.constants.K_0]:
                break


            if keys[pygame.constants.K_KP1]:
                weather = world.get_weather()
                weather.sun_altitude_angle = -10
                world.set_weather(weather)
            if keys[pygame.constants.K_KP2]:
                weather = world.get_weather()
                weather.sun_altitude_angle = 40
                world.set_weather(weather)
            if keys[pygame.constants.K_KP3]:
                weather.fog_density = 0
            if keys[pygame.constants.K_KP4]:
                weather.fog_density = 60
            if keys[pygame.constants.K_KP5]:
                weather.fog_density = 100
            if keys[pygame.constants.K_KP6]:
                weather.precipitation = 100

            if keys[pygame.constants.K_KP7]:
                weather = world.get_weather()
                weather.dust_storm = 30
                world.set_weather(weather)
            if keys[pygame.constants.K_KP8]:
                weather = world.get_weather()
                weather.dust_storm = 60
                world.set_weather(weather)
            if keys[pygame.constants.K_KP9]:
                weather = world.get_weather()
                weather.dust_storm = 100
                world.set_weather(weather)
            if keys[pygame.constants.K_KP0]:
                weather = world.get_weather()
                weather.dust_storm = 0
                world.set_weather(weather)



            if change == True:
                print(transform)
                change = False
                actor.set_transform(transform)

    finally:
        b1.destroy()
      #  x.join()
        print('ENDE!')

if __name__ == '__main__':
    main()


actor_list = []



list_cars = [
    "vehicle.chevrolet.impala",
    "vehicle.mercedesccc.mercedesccc",
    "vehicle.audi.a2",
    "vehicle.nissan.micra",

    "vehicle.audi.tt",
    "vehicle.bmw.grandtourer",
    "vehicle.bmw.isetta",
    "vehicle.chargercop2020.chargercop2020",

    "vehicle.citroen.c3",
    "vehicle.dodge_charger.police",
    "vehicle.jeep.wrangler_rubicon",
    "vehicle.mercedes-benz.coupe",

    "vehicle.mini.cooperst",
    "vehicle.nissan.patrol",
    "vehicle.seat.leon",
    "vehicle.toyota.prius",

    "vehicle.tesla.model3",
    "vehicle.tesla.cybertruck",
    "vehicle.audi.etron",
    "vehicle.lincoln.mkz2017",

    "vehicle.mustang.mustang",
    "vehicle.lincoln2020.mkz2020",
    "vehicle.charger2020.charger2020",
]

list_bikes = [
    "vehicle.harley-davidson.low_rider",
    "vehicle.yamaha.yzf",
    "vehicle.kawasaki.ninja",
]

list_cyclists = [
    "vehicle.bh.crossbike",
    "vehicle.gazelle.omafiets",
    "vehicle.diamondback.century",
]
list_others = [
    "vehicle.carlamotors.carlacola",
    "vehicle.volkswagen.t2",
]

list_pkw_new = [
    'vehicle.audi.a2',
    'vehicle.audi.etron',
    'vehicle.audi.tt',
    'vehicle.bmw.grandtourer',
    'vehicle.chevrolet.impala',

    'vehicle.citroen.c3',
    'vehicle.dodge.charger_2020',
    'vehicle.dodge.charger_police',
    'vehicle.dodge.charger_police_2020',
    'vehicle.ford.crown',

    'vehicle.ford.mustang',
    'vehicle.jeep.wrangler_rubicon',
    'vehicle.lincoln.mkz_2017',
    'vehicle.lincoln.mkz_2020',
    'vehicle.mercedes.coupe',

    'vehicle.mercedes.coupe_2020',
    'vehicle.micro.microlino',
    'vehicle.mini.cooper_s',
    'vehicle.mini.cooper_s_2021',
    'vehicle.nissan.micra',

    'vehicle.nissan.patrol',
    'vehicle.nissan.patrol_2021',
    'vehicle.seat.leon',
    'vehicle.tesla.cybertruck',
    'vehicle.tesla.model3',

    'vehicle.toyota.prius',
]

list_bike_new = [
    'vehicle.kawasaki.ninja',
    'vehicle.harley-davidson.low_rider',
    'vehicle.yamaha.yzf',
    'vehicle.vespa.zx125',
]

list_lkw_new = [
    'vehicle.ford.ambulance',
    "vehicle.carlamotors.carlacola",
    "vehicle.mercedes.sprinter",
    'vehicle.carlamotors.firetruck',
]

list_other_new = [
    'vehicle.bh.crossbike',
    'vehicle.gazelle.omafiets',
    'vehicle.diamondback.century',
    'vehicle.volkswagen.t2',
    'vehicle.volkswagen.t2_2021',
]
