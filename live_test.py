# live test. echtzeit laufende simulation

import queue
import numpy as np
import time
import random
from random import randint
import cv2
import threading
import pygame
import central_data as central
from central_data import carla
# import carla
from carla import Transform, Location, Rotation


from multiprocessing import Process,Pipe ,sharedctypes
import ctypes


import argparse
import os
import platform
import sys
from pathlib import Path

import torch
import torch.backends.cudnn as cudnn

from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import (LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, smart_inference_mode, time_sync

from utils.augmentations import (Albumentations, augment_hsv, classify_albumentations, classify_transforms, copy_paste,
                                 letterbox, mixup, random_perspective)


@smart_inference_mode()
def run(pipe,
    weights,
    data,
    conf_thres,
    iou_thres ,
    device,
        town):


    print(weights)
    print(data)
    print("--")
    print(conf_thres)
    print("--")
    print("dev "+device)


    """
    weights = "best.pt"
    data = 'data/vehicle_data.yaml'  # wichtig: wegen den klassen
    conf_thres = 0.5
    iou_thres = 0.45
    device = "cpu"

    """
    augment = False

    classes = None  # filter by class: --class 0, or --class 0 2 3
    imgsz = (picture_size_use, picture_size_use)
    max_det = 1000
    agnostic_nms = False
    half = False  # use FP16 half-precision inference
    dnn = False


    # Load model
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size



   # device = select_device("cpu")
   # model = attempt_load(weights, device=device)


    #  pruned_model = copy.deepcopy(model)
    #  save_name = model_filename_prefix +"quant"

    # Run inference
    batch_size = 1
    model.warmup(imgsz=(1 if pt else batch_size, 3, *imgsz))  # warmup
    windows, dt = [], [0.0, 0.0, 0.0]


    while True:
        sys.stdout.flush()
        # request next
        pipe.send(1)
        # copy over

        # wait for finish
        im0 = pipe.recv()  # warte auf array

     #   im0 = shared_array
    #    img0 = np.reshape(np.copy(shared_array.raw_data), (picture_size_use, picture_size_use, 4))

        im0 = cv2.cvtColor(im0, cv2.COLOR_BGR2RGB)
        im0 = cv2.cvtColor(im0, cv2.COLOR_RGB2BGR)
    #    im0 = cv2.imread(path)  # BGR

        im = letterbox(im0, picture_size_use, stride=32, auto=True)[0]  # padded resize
        im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        im = np.ascontiguousarray(im)  # contiguous

        t1 = time_sync()
        im = torch.from_numpy(im).to(device)
        im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        t2 = time_sync()
        dt[0] += t2 - t1

        # Inference
        pred = model(im, augment=augment, visualize=False)
        t3 = time_sync()
        dt[1] += t3 - t2

        # NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        dt[2] += time_sync() - t3

        # Second-stage classifier (optional)
        # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

        prediction_values = [0 for ele in names]
        # Process predictions

        hide_conf = True # test it out how it looks

        for i, det in enumerate(pred):  # per image
            s=""

            s += '%gx%g ' % im.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            annotator = Annotator(im0, line_width=2, example=str(names))

            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()
                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                    prediction_values[int(c)]+=int(n)  # my own: sum up predictions


                # BBox markieren
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)  # integer class
                    label = None if False else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                    annotator.box_label(xyxy, label, color=colors(c, True))

            # Stream results
            im0 = annotator.result()
            if True:
                if platform.system() == 'Linux':
                    windows.append(p)
                    cv2.namedWindow(str(p), cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
                    cv2.resizeWindow(str(p), im0.shape[1], im0.shape[0])
                cv2.imshow("Bild", im0)
                cv2.waitKey(1)  # 1 millisecond

            # Print time (inference-only)
            if prediction_values[0] !=0 or prediction_values[1] !=0 or prediction_values[2] !=0 :
                print("")
                print("")
                LOGGER.info(f'{s}Done. ({t3 - t2:.3f}s)')

                res = [[names[int(ind)], int(val)] for ind, val in enumerate(prediction_values) if val != 0]
                res_name = [names[int(ind)] + " Erkennungen: " + str(val) for ind, val in enumerate(prediction_values)  if val != 0]
                print(res_name)

    print("exit nn")


picture_size_use=640
up_translate = 40

def draw_image(surface, image, blend=False):

    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]
    array = array[:, :, ::-1]
    image_surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
    if blend:
        image_surface.set_alpha(100)
    surface.blit(image_surface, (0, 0))


def main(client,vehicles_list,carla_part, town):

    #  Town03  Town01  3  1
    type_town_command = town

    file_ending_image = ".jpeg"

    list_use_cam_car_location = central.list_live_test_camera_locations_t1

    world = None
    if type_town_command == 3:
        list_use_cam_car_location = central.list_live_test_camera_locations_t3
        random.seed(3781102)
        world = client.load_world('Town03')
        print("Town03")
    else:
        list_use_cam_car_location = central.list_live_test_camera_locations_t1
        random.seed(148280)
        world = client.load_world('Town01')
        print("Town01")

    settings = world.get_settings()
    frame = world.apply_settings(carla.WorldSettings(
        no_rendering_mode=False,
        synchronous_mode=True,
        fixed_delta_seconds=0.1))  # 1.0 / 60))

    blueprint_library = world.get_blueprint_library()



    active_location_index=0
    current_cam_location = list_use_cam_car_location[active_location_index][0]
    current_spawn_location = list_use_cam_car_location[active_location_index][1]
    cam_transform = carla.Transform(Location(x=current_cam_location.location.x, y=current_cam_location.location.y, z=current_cam_location.location.z),
              Rotation(pitch=current_cam_location.rotation.pitch, yaw=current_cam_location.rotation.yaw, roll=current_cam_location.rotation.roll))

    car_spawn_point = carla.Transform(Location(x=current_spawn_location.location.x, y=current_spawn_location.location.y, z=current_spawn_location.location.z),
              Rotation(pitch=current_spawn_location.rotation.pitch, yaw=current_spawn_location.rotation.yaw, roll=current_spawn_location.rotation.roll))


    positions_walkers = central.positions_walkers_t3
    list_cars_combined=[]

    if central.new_version == "1":
        list_cars_combined = [
            central.list_cars,
            central.list_bikes,
            central.list_lkw,
            central.list_bycicle,
        ]
    else:
        list_cars_combined = [
            central.list_pkw_new,
            central.list_bike_new,
            central.list_lkw_new,
            central.list_bicycle_new,
        ]


    # create object and camera
    box_bp = blueprint_library.filter("box01")[0]
    the_box = world.spawn_actor(box_bp, carla.Transform(
        carla.Location(x=246.709337, y=-13.22, z=10.09 ),
        carla.Rotation(pitch=0.0, yaw=0.0, roll=0.000000)))
    the_box.set_transform(cam_transform)



    # str(central.fov_list_train[0])



    camera_bp = blueprint_library.find('sensor.camera.rgb')
    camera_bp.set_attribute('image_size_x', str(picture_size_use))
    camera_bp.set_attribute('image_size_y', str(picture_size_use))
    camera_bp.set_attribute('fov', "40")
    cam_transform_bp = carla.Transform(carla.Location(x=1.0, z=0))

    camera_element = world.spawn_actor(camera_bp, cam_transform_bp, attach_to=the_box)
    camera_queue_images = queue.Queue()
    camera_element.listen(camera_queue_images.put)

    use_this_fov = ["5", "10", "15", "20", "30"]



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

    tm = client.get_trafficmanager(8003)
    tm_port = tm.get_port()
    tm.set_random_device_seed(288502)
    tm.global_percentage_speed_difference(30.0)
    tm.set_synchronous_mode(True)

    # für alte api version
    if central.new_version == "1":
        tm.set_global_distance_to_leading_vehicle(3)
    else:
        tm.global_distance_to_leading_vehicle(3)


    for car_actor_temp in vehicles_list:
        car_actor_temp.set_autopilot(True, tm_port)
        tm.ignore_walkers_percentage(car_actor_temp, 100)


    if type_town_command == 3:
        pass
    else:
        pass


    change = False

    data_queue = queue.Queue()

    pygame.init()

    display = pygame.display.set_mode(
        (picture_size_use, picture_size_use),
        pygame.HWSURFACE | pygame.DOUBLEBUF)
    clock = pygame.time.Clock()






    # TODO  pygame it is

    """
    
        def catchThread(ddqq):
        while True:
            key2 = cv2.waitKey(0)
            ddqq.put(key2)
    
    thread = threading.Thread(target=catchThread,
                     args=( data_queue,))
    thread.setDaemon(True)
    thread.start()
    
    data = camera_queue_images.get()
    img = np.reshape(np.copy(data.raw_data), (data.height, data.width, 4))

    cv2.imshow("image", img)
    
     if cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1:
            break
    
    
    """


    while (True):


        # todo  spawn cars
        # test if cars can be spawned
        # mabye radius aroudn camrea  and despawn if too far away ?
        # test virutal cam



        #  bewege und erzeuge sachen

        # erzeuge bilder
        # sende bilder zu virtual

        try:
            world.tick(2)
        except:
            print("WARNING: tick not received w")



        data = camera_queue_images.get()

        if carla_part.poll() and data is not None:
            carla_part.recv()
      #      np.copy(shared_array,data)
           # carla_part.send(1)
            img_copy = np.reshape(np.copy(data.raw_data), (data.height, data.width, 4))
            carla_part.send(img_copy)


    #    img = np.reshape(np.copy(data.raw_data), (data.height, data.width, 4))


        draw_image(display, data)

        pygame.display.flip()
        pygame.event.pump()

        keys = pygame.key.get_pressed()

        # frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # input  # steuerung für kamera und autos

        if keys[pygame.constants.K_1]:
            spawn_new_car(car_spawn_point, 0, blueprint_library, list_cars_combined, world)
        if keys[pygame.constants.K_2]:
            spawn_new_car(car_spawn_point, 1, blueprint_library, list_cars_combined, world)
        if keys[pygame.constants.K_3]:
            spawn_new_car(car_spawn_point, 2, blueprint_library, list_cars_combined, world)
        if keys[pygame.constants.K_4]:
            spawn_new_car(car_spawn_point, 3, blueprint_library, list_cars_combined, world)

        def spawn_new_car(car_spawn_point,type_id,blueprint_library,list_cars_combined,world):
            next_car_id_value = randint(0, len(list_cars_combined[type_id]) - 1)
            next_car_name = list_cars_combined[type_id][next_car_id_value]
            car_bp = blueprint_library.filter(next_car_name)[0]

            # todo teste, ob ein spawn möglich ist

            loca_n = car_spawn_point.location
            fine_apart = True

            def squaring(num):
                return num*num


            for ele in vehicles_list:
                loca_l = ele.get_transform().location
                dist2 = (squaring(loca_n.x - loca_l.x)  + squaring(loca_n.y - loca_l.y)  + squaring(loca_n.z - loca_l.z) )  #squared
               # print(str(dist2))
                if dist2 <22:
                    fine_apart=False
                    break

            if fine_apart:
                car_spawn_point.location.z += up_translate
                local_car_actor = world.spawn_actor(car_bp, car_spawn_point)
                local_car_actor.set_simulate_physics(False)
                if type_id!=3:
                    local_car_actor.set_light_state(carla.VehicleLightState(
                        carla.VehicleLightState.NONE | carla.VehicleLightState.LowBeam))
                vehicles_list.append(local_car_actor)
                car_spawn_point.location.z -= up_translate
                local_car_actor.set_transform(car_spawn_point)

                local_car_actor.set_autopilot(True, tm_port)
                tm.ignore_walkers_percentage(local_car_actor, 100)


        if keys[pygame.constants.K_w]:
            cam_transform.location.x += 1
            change=True
        if keys[pygame.constants.K_s]:
            cam_transform.location.x -= 1
            change = True
        if keys[pygame.constants.K_a]:
            cam_transform.location.y -= 1
            change = True
        if keys[pygame.constants.K_d]:
            cam_transform.location.y += 1
            change = True
        if keys[pygame.constants.K_q]:
            cam_transform.location.z += 1
            change = True
        if keys[pygame.constants.K_e]:
            cam_transform.location.z -= 1
            change = True
        if keys[pygame.constants.K_r]:
            cam_transform.rotation.yaw -= 0.5
            change = True
        if keys[pygame.constants.K_t]:
            cam_transform.rotation.yaw += 0.5
            change = True
        if keys[pygame.constants.K_z]:
            cam_transform.rotation.pitch += 0.5
            change = True
        if keys[pygame.constants.K_u]:
            cam_transform.rotation.pitch -= 0.5
            change = True
        if change:
            change=False
            the_box.set_transform(cam_transform)

        if keys[pygame.constants.K_f]:
            print(cam_transform)

        if keys[pygame.constants.K_COMMA]:
            for ele in vehicles_list:
                if ele is not None:
                    ele.destroy()
            vehicles_list=[]
        if keys[pygame.constants.K_PERIOD]:
            ele_veh = vehicles_list[len(vehicles_list)-1]
            ele_veh.destroy()
            vehicles_list.remove(ele_veh)

        if keys[pygame.constants.K_y]:
            camera_queue_images = queue.Queue()
            camera_element.destroy()
            camera_bp.set_attribute('fov', use_this_fov[0])
            camera_element = world.spawn_actor(camera_bp, cam_transform_bp, attach_to=the_box)
            camera_element.listen(camera_queue_images.put)

        if keys[pygame.constants.K_x]:
            camera_queue_images = queue.Queue()
            camera_element.destroy()
            camera_bp.set_attribute('fov', use_this_fov[1])
            camera_element = world.spawn_actor(camera_bp, cam_transform_bp, attach_to=the_box)
            camera_element.listen(camera_queue_images.put)

        if keys[pygame.constants.K_c]:
            camera_queue_images = queue.Queue()
            camera_element.destroy()
            camera_bp.set_attribute('fov', use_this_fov[2])
            camera_element = world.spawn_actor(camera_bp, cam_transform_bp, attach_to=the_box)
            camera_element.listen(camera_queue_images.put)

        if keys[pygame.constants.K_v]:
            camera_queue_images = queue.Queue()
            camera_element.destroy()
            camera_bp.set_attribute('fov', use_this_fov[3])
            camera_element = world.spawn_actor(camera_bp, cam_transform_bp, attach_to=the_box)
            camera_element.listen(camera_queue_images.put)

        if keys[pygame.constants.K_b]:
            camera_queue_images = queue.Queue()
            camera_element.destroy()
            camera_bp.set_attribute('fov', use_this_fov[4])
            camera_element = world.spawn_actor(camera_bp, cam_transform_bp, attach_to=the_box)
            camera_element.listen(camera_queue_images.put)




        if keys[pygame.constants.K_8]:
            if  active_location_index > 0:
                active_location_index -= 1
            current_cam_car_location = list_use_cam_car_location[active_location_index]
            current_cam_location = current_cam_car_location[0]
            current_spawn_location = current_cam_car_location[1]

            cam_transform = carla.Transform(
                Location(x=current_cam_location.location.x, y=current_cam_location.location.y,
                         z=current_cam_location.location.z),
                Rotation(pitch=current_cam_location.rotation.pitch, yaw=current_cam_location.rotation.yaw,
                         roll=current_cam_location.rotation.roll))

            car_spawn_point = carla.Transform(
                Location(x=current_spawn_location.location.x, y=current_spawn_location.location.y,
                         z=current_spawn_location.location.z),
                Rotation(pitch=current_spawn_location.rotation.pitch, yaw=current_spawn_location.rotation.yaw,
                         roll=current_spawn_location.rotation.roll))

            the_box.set_transform(cam_transform)

            time.sleep(0.3)

        elif keys[pygame.constants.K_9]:
            if active_location_index < len(list_use_cam_car_location)-1:
                active_location_index+=1
            current_cam_car_location = list_use_cam_car_location[active_location_index]
            current_cam_location = current_cam_car_location[0]
            current_spawn_location = current_cam_car_location[1]
            cam_transform = carla.Transform(
                Location(x=current_cam_location.location.x, y=current_cam_location.location.y,
                         z=current_cam_location.location.z),
                Rotation(pitch=current_cam_location.rotation.pitch, yaw=current_cam_location.rotation.yaw,
                         roll=current_cam_location.rotation.roll))

            car_spawn_point = carla.Transform(
                Location(x=current_spawn_location.location.x, y=current_spawn_location.location.y,
                         z=current_spawn_location.location.z),
                Rotation(pitch=current_spawn_location.rotation.pitch, yaw=current_spawn_location.rotation.yaw,
                         roll=current_spawn_location.rotation.roll))

            the_box.set_transform(cam_transform)

            time.sleep(0.3)


    exit(0)


def parse_opt():

    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', default= "best.pt", type=str, help='model path(s)')
    parser.add_argument('--data', type=str,  default= "data/vehicle_data.yaml",help='(optional) dataset.yaml path')
    parser.add_argument('--conf-thres', type=float, default=0.5, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float,  default= 0.45,help='NMS IoU threshold')
    parser.add_argument('--device', default='cpu', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--town', default='3',type=int, help='1 oder 3 für town01 oder town03')

    opt = parser.parse_args()
    print(opt)
    return opt

def mrun(pipe,opt):
    run(pipe,**vars(opt) )

if __name__ == '__main__':
    opt = parse_opt()
    print(opt.town)

    carla_part, nn_part = Pipe()

    p = Process(target=mrun, args= ( nn_part,opt))
    p.start()

    vehicles_list = []
    client = None
    try:
        address = "localhost"
        address_network = "192.168.1.110"
        client = carla.Client(address, 2000)
        client.set_timeout(10.0)
        main(client,vehicles_list,carla_part,opt.town)
    finally:
        print("exit sim")
        for ele in vehicles_list:
            ele.destroy()
        vehicles_list = []
        world = client.load_world('Town03')
        sys.exit(0)

