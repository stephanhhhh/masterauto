# Daten Datei

import sys


# egg Datei muss korrekte Verison haben und im gleichen Order sein , wie dieses skript
new_version="3" # 1  3
try:
    sys.path.append("carla-0.9.1" + new_version + "-py3.7-win-amd64.egg")
  #  sys.path.append( "C:\\Users\\Stephan\\Desktop\\CARLA_0.9.11\\WindowsNoEditor\\PythonAPI\\carla\\dist\\carla-0.9.1"+new_version+"-py3.7-win-amd64.egg")
except IndexError:
    pass

import carla
from carla import Transform, Location, Rotation

import numpy as np

label_car = 0
label_bike = 1
label_lkw = 2

main_path = "c:\\my_p_data\\vehicle_data\\"
rel_path = "..\\vehicle_data9\\"

fov_list_train =  [40,50,65]
fov_list_test =  [42,51,66]


cutoffs=[639,80] # x ende  y start
picture_size =  [int(1280),int(720)]   # vlt.  1920x1080
#picture_size =  [int(640),int(640)]       # [int(1280),int(720)]  # 640

# training autos
list_empty_train=["static.prop.advertisement","walker.pedestrian.0012","walker.pedestrian.0016", "static.prop.bench01", "static.prop.clothcontainer",
     "static.prop.vendingmachine"]

list_pkw_train=[
    'vehicle.audi.a2',
    'vehicle.audi.etron',
    'vehicle.audi.tt',
    'vehicle.bmw.grandtourer',
    'vehicle.chevrolet.impala',

    'vehicle.citroen.c3',
    'vehicle.dodge.charger_2020',

    'vehicle.tesla.cybertruck',
    'vehicle.dodge.charger_police',
    'vehicle.dodge.charger_police_2020',

    'vehicle.ford.crown',
    'vehicle.jeep.wrangler_rubicon',

    'vehicle.toyota.prius',
]
list_bike_train=[
    'vehicle.kawasaki.ninja',

    'vehicle.yamaha.yzf',
    'vehicle.vespa.zx125',
]
list_lkw_train=[
    "vehicle.carlamotors.carlacola",
    "vehicle.mercedes.sprinter",
    'vehicle.carlamotors.firetruck',
]

list_bicycle_train=[
    'vehicle.diamondback.century',

    'vehicle.gazelle.omafiets',
]

# test autos
list_empty_test=["static.prop.glasscontainer","walker.pedestrian.0015","walker.pedestrian.0019", "static.prop.bench02", "static.prop.clothcontainer",
     "static.prop.box02"]

list_pkw_test=[
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
    'vehicle.ford.mustang',
    'vehicle.tesla.model3',

]
list_bike_test=[
    'vehicle.harley-davidson.low_rider',
]

list_lkw_test=[
'vehicle.ford.ambulance',
]

list_bicycle_test=[
    'vehicle.bh.crossbike',
]

list_cars_this_train = [
    list_empty_train,
    list_pkw_train,
    list_bike_train,
    list_lkw_train,
    list_bicycle_train,
]

list_cars_this_test = [
    list_empty_test,
    list_pkw_test,
    list_bike_test,
    list_lkw_test,
    list_bicycle_test,
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

    'vehicle.volkswagen.t2',
    'vehicle.volkswagen.t2_2021',
]
list_bicycle_new=[
    'vehicle.bh.crossbike',
    'vehicle.gazelle.omafiets',
    'vehicle.diamondback.century',
]


all_cars_lists_true = [
["static.prop.glasscontainer","walker.pedestrian.0012","walker.pedestrian.0016", "static.prop.bench01", "static.prop.clothcontainer",
     "static.prop.vendingmachine", "static.prop.box02"],
list_pkw_new,
list_bike_new,
list_lkw_new,
list_bicycle_new,
]


weather_reset = carla.WeatherParameters( sun_altitude_angle=0, sun_azimuth_angle =0, fog_density =0 , precipitation =0, precipitation_deposits =0,  wetness =0   )
#weather_reset = carla.WeatherParameters( sun_altitude_angle=0, sun_azimuth_angle =0, fog_density =0 , precipitation =0, dust_storm=0, precipitation_deposits =0,  wetness =0   )


weather_settings = [
    # sset 1: not so good. too blurry rain. htis camrea lense. thereofre bad. better remove it. otehrwise usable
#carla.WeatherParameters( sun_altitude_angle=-10, sun_azimuth_angle =20, fog_density =0 , precipitation =0, precipitation_deposits =0,  wetness =0   ),
#carla.WeatherParameters( sun_altitude_angle=3, sun_azimuth_angle =20, fog_density =50   ,precipitation =100 , precipitation_deposits =60 ,wetness =100 ),
#carla.WeatherParameters( sun_altitude_angle=64, sun_azimuth_angle =210 ),
#carla.WeatherParameters( sun_altitude_angle=28, sun_azimuth_angle =20,fog_density =40,precipitation_deposits =60,  wetness =100 ),
#carla.WeatherParameters( sun_altitude_angle=4, sun_azimuth_angle =20, fog_density =0   ),
#carla.WeatherParameters( sun_altitude_angle=11, sun_azimuth_angle =20, precipitation =100 , precipitation_deposits =60,  wetness =100),

# carla.WeatherParameters( sun_altitude_angle=-10, sun_azimuth_angle =20, fog_density =0 ,  precipitation_deposits =0,  wetness =0   ),

carla.WeatherParameters( sun_altitude_angle=8, sun_azimuth_angle =25,  precipitation_deposits =24 ,wetness =23 ),
carla.WeatherParameters( sun_altitude_angle=3, sun_azimuth_angle =22, fog_density =36 , precipitation_deposits =22 ,wetness =72 ),
carla.WeatherParameters( sun_altitude_angle=54, sun_azimuth_angle =210 ),
carla.WeatherParameters( sun_altitude_angle=25, sun_azimuth_angle =113, precipitation_deposits =61,  wetness =100 ),
carla.WeatherParameters( sun_altitude_angle=31, sun_azimuth_angle =123,fog_density =21,precipitation_deposits =62,  wetness =91 ),
carla.WeatherParameters( sun_altitude_angle=72, sun_azimuth_angle =45,  ),
carla.WeatherParameters( sun_altitude_angle=-4, sun_azimuth_angle =12,fog_density =11,precipitation_deposits =9,  wetness =12 ),
carla.WeatherParameters( sun_altitude_angle=11, sun_azimuth_angle =61, precipitation_deposits =53,  wetness =81),
#carla.WeatherParameters( sun_altitude_angle=45, sun_azimuth_angle =183,  ),
#carla.WeatherParameters( sun_altitude_angle=19, sun_azimuth_angle =147 , precipitation_deposits =87,  wetness =49),

#carla.WeatherParameters( sun_altitude_angle=2, sun_azimuth_angle =20, fog_density =0   ),
#carla.WeatherParameters( sun_altitude_angle=6, sun_azimuth_angle =80, fog_density =0   ),
#carla.WeatherParameters( sun_altitude_angle=10, sun_azimuth_angle =140, fog_density =0   ),
#carla.WeatherParameters( sun_altitude_angle=25, sun_azimuth_angle =190, fog_density =0   ),
#carla.WeatherParameters( sun_altitude_angle=45, sun_azimuth_angle =220, fog_density =0   ),
#carla.WeatherParameters( sun_altitude_angle=62, sun_azimuth_angle =100, fog_density =0   ),



#carla.WeatherParameters( sun_altitude_angle=6, sun_azimuth_angle =80, fog_density =20 ),
#carla.WeatherParameters( sun_altitude_angle=6, sun_azimuth_angle =80, fog_density =80 ),
#carla.WeatherParameters( sun_altitude_angle=6, sun_azimuth_angle =80, precipitation_deposits =20,  wetness =40 ),
#carla.WeatherParameters( sun_altitude_angle=6, sun_azimuth_angle =80, precipitation_deposits =60,  wetness =40 ),
#carla.WeatherParameters( sun_altitude_angle=6, sun_azimuth_angle =80, precipitation_deposits =60,  wetness =100 ),
#carla.WeatherParameters( sun_altitude_angle=6, sun_azimuth_angle =80, fog_density =40,precipitation_deposits =60,  wetness =100 ),



#carla.WeatherParameters( sun_altitude_angle=3, sun_azimuth_angle =20, fog_density =40   ),

#carla.WeatherParameters( sun_altitude_angle=5, sun_azimuth_angle =20, fog_density =40   ),

#carla.WeatherParameters( sun_altitude_angle=6, sun_azimuth_angle =18, fog_density =0   ),
#carla.WeatherParameters( sun_altitude_angle=7, sun_azimuth_angle =19, fog_density =40),
#carla.WeatherParameters( sun_altitude_angle=8, sun_azimuth_angle =20, fog_density =60),
#carla.WeatherParameters( sun_altitude_angle=9, sun_azimuth_angle =18, fog_density =60 , precipitation =100 , precipitation_deposits =60,  wetness =100),
#carla.WeatherParameters( sun_altitude_angle=10, sun_azimuth_angle =19, fog_density =100),


#carla.WeatherParameters( sun_altitude_angle=26, sun_azimuth_angle =18 ),
#carla.WeatherParameters( sun_altitude_angle=30, sun_azimuth_angle =98 ),
#carla.WeatherParameters( sun_altitude_angle=32, sun_azimuth_angle =100 ,fog_density =60 ,precipitation =100 , precipitation_deposits =60,  wetness =100),
#carla.WeatherParameters( sun_altitude_angle=34, sun_azimuth_angle =210 ),

#carla.WeatherParameters( sun_altitude_angle=56, sun_azimuth_angle =18 ),
#carla.WeatherParameters( sun_altitude_angle=58, sun_azimuth_angle =20, fog_density =40,precipitation_deposits =60,  wetness =100),
#carla.WeatherParameters( sun_altitude_angle=60, sun_azimuth_angle =98),
#carla.WeatherParameters( sun_altitude_angle=62, sun_azimuth_angle =100 ,fog_density =60, precipitation =100 , precipitation_deposits =60,  wetness =100),

]

#fog is not greatly visible at night only max fog is a bit visible

weather_fog = [0, 40, 60, 100]
weather_rain = [0, 100]  # schwacher effekt
weather_deposits = [0, 40, 60]  # aber nur background
weather_sun_angle = [20, 100, 210]  # bad with fog  60 100 kein effekt hier
# weather_dust_storm=[0,60]
weather_sun_altitude = [-10, 0, 30, 60]  # -10 0 kein sun angle
weather_wettness = [0, 100]  # schwacher effekt




car_rotations = [0,24]

# new locations

# Camera Position Town 1:
cam_pos_t1_c = [
    [
        Transform(Location(x=158.000000, y=-4.000000, z=8.000000),
                  Rotation(pitch=-13.998902, yaw=11.022917, roll=0.000001)),
        Transform(Location(x=158.000000, y=-4.000000, z=6.000000),
                  Rotation(pitch=-11.999659, yaw=11.511637, roll=0.000000)),
        Transform(Location(x=158.000000, y=-8.000000, z=4.000000),
                  Rotation(pitch=-9.499754, yaw=22.502079, roll=0.000010)),
        Transform(Location(x=158.000000, y=-8.000000, z=8.000000),
                  Rotation(pitch=-15.499324, yaw=23.511272, roll=-0.000000)),
    ],

    [
        Transform(Location(x=-4.000000, y=188.000000, z=8.000000),
                  Rotation(pitch=-19.499205, yaw=-76.980698, roll=0.000025)),
        Transform(Location(x=-4.000000, y=188.000000, z=6.000000),
                  Rotation(pitch=-17.499176, yaw=-73.975433, roll=0.000032)),
        Transform(Location(x=-8.000000, y=188.000000, z=4.000000),
                  Rotation(pitch=-9.998809, yaw=-68.481750, roll=0.000053)),
        Transform(Location(x=-8.000000, y=188.000000, z=8.000000),
                  Rotation(pitch=-14.498592, yaw=-68.983093, roll=0.000030)),
    ],

    [
        Transform(Location(x=151.000000, y=324.000000, z=5.000000),
                  Rotation(pitch=-11.499084, yaw=13.504361, roll=0.000082)),
        Transform(Location(x=151.000000, y=324.000000, z=6.000000),
                  Rotation(pitch=-16.498840, yaw=14.518740, roll=0.000083)),
    ],

    [
        Transform(Location(x=197.000000, y=54.000000, z=6.000000),
                  Rotation(pitch=-19.498775, yaw=12.522795, roll=0.000073)),
        Transform(Location(x=197.000000, y=54.000000, z=8.000000),
                  Rotation(pitch=-11.998838, yaw=7.520432, roll=0.000079)),
        Transform(Location(x=197.000000, y=50.000000, z=6.000000),
                  Rotation(pitch=-13.998650, yaw=19.518175, roll=0.000085)),
        Transform(Location(x=197.000000, y=50.000000, z=8.000000),
                  Rotation(pitch=-18.498596, yaw=17.021996, roll=0.000086)),
    ],

    [
        Transform(Location(x=162.000000, y=192.000000, z=7.000000),
                  Rotation(pitch=-19.998226, yaw=18.538794, roll=0.000079)),
        Transform(Location(x=161.000000, y=192.000000, z=8.000000),
                  Rotation(pitch=-14.998473, yaw=15.034284, roll=0.000051)),
        Transform(Location(x=162.000000, y=192.000000, z=12.000000),
                  Rotation(pitch=-21.492310, yaw=16.060303, roll=0.000090)),
    ],

    [
        Transform(Location(x=98.000000, y=234.000000, z=8.000000),
                  Rotation(pitch=-19.491207, yaw=111.050804, roll=0.000107)),
    ],

]


# Camera Position Town 3:
cam_pos_t3_c = [
    [
    Transform(Location(x=26.000000, y=-13.000000, z=8.000000), Rotation(pitch=-20.497492, yaw=26.497398, roll=0.000000)),
    Transform(Location(x=25.000000, y=-12.000000, z=4.000000), Rotation(pitch=-10.497679, yaw= 33.986736, roll=0.000000)),
    Transform(Location(x=28.000000, y=-13.000000, z=6.000000), Rotation(pitch=-16.997431, yaw= 37.977139, roll=0.000011)),
    ],
#    alte dateb
#    [
#    Transform(Location(x=252.000000, y=-15.000000, z=8.000000), Rotation(pitch=-19.993711, yaw=115.479904, roll=0.000027)),
#    Transform(Location(x=251.000000, y=-15.000000, z=4.000000), Rotation(pitch=-9.993769, yaw=112.985764, roll=0.000065)),
#    Transform(Location(x=257.000000, y=-15.000000, z=8.000000), Rotation(pitch=-19.993587, yaw=128.483810, roll=0.000054)),
#    ],

    [
Transform(Location(x=252.000000, y=16.000000, z=8.000000), Rotation(pitch=-17.993586, yaw=113.977409, roll=0.000029)),
Transform(Location(x=252.000000, y=19.000000, z=5.000000), Rotation(pitch=-12.993676, yaw=118.984581, roll=0.000051)),
Transform(Location(x=254.000000, y=18.000000, z=8.000000), Rotation(pitch=-19.993582, yaw=122.983612, roll=0.000043)),
    ],

    [
    Transform(Location(x=253.000000, y=-62.000000, z=11.000000), Rotation(pitch=-27.492704, yaw=118.999405, roll=0.000025)),
    Transform(Location(x=253.000000, y=-62.000000, z=8.000000), Rotation(pitch=-22.493553, yaw=123.490852, roll=0.000037)),
    ],
    [
    Transform(Location(x=51.000000, y=214.000000, z=8.000000), Rotation(pitch=-21.492186, yaw=-150.988556, roll=0.000075)),
    Transform(Location(x=46.000000, y=214.000000, z=6.000000), Rotation(pitch=-14.491632, yaw=-152.994888, roll=0.000101)),
    ],
    [
    Transform(Location(x=-68.000000, y=-216.000000, z=8.000000), Rotation(pitch=-18.491631, yaw=21.013292, roll=0.000153)),
    Transform(Location(x=-68.000000, y=-216.000000, z=4.000000), Rotation(pitch=-10.991727, yaw=23.014109, roll=0.000157)),
    Transform(Location(x=-74.000000, y=-218.000000, z=6.000000), Rotation(pitch=-11.991667, yaw=20.014849, roll=0.000160)),
    ],
    [
    Transform(Location(x=-94.000000, y=-58.000000, z=8.000000), Rotation(pitch=-19.497492, yaw=-67.001534, roll=0.000028)),
    Transform(Location(x=-95.000000, y=-59.000000, z=4.000000), Rotation(pitch=-12.997890, yaw=-58.483383, roll=0.000057)),
    Transform(Location(x=-94.000000, y=-51.000000, z=6.000000), Rotation(pitch=-15.997067, yaw=-68.004120, roll=0.000029)),
    ],
    [
    Transform(Location(x=-26.000000, y=144.000000, z=8.000000), Rotation(pitch=-20.486933, yaw=-154.484680, roll=0.000073)),
    Transform(Location(x=-11.000000, y=142.000000, z=8.000000), Rotation(pitch=-16.983339, yaw=-165.976242, roll=0.000100)),
    Transform(Location(x=-32.000000, y=141.000000, z=6.000000), Rotation(pitch=-15.983400, yaw=-149.979996, roll=0.000118)),
    ],
]

car_pos_targets_t1 = [
    [
        [Transform(Location(x=175.604065, y=-1.999993, z=0.001584),
                   Rotation(pitch=0.000178, yaw=179.997025, roll=-0.000366)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=175.604065, y=-1.999993, z=0.001584),
                   Rotation(pitch=0.000178, yaw=179.997025, roll=-0.000366)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=175.604065, y=-1.999993, z=0.001584),
                   Rotation(pitch=0.000178, yaw=179.997025, roll=-0.000366)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=173.604065, y=-1.999992, z=0.001584),
                   Rotation(pitch=0.000178, yaw=179.497055, roll=-0.000366)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=173.604065, y=-1.999992, z=0.001584),
                   Rotation(pitch=0.000178, yaw=179.497055, roll=-0.000366)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=173.604065, y=-1.999992, z=0.001584),
                   Rotation(pitch=0.000178, yaw=179.497055, roll=-0.000366)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=175.604065, y=-1.999992, z=0.001584),
                   Rotation(pitch=0.000178, yaw=179.497055, roll=-0.000366)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=175.604065, y=-1.999992, z=0.001584),
                   Rotation(pitch=0.000178, yaw=179.497055, roll=-0.000366)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=175.604065, y=-1.999992, z=0.001584),
                   Rotation(pitch=0.000178, yaw=179.497055, roll=-0.000366)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=174.604950, y=-1.999990, z=0.001730),
                   Rotation(pitch=0.000027, yaw=179.997025, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=174.604950, y=-1.999990, z=0.001730),
                   Rotation(pitch=0.000027, yaw=179.997025, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=174.604950, y=-1.999990, z=0.001730),
                   Rotation(pitch=0.000027, yaw=179.997025, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=-1.999989, y=173.603226, z=0.001687),
                   Rotation(pitch=0.000027, yaw=89.999374, roll=-0.000031)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
        [Transform(Location(x=-1.999989, y=173.603226, z=0.001687),
                   Rotation(pitch=0.000027, yaw=89.999374, roll=-0.000031)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
        [Transform(Location(x=-1.999989, y=173.603226, z=0.001687),
                   Rotation(pitch=0.000027, yaw=89.999374, roll=-0.000031)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=-1.999989, y=176.603226, z=0.001733),
                   Rotation(pitch=0.000027, yaw=89.999374, roll=-0.000031)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
        [Transform(Location(x=-1.999989, y=176.603226, z=0.001733),
                   Rotation(pitch=0.000027, yaw=89.999374, roll=-0.000031)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
        [Transform(Location(x=-1.999989, y=176.603226, z=0.001733),
                   Rotation(pitch=0.000027, yaw=89.999374, roll=-0.000031)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
    ],



    [
        [Transform(Location(x=-1.999989, y=169.603226, z=0.001733),
                   Rotation(pitch=0.000027, yaw=89.999229, roll=-0.000031)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
        [Transform(Location(x=-1.999989, y=169.603226, z=0.001733),
                   Rotation(pitch=0.000027, yaw=89.999229, roll=-0.000031)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
        [Transform(Location(x=-1.999989, y=169.603226, z=0.001733),
                   Rotation(pitch=0.000027, yaw=89.999229, roll=-0.000031)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=-1.999989, y=168.603226, z=0.001733),
                   Rotation(pitch=0.000027, yaw=89.999229, roll=-0.000031)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
        [Transform(Location(x=-1.999989, y=168.603226, z=0.001733),
                   Rotation(pitch=0.000027, yaw=89.999229, roll=-0.000031)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
        [Transform(Location(x=-1.999989, y=168.603226, z=0.001733),
                   Rotation(pitch=0.000027, yaw=89.999229, roll=-0.000031)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=165.604111, y=326.000000, z=0.001674),
                   Rotation(pitch=0.000000, yaw=179.997589, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=165.604111, y=326.000000, z=0.001674),
                   Rotation(pitch=0.000000, yaw=179.997589, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=165.604111, y=326.000000, z=0.001674),
                   Rotation(pitch=0.000000, yaw=179.997589, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=163.604111, y=326.000000, z=0.001674),
                   Rotation(pitch=0.000000, yaw=179.997589, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=163.604111, y=326.000000, z=0.001674),
                   Rotation(pitch=0.000000, yaw=179.997589, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=163.604111, y=326.000000, z=0.001674),
                   Rotation(pitch=0.000000, yaw=179.997589, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=207.604980, y=55.000000, z=0.001096),
                   Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=207.604980, y=55.000000, z=0.001096),
                   Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=207.604980, y=55.000000, z=0.001096),
                   Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=216.604111, y=55.000000, z=0.001096),
                   Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=215.604111, y=55.000000, z=0.001096),
                   Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=214.604111, y=55.000000, z=0.001096),
                   Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=214.604111, y=55.000000, z=0.001096),
                   Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=214.604111, y=55.000000, z=0.001096),
                   Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=214.604111, y=55.000000, z=0.001096),
                   Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=218.604980, y=55.000000, z=0.001096),
                   Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=218.604980, y=55.000000, z=0.001096),
                   Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=218.604980, y=55.000000, z=0.001096),
                   Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=175.604950, y=195.000198, z=0.001690),
                   Rotation(pitch=0.000034, yaw=179.997543, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=175.604950, y=195.000198, z=0.001690),
                   Rotation(pitch=0.000034, yaw=179.997543, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=175.604950, y=195.000198, z=0.001690),
                   Rotation(pitch=0.000034, yaw=179.997543, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=178.604950, y=195.000198, z=0.001690),
                   Rotation(pitch=0.000034, yaw=179.997543, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=178.604950, y=195.000198, z=0.001690),
                   Rotation(pitch=0.000034, yaw=179.997543, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=178.604950, y=195.000198, z=0.001690),
                   Rotation(pitch=0.000034, yaw=179.997543, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=182.604950, y=195.000198, z=0.001690),
                   Rotation(pitch=0.000034, yaw=179.997543, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=182.604950, y=195.000198, z=0.001690),
                   Rotation(pitch=0.000034, yaw=179.997543, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=182.604950, y=195.000198, z=0.001690),
                   Rotation(pitch=0.000034, yaw=179.997543, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=92.781563, y=250.352228, z=0.001686),
                   Rotation(pitch=0.000075, yaw=-89.903191, roll=0.000021)),
         Location(x=0.000000, y=1.000000, z=0.000000)],
        [Transform(Location(x=92.781563, y=250.352228, z=0.001686),
                   Rotation(pitch=0.000075, yaw=-89.903191, roll=0.000021)),
         Location(x=0.000000, y=1.000000, z=0.000000)],
        [Transform(Location(x=92.781563, y=250.352228, z=0.001686),
                   Rotation(pitch=0.000075, yaw=-89.903191, roll=0.000021)),
         Location(x=0.000000, y=1.000000, z=0.000000)],
    ],
]


car_pos_targets_t3 = [
    [
        [Transform(Location(x=39.266800, y=-7.999272, z=0.031731),
                   Rotation(pitch=0.000020, yaw=179.999893, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=39.266800, y=-7.999272, z=0.031731),
                   Rotation(pitch=0.000020, yaw=179.999893, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=39.266800, y=-7.999272, z=0.031731),
                   Rotation(pitch=0.000020, yaw=179.999893, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=39.26680, y=-3.999272, z=0.001689),
                   Rotation(pitch=0.000020, yaw=179.999893, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=39.26680, y=-3.999272, z=0.001689),
                   Rotation(pitch=0.000020, yaw=179.999893, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=39.26680, y=-3.999272, z=0.001689),
                   Rotation(pitch=0.000020, yaw=179.999893, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=41.26680, y=-3.999272, z=0.001729),
                   Rotation(pitch=0.000020, yaw=179.999893, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=41.26680, y=-3.999272, z=0.001729),
                   Rotation(pitch=0.000020, yaw=179.999893, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=41.26680, y=-3.999272, z=0.001729),
                   Rotation(pitch=0.000020, yaw=179.999893, roll=0.000000)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
    ],

# alte daten
#    [
#        [Transform(Location(x=246.998764, y=-0.79, z=0.001727),
#                   Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)),
#         Location(x=0.000000, y=1.000000, z=0.000000)],
#        [Transform(Location(x=246.998764, y=-0.79, z=0.001727),
#                   Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)),
#         Location(x=0.000000, y=1.000000, z=0.000000)],
#        [Transform(Location(x=246.998764, y=-0.79, z=0.001727),
#                   Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)),
#         Location(x=0.000000, y=1.000000, z=0.000000)],
#    ],
#
#    [
#        [Transform(Location(x=246.998764, y=-2.765, z=0.001696),
#                   Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)),
#         Location(x=0.000000, y=1.000000, z=0.000000)],
#        [Transform(Location(x=246.998764, y=-2.765, z=0.001696),
#                   Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)),
#         Location(x=0.000000, y=1.000000, z=0.000000)],
#        [Transform(Location(x=246.998764, y=-2.765, z=0.001696),
#                   Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)),
#         Location(x=0.000000, y=1.000000, z=0.000000)],
#    ],
#
#    [
#        [Transform(Location(x=246.998764, y=-0.765000, z=0.001730),
#                   Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)),
#         Location(x=0.000000, y=1.000000, z=0.000000)],
#        [Transform(Location(x=246.998764, y=-0.765000, z=0.001730),
#                   Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)),
#         Location(x=0.000000, y=1.000000, z=0.000000)],
#        [Transform(Location(x=246.998764, y=-0.765000, z=0.001730),
#                   Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)),
#         Location(x=0.000000, y=1.000000, z=0.000000)],
#    ],

    [
[Transform(Location(x=246.998764, y=31.209999, z=0.001727), Rotation(pitch=0.000020, yaw=-89.998703, roll=0.000002)),Location(x=0.000000, y=1.000000, z=0.000000)],
[Transform(Location(x=246.998764, y=31.209999, z=0.001727), Rotation(pitch=0.000020, yaw=-89.998703, roll=0.000002)),Location(x=0.000000, y=1.000000, z=0.000000)],
[Transform(Location(x=246.998764, y=31.209999, z=0.001727), Rotation(pitch=0.000020, yaw=-89.998703, roll=0.000002)),Location(x=0.000000, y=1.000000, z=0.000000)],
    ],

    [
[Transform(Location(x=246.998764, y=31.209999, z=0.001727), Rotation(pitch=0.000020, yaw=-89.998703, roll=0.000002)),Location(x=0.000000, y=1.000000, z=0.000000)],
[Transform(Location(x=246.998764, y=31.209999, z=0.001727), Rotation(pitch=0.000020, yaw=-89.998703, roll=0.000002)),Location(x=0.000000, y=1.000000, z=0.000000)],
[Transform(Location(x=246.998764, y=31.209999, z=0.001727), Rotation(pitch=0.000020, yaw=-89.998703, roll=0.000002)),Location(x=0.000000, y=1.000000, z=0.000000)],
    ],

    [
[Transform(Location(x=246.998764, y=32.209999, z=0.001727), Rotation(pitch=0.000020, yaw=-89.998703, roll=0.000002)),Location(x=0.000000, y=1.000000, z=0.000000)],
[Transform(Location(x=246.998764, y=32.209999, z=0.001727), Rotation(pitch=0.000020, yaw=-89.998703, roll=0.000002)),Location(x=0.000000, y=1.000000, z=0.000000)],
[Transform(Location(x=246.998764, y=32.209999, z=0.001727), Rotation(pitch=0.000020, yaw=-89.998703, roll=0.000002)),Location(x=0.000000, y=1.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=246.998947, y=-47.670425, z=0.001732),
                   Rotation(pitch=0.000034, yaw=-89.998703, roll=-0.000031)),
         Location(x=0.000000, y=1.000000, z=0.000000)],
        [Transform(Location(x=246.998947, y=-47.670425, z=0.001732),
                   Rotation(pitch=0.000034, yaw=-89.998703, roll=-0.000031)),
         Location(x=0.000000, y=1.000000, z=0.000000)],
        [Transform(Location(x=246.998947, y=-47.670425, z=0.001732),
                   Rotation(pitch=0.000034, yaw=-89.998703, roll=-0.000031)),
         Location(x=0.000000, y=1.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=246.998947, y=-50.670425, z=0.001730),
                   Rotation(pitch=0.000034, yaw=-89.998703, roll=-0.000031)),
         Location(x=0.000000, y=1.000000, z=0.000000)],
        [Transform(Location(x=246.998947, y=-50.670425, z=0.001730),
                   Rotation(pitch=0.000034, yaw=-89.998703, roll=-0.000031)),
         Location(x=0.000000, y=1.000000, z=0.000000)],
        [Transform(Location(x=246.998947, y=-50.670425, z=0.001730),
                   Rotation(pitch=0.000034, yaw=-89.998703, roll=-0.000031)),
         Location(x=0.000000, y=1.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=37.899876, y=208.000000, z=0.081553),
                   Rotation(pitch=0.218839, yaw=0.000725, roll=0.001658)),
         Location(x=-1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=37.899876, y=208.000000, z=0.081553),
                   Rotation(pitch=0.218839, yaw=0.000725, roll=0.001658)),
         Location(x=-1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=37.899876, y=208.000000, z=0.081553),
                   Rotation(pitch=0.218839, yaw=0.000725, roll=0.001658)),
         Location(x=-1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=31.899876, y=208.000000, z=0.036137),
                   Rotation(pitch=0.397271, yaw=0.001687, roll=0.001021)),
         Location(x=-1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=31.899876, y=208.000000, z=0.036137),
                   Rotation(pitch=0.397271, yaw=0.001687, roll=0.001021)),
         Location(x=-1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=31.899876, y=208.000000, z=0.036137),
                   Rotation(pitch=0.397271, yaw=0.001687, roll=0.001021)),
         Location(x=-1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=-48.695994, y=-209.999802, z=0.001692),
                   Rotation(pitch=0.000027, yaw=-179.999954, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=-48.695994, y=-209.999802, z=0.001692),
                   Rotation(pitch=0.000027, yaw=-179.999954, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=-48.695994, y=-209.999802, z=0.001692),
                   Rotation(pitch=0.000027, yaw=-179.999954, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=-50.695994, y=-209.999802, z=0.001729),
                   Rotation(pitch=0.000027, yaw=-179.999954, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=-50.695994, y=-209.999802, z=0.001729),
                   Rotation(pitch=0.000027, yaw=-179.999954, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=-50.695994, y=-209.999802, z=0.001729),
                   Rotation(pitch=0.000027, yaw=-179.999954, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=-47.695994, y=-209.999802, z=0.001684),
                   Rotation(pitch=0.000027, yaw=-179.999954, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=-47.695994, y=-209.999802, z=0.001684),
                   Rotation(pitch=0.000027, yaw=-179.999954, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=-47.695994, y=-209.999802, z=0.001684),
                   Rotation(pitch=0.000027, yaw=-179.999954, roll=-0.000031)),
         Location(x=1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=-88.999977, y=-72.900533, z=-0.821090),
                   Rotation(pitch=0.581379, yaw=90.000458, roll=0.001621)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
        [Transform(Location(x=-88.999977, y=-72.900533, z=-0.821090),
                   Rotation(pitch=0.581379, yaw=90.000458, roll=0.001621)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
        [Transform(Location(x=-88.999977, y=-72.900533, z=-0.821090),
                   Rotation(pitch=0.581379, yaw=90.000458, roll=0.001621)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=-88.999977, y=-71.600533, z=-0.821090),
                   Rotation(pitch=0.581379, yaw=90.000458, roll=0.001621)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
        [Transform(Location(x=-88.999977, y=-71.600533, z=-0.821090),
                   Rotation(pitch=0.581379, yaw=90.000458, roll=0.001621)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
        [Transform(Location(x=-88.999977, y=-71.600533, z=-0.821090),
                   Rotation(pitch=0.581379, yaw=90.000458, roll=0.001621)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=-88.999977, y=-66.400269, z=-0.715861),
                   Rotation(pitch=0.841356, yaw=89.999878, roll=0.002327)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
        [Transform(Location(x=-88.999977, y=-66.400269, z=-0.715861),
                   Rotation(pitch=0.841356, yaw=89.999878, roll=0.002327)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
        [Transform(Location(x=-88.999977, y=-66.400269, z=-0.715861),
                   Rotation(pitch=0.841356, yaw=89.999878, roll=0.002327)),
         Location(x=0.000000, y=-1.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=-39.400993, y=138.999924, z=0.001685),
                   Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
         Location(x=-1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=-39.400993, y=138.999924, z=0.001685),
                   Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
         Location(x=-1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=-39.400993, y=138.999924, z=0.001685),
                   Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
         Location(x=-1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=-28.400990, y=138.999924, z=0.001685),
                   Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
         Location(x=-1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=-28.400990, y=138.999924, z=0.001685),
                   Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
         Location(x=-1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=-28.400990, y=138.999924, z=0.001685),
                   Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
         Location(x=-1.000000, y=0.000000, z=0.000000)],
    ],

    [
        [Transform(Location(x=-44.400993, y=134.999924, z=0.001730),
                   Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
         Location(x=-1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=-44.400993, y=134.999924, z=0.001730),
                   Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
         Location(x=-1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=-44.400993, y=134.999924, z=0.001730),
                   Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
         Location(x=-1.000000, y=0.000000, z=0.000000)],
    ],

]


car_pos_opposite_t3 = [

    [Transform(Location(x=36.596676, y=3.000722, z=0.001561), Rotation(pitch=0.000266, yaw=0, roll=-0.000763)),
     Location(x=1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=36.596676, y=3.000722, z=0.001561), Rotation(pitch=0.000266, yaw=0, roll=-0.000763)),
     Location(x=1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=36.596676, y=3.000722, z=0.001561), Rotation(pitch=0.000266, yaw=0, roll=-0.000763)),
     Location(x=1.000000, y=0.000000, z=0.000000)],

    [Transform(Location(x=234.998764, y=-0.376438, z=0.001543), Rotation(pitch=0.000014, yaw=90, roll=-0.000977)),
     Location(x=0.000000, y=1.000000, z=0.000000)],
    [Transform(Location(x=234.998764, y=-0.376438, z=0.001543), Rotation(pitch=0.000014, yaw=90, roll=-0.000977)),
     Location(x=0.000000, y=1.000000, z=0.000000)],
    [Transform(Location(x=234.998764, y=-0.376438, z=0.001543), Rotation(pitch=0.000014, yaw=90, roll=-0.000977)),
     Location(x=0.000000, y=1.000000, z=0.000000)],

    [Transform(Location(x=234.998764, y=-24.375631, z=0.001696), Rotation(pitch=0.000034, yaw=90, roll=-0.000031)),
     Location(x=0.000000, y=1.000000, z=0.000000)],
    [Transform(Location(x=234.998764, y=-24.375631, z=0.001696), Rotation(pitch=0.000034, yaw=90, roll=-0.000031)),
     Location(x=0.000000, y=1.000000, z=0.000000)],

    [Transform(Location(x=31.601637, y=196.000916, z=0.012507),
               Rotation(pitch=-0.225833, yaw=-179.999878, roll=-0.000366)),
     Location(x=-1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=31.601637, y=196.000916, z=0.012507),
               Rotation(pitch=-0.225833, yaw=-179.999878, roll=-0.000366)),
     Location(x=-1.000000, y=0.000000, z=0.000000)],

    [Transform(Location(x=-50.399994, y=-197.999802, z=0.001634), Rotation(pitch=0.000116, yaw=-0.0, roll=-0.000214)),
     Location(x=1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=-50.399994, y=-197.999802, z=0.001634), Rotation(pitch=0.000116, yaw=-0.0, roll=-0.000214)),
     Location(x=1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=-50.399994, y=-197.999802, z=0.001634), Rotation(pitch=0.000116, yaw=-0.0, roll=-0.000214)),
     Location(x=1.000000, y=0.000000, z=0.000000)],

    [Transform(Location(x=-77.999557, y=-64.694176, z=-0.786894),
               Rotation(pitch=0.745406, yaw=-90.000038, roll=0.002153)), Location(x=0.000000, y=-1.000000, z=0.000000)],
    [Transform(Location(x=-77.999557, y=-64.694176, z=-0.786894),
               Rotation(pitch=0.745406, yaw=-90.000038, roll=0.002153)), Location(x=0.000000, y=-1.000000, z=0.000000)],
    [Transform(Location(x=-77.999557, y=-64.694176, z=-0.786894),
               Rotation(pitch=0.745406, yaw=-90.000038, roll=0.002153)), Location(x=0.000000, y=-1.000000, z=0.000000)],

    [Transform(Location(x=-46.700001, y=131.000000, z=0.000000),
               Rotation(pitch=0.000000, yaw=180.000000, roll=0.000000)), Location(x=-1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=-46.700001, y=131.000000, z=0.000000),
               Rotation(pitch=0.000000, yaw=180.000000, roll=0.000000)), Location(x=-1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=-46.700001, y=131.000000, z=0.000000),
               Rotation(pitch=0.000000, yaw=180.000000, roll=0.000000)), Location(x=-1.000000, y=0.000000, z=0.000000)],

]

car_pos_opposite_t1 = [

[Transform(Location(x=169.395889, y=2.000000, z=0.001730), Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=169.395889, y=2.000000, z=0.001730), Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=169.395889, y=2.000000, z=0.001730), Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=169.395889, y=2.000000, z=0.001730), Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],

[Transform(Location(x=1.999856, y=179.604065, z=0.001690), Rotation(pitch=0.000014, yaw=-89.999420, roll=0.000000)),Location(x=0.000000, y=-1.000000, z=0.000000)],
[Transform(Location(x=1.999856, y=179.604065, z=0.001690), Rotation(pitch=0.000014, yaw=-89.999420, roll=0.000000)),Location(x=0.000000, y=-1.000000, z=0.000000)],
[Transform(Location(x=1.999856, y=179.604065, z=0.001690), Rotation(pitch=0.000014, yaw=-89.999420, roll=0.000000)),Location(x=0.000000, y=-1.000000, z=0.000000)],
[Transform(Location(x=1.999856, y=179.604065, z=0.001690), Rotation(pitch=0.000014, yaw=-89.999420, roll=0.000000)),Location(x=0.000000, y=-1.000000, z=0.000000)],

[Transform(Location(x=160.395844, y=331.005920, z=0.001697), Rotation(pitch=0.000007, yaw=-0.001892, roll=-0.000061)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=160.395844, y=331.005920, z=0.001697), Rotation(pitch=0.000007, yaw=-0.001892, roll=-0.000061)),Location(x=1.000000, y=0.000000, z=0.000000)],

[Transform(Location(x=206.395889, y=60.000000, z=0.000000), Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=206.395889, y=60.000000, z=0.000000), Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=206.395889, y=60.000000, z=0.000000), Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=206.395889, y=60.000000, z=0.000000), Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],

[Transform(Location(x=169.395889, y=198.999802, z=0.001697), Rotation(pitch=0.000020, yaw=0.000000, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=169.395889, y=198.999802, z=0.001697), Rotation(pitch=0.000020, yaw=0.000000, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=169.395889, y=198.999802, z=0.001697), Rotation(pitch=0.000020, yaw=0.000000, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],

[Transform(Location(x=88.000153, y=244.395889, z=0.001690), Rotation(pitch=0.000020, yaw=90.000114, roll=-0.000031)),Location(x=0.000000, y=1.000000, z=0.000000)],
[Transform(Location(x=88.000153, y=244.395889, z=0.001690), Rotation(pitch=0.000020, yaw=90.000114, roll=-0.000031)),Location(x=0.000000, y=1.000000, z=0.000000)],
[Transform(Location(x=88.000153, y=244.395889, z=0.001690), Rotation(pitch=0.000020, yaw=90.000114, roll=-0.000031)),Location(x=0.000000, y=1.000000, z=0.000000)],


]


positions_walkers_t3=[
    # 1-3
    [Transform(Location(x=31.599997, y=-1.000000, z=1.000000),
               Rotation(pitch=-0.500004, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=33.599998, y=-1.000000, z=1.000000),
               Rotation(pitch=-0.500004, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=46.599998, y=-1.000000, z=1.000000),
               Rotation(pitch=-0.500004, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=50.599998, y=-1.000000, z=1.000000),
               Rotation(pitch=-0.500004, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=56.599998, y=-1.000000, z=1.000000),
               Rotation(pitch=-0.500004, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=64.599998, y=-1.000000, z=1.000000),
               Rotation(pitch=-0.500004, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=71.599998, y=-1.000000, z=1.000000),
               Rotation(pitch=-0.500004, yaw=-179.999954, roll=0.000000)), ],

        # 4-8
    [
Transform(Location(x=250.998764, y=18.234997, z=1.001731), Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)),
Transform(Location(x=250.998764, y=22.234997, z=1.001731), Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)),
Transform(Location(x=250.998764, y=26.234997, z=1.001731), Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)),
Transform(Location(x=251.998764, y=30.234997, z=1.001731), Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)),
Transform(Location(x=251.998764, y=39.234997, z=1.001731), Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)),
Transform(Location(x=250.998764, y=47.234993, z=1.001731), Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)),
Transform(Location(x=250.998764, y=54.234993, z=1.001731), Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)),
Transform(Location(x=225.998764, y=83.234978, z=1.001731), Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)),
Transform(Location(x=225.998764, y=93.234978, z=1.001731), Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)),


        Transform(Location(x=252.000000, y=-42.399998, z=1.000000),
               Rotation(pitch=2.499999, yaw=-90.000000, roll=-0.000000)),
     Transform(Location(x=252.000000, y=-35.399998, z=1.000000),
               Rotation(pitch=2.499999, yaw=-90.000000, roll=-0.000000)),
     Transform(Location(x=252.000000, y=-22.399998, z=1.000000),
               Rotation(pitch=2.499999, yaw=-90.000000, roll=-0.000000)),
     Transform(Location(x=251.000000, y=-3.399995, z=1.000000),
               Rotation(pitch=2.499999, yaw=-90.000000, roll=-0.000000)),
     Transform(Location(x=251.000000, y=3.600005, z=1.000000),
               Rotation(pitch=2.499999, yaw=-90.000000, roll=-0.000000)),
     Transform(Location(x=251.000000, y=12.600003, z=1.000000),
               Rotation(pitch=2.499999, yaw=-90.000000, roll=-0.000000)),
     Transform(Location(x=251.000000, y=20.600002, z=1.000000),
               Rotation(pitch=2.499999, yaw=-90.000000, roll=-0.000000)),
     Transform(Location(x=256.000000, y=6.600003, z=1.000000),
               Rotation(pitch=2.499999, yaw=-90.000000, roll=-0.000000)),
     Transform(Location(x=256.000000, y=-5.399997, z=1.000000),
               Rotation(pitch=2.499999, yaw=-90.000000, roll=-0.000000)),
     Transform(Location(x=219.000000, y=2.600004, z=1.000000),
               Rotation(pitch=2.499999, yaw=-90.000000, roll=-0.000000)),
     Transform(Location(x=224.000000, y=25.600002, z=1.000000),
               Rotation(pitch=2.499999, yaw=-90.000000, roll=-0.000000)),
     Transform(Location(x=224.000000, y=34.600002, z=1.000000),
               Rotation(pitch=2.499999, yaw=-90.000000, roll=-0.000000)),],

        # 9-10
    [Transform(Location(x=35.599998, y=188.000000, z=1.000000),
               Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=31.599997, y=188.000000, z=1.000000),
               Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=25.599997, y=188.000000, z=1.000000),
               Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=16.599997, y=188.000000, z=1.000000),
               Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=43.599998, y=213.000000, z=1.000000),
               Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=37.599998, y=213.000000, z=1.000000),
               Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=35.599998, y=213.000000, z=1.000000),
               Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=31.599997, y=213.000000, z=1.000000),
               Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=23.599997, y=213.000000, z=1.000000),
               Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=12.599995, y=213.000000, z=1.000000),
               Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=2.599993, y=213.000000, z=1.000000),
               Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=-19.400002, y=186.000000, z=1.000000),
               Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),],

        # 11-13
    [Transform(Location(x=-59.399994, y=-216.000000, z=1.000000),
               Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=-55.399994, y=-216.000000, z=1.000000),
               Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=-46.399994, y=-217.000000, z=1.000000),
               Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=-42.399994, y=-216.000000, z=1.000000),
               Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=-28.399994, y=-215.000000, z=1.000000),
               Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
     Transform(Location(x=-16.399994, y=-188.000000, z=1.000000),
               Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),],

        # 14-16
    [Transform(Location(x=-95.000000, y=-63.699993, z=0.575210),
               Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
     Transform(Location(x=-95.000000, y=-66.699997, z=0.575210),
               Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
     Transform(Location(x=-95.000000, y=-73.699997, z=0.575210),
               Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
     Transform(Location(x=-95.000000, y=-85.699997, z=0.575210),
               Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
     Transform(Location(x=-95.000000, y=-92.699997, z=0.575210),
               Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
     Transform(Location(x=-97.000000, y=-75.699997, z=0.575210),
               Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
     Transform(Location(x=-70.000000, y=-66.699997, z=0.575210),
               Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
     Transform(Location(x=-70.000000, y=-77.699997, z=0.575210),
               Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
     Transform(Location(x=-70.000000, y=-82.699997, z=0.575210),
               Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
     Transform(Location(x=-96.000000, y=-82.699997, z=0.575210),
               Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
     Transform(Location(x=-96.000000, y=-76.699997, z=0.575210),
               Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),],

        # 17-19
    [Transform(Location(x=-47.699993, y=123.000000, z=1.000000), Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
     Transform(Location(x=-49.699993, y=123.000000, z=1.000000), Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
     Transform(Location(x=-55.699993, y=123.000000, z=1.000000), Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
     Transform(Location(x=-59.699993, y=123.000000, z=1.000000), Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
     Transform(Location(x=-62.699993, y=122.000000, z=1.000000), Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
     Transform(Location(x=-107.699997, y=124.000000, z=1.000000),
               Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
     Transform(Location(x=-40.699989, y=142.000000, z=1.000000), Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
     Transform(Location(x=-44.699989, y=142.000000, z=1.000000), Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
     Transform(Location(x=-55.699989, y=142.000000, z=1.000000), Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
     Transform(Location(x=-64.699989, y=142.000000, z=1.000000), Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
     Transform(Location(x=-79.699989, y=143.000000, z=1.000000), Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
     Transform(Location(x=-62.699989, y=118.000000, z=1.000000), Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
     Transform(Location(x=-62.699989, y=147.000000, z=1.000000),
               Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),],
]


positions_walkers_t1=[
#1-4
[
Transform(Location(x=163.412308, y=-6.000000, z=1.000000), Rotation(pitch=0.000000, yaw=179.999954, roll=0.000000)),
Transform(Location(x=165.412308, y=-6.000000, z=1.000000), Rotation(pitch=0.000000, yaw=179.999954, roll=0.000000)),
Transform(Location(x=170.412308, y=-6.000000, z=1.000000), Rotation(pitch=0.000000, yaw=179.999954, roll=0.000000)),
Transform(Location(x=179.412308, y=-6.000000, z=1.000000), Rotation(pitch=0.000000, yaw=179.999954, roll=0.000000)),
Transform(Location(x=189.412308, y=-6.000000, z=1.000000), Rotation(pitch=0.000000, yaw=179.999954, roll=0.000000)),
Transform(Location(x=200.412308, y=-5.000000, z=1.000000), Rotation(pitch=0.000000, yaw=179.999954, roll=0.000000)),
Transform(Location(x=210.412308, y=-5.000000, z=1.000000), Rotation(pitch=0.000000, yaw=179.999954, roll=0.000000)),
Transform(Location(x=216.412308, y=5.000000, z=1.000000), Rotation(pitch=0.000000, yaw=179.999954, roll=0.000000)),
Transform(Location(x=207.412308, y=5.000000, z=1.000000), Rotation(pitch=0.000000, yaw=179.999954, roll=0.000000)),
Transform(Location(x=195.412308, y=6.000000, z=1.000000), Rotation(pitch=0.000000, yaw=179.999954, roll=0.000000)),
Transform(Location(x=186.412308, y=6.000000, z=1.000000), Rotation(pitch=0.000000, yaw=179.999954, roll=0.000000)),
Transform(Location(x=176.412308, y=6.000000, z=1.000000), Rotation(pitch=0.000000, yaw=179.999954, roll=0.000000)),
Transform(Location(x=171.412308, y=6.000000, z=1.000000), Rotation(pitch=0.000000, yaw=179.999954, roll=0.000000)),
Transform(Location(x=168.412308, y=7.000000, z=1.000000), Rotation(pitch=0.000000, yaw=179.999954, roll=0.000000)),],

#5-8
[
Transform(Location(x=-7.000000, y=181.587677, z=1.000000), Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
Transform(Location(x=-6.000000, y=180.587677, z=1.000000), Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
Transform(Location(x=-6.000000, y=176.587677, z=1.000000), Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
Transform(Location(x=-6.000000, y=172.587677, z=1.000000), Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
Transform(Location(x=-6.000000, y=166.587677, z=1.000000), Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
Transform(Location(x=-6.000000, y=159.587677, z=1.000000), Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
Transform(Location(x=-7.000000, y=144.587677, z=1.000000), Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
Transform(Location(x=-7.000000, y=130.587677, z=1.000000), Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
Transform(Location(x=6.000000, y=140.587677, z=1.000000), Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
Transform(Location(x=6.000000, y=146.587677, z=1.000000), Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
Transform(Location(x=6.000000, y=155.587677, z=1.000000), Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
Transform(Location(x=6.000000, y=164.587677, z=1.000000), Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
Transform(Location(x=6.000000, y=172.587677, z=1.000000), Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
Transform(Location(x=6.000000, y=178.587677, z=1.000000), Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),
Transform(Location(x=5.000000, y=180.587677, z=1.000000), Rotation(pitch=0.000000, yaw=89.999962, roll=0.000000)),],
#9-10
[
Transform(Location(x=158.412323, y=334.000000, z=1.000000), Rotation(pitch=0.000000, yaw=179.999954, roll=0.000000)),
Transform(Location(x=162.412323, y=334.000000, z=1.000000), Rotation(pitch=0.000000, yaw=179.999954, roll=0.000000)),
Transform(Location(x=171.412308, y=334.000000, z=1.000000), Rotation(pitch=0.000000, yaw=179.999954, roll=0.000000)),
Transform(Location(x=180.412308, y=334.000000, z=1.000000), Rotation(pitch=0.000000, yaw=179.999954, roll=0.000000)),
Transform(Location(x=194.412308, y=334.000000, z=1.000000), Rotation(pitch=0.000000, yaw=179.999954, roll=0.000000)),
Transform(Location(x=201.412308, y=334.000000, z=1.000000), Rotation(pitch=0.000000, yaw=179.999954, roll=0.000000)),],

#11-14
[
Transform(Location(x=201.412308, y=51.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.500000, roll=0.000000)),
Transform(Location(x=204.412308, y=51.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.500000, roll=0.000000)),
Transform(Location(x=207.412308, y=51.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.500000, roll=0.000000)),
Transform(Location(x=211.412308, y=51.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.500000, roll=0.000000)),
Transform(Location(x=217.412308, y=51.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.500000, roll=0.000000)),
Transform(Location(x=223.412308, y=51.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.500000, roll=0.000000)),
Transform(Location(x=234.412308, y=51.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.500000, roll=0.000000)),
Transform(Location(x=240.412308, y=50.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.500000, roll=0.000000)),
Transform(Location(x=241.412308, y=64.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.500000, roll=0.000000)),
Transform(Location(x=230.412308, y=64.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.500000, roll=0.000000)),
Transform(Location(x=225.412308, y=63.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.500000, roll=0.000000)),
Transform(Location(x=212.412308, y=63.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.500000, roll=0.000000)),
Transform(Location(x=205.412308, y=63.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.500000, roll=0.000000)),
Transform(Location(x=210.412308, y=70.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.500000, roll=0.000000)),],


#15-17
[
Transform(Location(x=166.412308, y=191.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=168.412308, y=191.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=168.412308, y=188.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=171.412308, y=188.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=171.412308, y=192.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=175.412308, y=192.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=176.412308, y=188.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=178.412308, y=192.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=182.412308, y=188.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=188.412308, y=188.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=188.412308, y=191.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=197.412308, y=189.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=208.412308, y=189.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=206.412308, y=203.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=197.412308, y=203.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=192.412308, y=203.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=184.412308, y=203.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=184.412308, y=205.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=176.412308, y=205.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=170.412308, y=205.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=170.412308, y=207.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=166.412308, y=205.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),
Transform(Location(x=164.412308, y=203.000000, z=1.000000), Rotation(pitch=0.000000, yaw=-179.999954, roll=0.000000)),],

#18
[
Transform(Location(x=97.000000, y=239.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=97.000000, y=241.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=97.000000, y=244.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=97.000000, y=249.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=97.000000, y=254.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=97.000000, y=261.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=97.000000, y=267.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=97.000000, y=273.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=97.000000, y=285.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=96.000000, y=307.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=99.000000, y=307.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=99.000000, y=284.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=99.000000, y=266.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=99.000000, y=255.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=98.000000, y=249.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=102.000000, y=251.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=102.000000, y=242.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=101.000000, y=240.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=100.000000, y=242.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=100.000000, y=247.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=85.000000, y=242.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=83.000000, y=248.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=83.000000, y=253.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=85.000000, y=256.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=85.000000, y=264.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=85.000000, y=270.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=85.000000, y=275.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=85.000000, y=288.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=85.000000, y=297.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),
Transform(Location(x=85.000000, y=311.000000, z=1.000000), Rotation(pitch=-21.991636, yaw=106.558693, roll=0.000106)),],

]

list_live_test_camera_locations_t1=[
[
Transform(Location(x=-4.000000, y=285.000000, z=8.000000), Rotation(pitch=-5.498894, yaw=-90.477783, roll=0.000088)),
Transform(Location(x=-1.000000, y=21.395889, z=2.000000), Rotation(pitch=0.000000, yaw=90.499374, roll=0.000000)),Location(x=0.000000, y=-1.000000, z=0.000000),

],

[
Transform(Location(x=117.000000, y=54.000000, z=8.000000), Rotation(pitch=-5.998846, yaw=-0.478960, roll=0.000081)),
Transform(Location(x=323.604095, y=56.000000, z=2.000000), Rotation(pitch=-0.000061, yaw=-178.502090, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000),

],

]

list_live_test_camera_locations_t3=[

    [
Transform(Location(x=39.000000, y=189.000000, z=8.000000), Rotation(pitch=-9.497165, yaw=6.014590, roll=0.000001)),
Transform(Location(x=152.604111, y=193.000000, z=3.000000), Rotation(pitch=0.000000, yaw=176.497650, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000),

],
    [
Transform(Location(x=224.000000, y=17.000000, z=8.000000), Rotation(pitch=-6.997276, yaw=-172.000336, roll=0.000055)),
Transform(Location(x=38.237736, y=6.967196, z=1.484459), Rotation(pitch=-0.036378, yaw=-0.057861, roll=0.099393)),Location(x=-1.000000, y=0.000000, z=0.000000),

    ],




]



































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

list_lkw = [
    "vehicle.carlamotors.carlacola",
]
list_bycicle = [

    "vehicle.bh.crossbike",
    "vehicle.gazelle.omafiets",
    "vehicle.diamondback.century",
]
list_others = [

    "vehicle.volkswagen.t2",

]



# data size: goal is maybe 100 KB per image.
# 10% empty images  30K per class: total 100.000 images : total size goal 10 GB data
#

all_cars_lists_old = [
    ["walker.pedestrian.0012","walker.pedestrian.0016","static.prop.bench01", "static.prop.clothcontainer", "static.prop.vendingmachine" ],  # also empty and 2 props
list_cars,
list_bikes,
list_lkw,
]
# list_others ,

cars_old_train = [
    ["static.prop.advertisement","walker.pedestrian.0012", "walker.pedestrian.0016", "static.prop.bench01", "static.prop.clothcontainer",
     "static.prop.vendingmachine"],
[  "vehicle.chevrolet.impala",
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
    "vehicle.mercedes-benz.coupe",],
["vehicle.harley-davidson.low_rider",
    "vehicle.yamaha.yzf",],
[ "vehicle.carlamotors.carlacola",],
[
    "vehicle.bh.crossbike",
    "vehicle.gazelle.omafiets",
],
]

cars_old_test = [
["static.prop.glasscontainer","walker.pedestrian.0017","walker.pedestrian.0019","static.prop.bench02", "static.prop.busstop", "static.prop.box02" ],
[    "vehicle.mini.cooperst",
    "vehicle.nissan.patrol",
    "vehicle.seat.leon",
    "vehicle.toyota.prius",

    "vehicle.tesla.model3",
    "vehicle.tesla.cybertruck",
    "vehicle.audi.etron",
    "vehicle.lincoln.mkz2017",

    "vehicle.mustang.mustang",
    "vehicle.lincoln2020.mkz2020",
    "vehicle.charger2020.charger2020",],
["vehicle.kawasaki.ninja",],
[ "vehicle.carlamotors.carlacola",],
[
    "vehicle.diamondback.century",
],
]


def dot(vec1, vec2):
    return vec1.x * vec2.x + vec1.y * vec2.y + vec1.z * vec2.z


BB_COLOR = (248, 64, 24)


# test daten:  pro wetter gibt es ne rotation dazu


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
    focal = w / (2.0 * np.tan(fov * np.pi / 360.0))
    K = np.identity(3)
    K[0, 0] = K[1, 1] = focal
    K[0, 2] = w / 2.0
    K[1, 2] = h / 2.0
    return K








































"""
# Old Stuff 2
cam_pos_t1_c = [
   [
    [Transform(Location(x=158.000000, y=-4.000000, z=8.000000),
               Rotation(pitch=-21.999784, yaw=7.003734, roll=0.000003)),
     Transform(Location(x=158.000000, y=-4.000000, z=4.000000),
               Rotation(pitch=-14.999689, yaw=9.508002, roll=0.000001)),
     Transform(Location(x=158.000000, y=-8.000000, z=4.000000),
               Rotation(pitch=-8.999750, yaw=18.509815, roll=0.000000)),
     Transform(Location(x=158.000000, y=-8.000000, z=8.000000),
               Rotation(pitch=-21.499447, yaw=19.011110, roll=0.000002)), ],

    [Transform(Location(x=-4.000000, y=188.000000, z=8.000000),
               Rotation(pitch=-21.999266, yaw=-82.484245, roll=0.000028)),
     Transform(Location(x=-4.000000, y=188.000000, z=4.000000),
               Rotation(pitch=-13.999264, yaw=-82.483452, roll=0.000038)),
     Transform(Location(x=-8.000000, y=188.000000, z=4.000000),
               Rotation(pitch=-11.998838, yaw=-69.981018, roll=0.000044)),
     Transform(Location(x=-8.000000, y=188.000000, z=8.000000),
               Rotation(pitch=-20.498770, yaw=-69.481377, roll=0.000025)), ],

    [Transform(Location(x=151.000000, y=324.000000, z=4.000000),
               Rotation(pitch=-19.499172, yaw=11.506786, roll=0.000055)),
     Transform(Location(x=151.000000, y=324.000000, z=6.000000),
               Rotation(pitch=-21.498894, yaw=14.013792, roll=0.000067)), ],

    [Transform(Location(x=197.000000, y=54.000000, z=4.000000),
               Rotation(pitch=-13.498810, yaw=5.516876, roll=0.000072)),
     Transform(Location(x=197.000000, y=54.000000, z=8.000000),
               Rotation(pitch=-23.498840, yaw=3.016092, roll=0.000070)),
     Transform(Location(x=197.000000, y=50.000000, z=4.000000),
               Rotation(pitch=-11.998811, yaw=17.018867, roll=0.000075)),
     Transform(Location(x=197.000000, y=50.000000, z=8.000000),
               Rotation(pitch=-23.498779, yaw=18.021101, roll=0.000071)), ],

    [Transform(Location(x=162.000000, y=192.000000, z=7.000000),
               Rotation(pitch=-20.998350, yaw=15.035479, roll=0.000061)),
     Transform(Location(x=162.000000, y=188.000000, z=7.000000),
               Rotation(pitch=-19.998472, yaw=23.030212, roll=0.000054)),
     Transform(Location(x=162.000000, y=192.000000, z=12.000000),
               Rotation(pitch=-39.492481, yaw=17.555870, roll=0.000068)), ],

    [Transform(Location(x=98.000000, y=234.000000, z=8.000000),
                Rotation(pitch=-21.991636, yaw=106.558609, roll=0.000105)),],
]



cam_pos_t3_c = [
    [Transform(Location(x=26.000000, y=-13.000000, z=8.000000), Rotation(pitch=-19.997707, yaw=22.494951, roll=0.000000)),
Transform(Location(x=25.000000, y=-12.000000, z=4.000000), Rotation(pitch=-7.997680, yaw=21.986094, roll=0.000001)),
     Transform(Location(x=28.000000, y=-13.000000, z=6.000000), Rotation(pitch=-14.997428, yaw=24.979946, roll=0.000024)),
     ],

    [Transform(Location(x=252.000000, y=-15.000000, z=8.000000),
               Rotation(pitch=-20.493954, yaw=107.990952, roll=0.000029)),
     Transform(Location(x=251.000000, y=-15.000000, z=4.000000),
               Rotation(pitch=-9.493833, yaw=109.491188, roll=0.000062)),
     Transform(Location(x=257.000000, y=-15.000000, z=8.000000),
               Rotation(pitch=-20.493893, yaw=124.990349, roll=0.000041)),

     Transform(Location(x=252.000000, y=-49.000000, z=11.000000),
               Rotation(pitch=-25.493038, yaw=106.999550, roll=0.000024)),
     Transform(Location(x=253.000000, y=-54.000000, z=8.000000),
               Rotation(pitch=-11.993832, yaw=103.993469, roll=0.000039)),
     ],
    [
Transform(Location(x=51.000000, y=214.000000, z=8.000000), Rotation(pitch=-15.492582, yaw=-160.490005, roll=0.000070)),
                Transform(Location(x=46.000000, y=214.000000, z=6.000000), Rotation(pitch=-16.492489, yaw=-158.489731, roll=0.000073)),
],

    [Transform(Location(x=-68.000000, y=-216.000000, z=8.000000),
               Rotation(pitch=-14.991725, yaw=13.014227, roll=0.000152)),
     Transform(Location(x=-68.000000, y=-216.000000, z=4.000000),
               Rotation(pitch=-6.991730, yaw=16.017057, roll=0.000153)),
     Transform(Location(x=-68.000000, y=-219.000000, z=4.000000), Rotation(pitch=-9.491671, yaw=17.514860, roll=0.000157)),],

    [  Transform(Location(x=-97.000000, y=-60.000000, z=8.000000),
               Rotation(pitch=-35.998161, yaw=-44.999874, roll=0.000001)),
     Transform(Location(x=-97.000000, y=-60.000000, z=4.000000),
               Rotation(pitch=-18.497982, yaw=-43.999771, roll=0.000013)),
Transform(Location(x=-95.000000, y=-51.000000, z=6.000000), Rotation(pitch=-16.497705, yaw=-67.496742, roll=0.000028)),
     ],

    [  Transform(Location(x=-43.000000, y=144.000000, z=8.000000),
               Rotation(pitch=-31.488836, yaw=-136.479706, roll=0.000032)),
Transform(Location(x=-42.000000, y=145.000000, z=4.000000), Rotation(pitch=-11.483638, yaw=-145.481155, roll=0.000097)),
     Transform(Location(x=-37.000000, y=142.000000, z=4.000000),
               Rotation(pitch=-11.483638, yaw=-156.481155, roll=0.000098)),
     ],
]



car_pos_targets_t1 = [

[Transform(Location(x=167.604080, y=-1.999993, z=0.001584), Rotation(pitch=0.000178, yaw=179.997025, roll=-0.000366)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=165.604080, y=-1.999990, z=0.001730), Rotation(pitch=0.000027, yaw=179.997025, roll=-0.000031)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=168.604954, y=-1.999990, z=0.001697), Rotation(pitch=0.000027, yaw=179.997025, roll=-0.000031)),Location(x=1.000000, y=0.000000, z=0.000000)],

[Transform(Location(x=166.604065, y=-1.999990, z=0.001730), Rotation(pitch=0.000027, yaw=179.997025, roll=-0.000031)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=163.604065, y=-1.999990, z=0.001731), Rotation(pitch=0.000027, yaw=179.997025, roll=-0.000031)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=166.604954, y=-1.999990, z=0.001686), Rotation(pitch=0.000027, yaw=179.997025, roll=-0.000031)),Location(x=1.000000, y=0.000000, z=0.000000)],

[Transform(Location(x=168.604065, y=-1.999990, z=0.001733), Rotation(pitch=0.000027, yaw=179.997025, roll=-0.000031)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=165.604065, y=-1.999990, z=0.001732), Rotation(pitch=0.000027, yaw=179.997025, roll=-0.000031)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=168.604954, y=-1.999990, z=0.001732), Rotation(pitch=0.000027, yaw=179.997025, roll=-0.000031)),Location(x=1.000000, y=0.000000, z=0.000000)],

[Transform(Location(x=167.604065, y=-1.999990, z=0.001733), Rotation(pitch=0.000027, yaw=179.997025, roll=-0.000031)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=164.604065, y=-1.999990, z=0.001686), Rotation(pitch=0.000027, yaw=179.997025, roll=-0.000031)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=168.604954, y=-1.999990, z=0.001730), Rotation(pitch=0.000027, yaw=179.997025, roll=-0.000031)),Location(x=1.000000, y=0.000000, z=0.000000)],


[Transform(Location(x=-1.999993, y=178.395905, z=0.001454), Rotation(pitch=0.000239, yaw=89.999374, roll=-0.000488)),Location(x=0.000000, y=-1.000000, z=0.000000)],
[Transform(Location(x=-1.999990, y=180.395889, z=0.001728), Rotation(pitch=0.000027, yaw=89.999374, roll=-0.000031)),Location(x=0.000000, y=-1.000000, z=0.000000)],
[Transform(Location(x=-1.999990, y=178.395000, z=0.001687), Rotation(pitch=0.000027, yaw=89.999374, roll=-0.000031)),Location(x=0.000000, y=-1.000000, z=0.000000)],

[Transform(Location(x=-1.999990, y=179.395889, z=0.001699), Rotation(pitch=0.000027, yaw=89.999374, roll=-0.000031)),Location(x=0.000000, y=-1.000000, z=0.000000)],
[Transform(Location(x=-1.999990, y=182.395889, z=0.001733), Rotation(pitch=0.000027, yaw=89.999374, roll=-0.000031)),Location(x=0.000000, y=-1.000000, z=0.000000)],
[Transform(Location(x=-1.999990, y=179.395000, z=0.001733), Rotation(pitch=0.000027, yaw=89.999374, roll=-0.000031)),Location(x=0.000000, y=-1.000000, z=0.000000)],

[Transform(Location(x=-1.999990, y=178.395889, z=0.001732), Rotation(pitch=0.000027, yaw=89.999374, roll=-0.000031)),Location(x=0.000000, y=-1.000000, z=0.000000)],
[Transform(Location(x=-1.999990, y=181.395889, z=0.001685), Rotation(pitch=0.000027, yaw=89.999374, roll=-0.000031)),Location(x=0.000000, y=-1.000000, z=0.000000)],
[Transform(Location(x=-1.999990, y=178.395000, z=0.001730), Rotation(pitch=0.000027, yaw=89.999374, roll=-0.000031)),Location(x=0.000000, y=-1.000000, z=0.000000)],

[Transform(Location(x=-1.999990, y=178.395889, z=0.001687), Rotation(pitch=0.000027, yaw=89.999374, roll=-0.000031)),Location(x=0.000000, y=-1.000000, z=0.000000)],
[Transform(Location(x=-1.999990, y=181.395889, z=0.001700), Rotation(pitch=0.000027, yaw=89.999374, roll=-0.000031)),Location(x=0.000000, y=-1.000000, z=0.000000)],
[Transform(Location(x=-1.999990, y=177.395000, z=0.001731), Rotation(pitch=0.000027, yaw=89.999374, roll=-0.000031)),Location(x=0.000000, y=-1.000000, z=0.000000)],


[Transform(Location(x=156.604111, y=326.000000, z=0.001674), Rotation(pitch=0.000000, yaw=179.997589, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=155.604111, y=326.000000, z=0.001674), Rotation(pitch=0.000000, yaw=179.997589, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=157.605000, y=326.000000, z=0.001674), Rotation(pitch=0.000000, yaw=179.997589, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],

[Transform(Location(x=158.604111, y=326.000000, z=0.001674), Rotation(pitch=0.000000, yaw=179.997589, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=156.604111, y=326.000000, z=0.001674), Rotation(pitch=0.000000, yaw=179.997589, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=159.605000, y=326.000000, z=0.001674), Rotation(pitch=0.000000, yaw=179.997589, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],


[Transform(Location(x=205.604111, y=55.000000, z=0.001096), Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=203.604111, y=55.000000, z=0.001096), Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=204.605000, y=55.000000, z=0.001096), Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],

[Transform(Location(x=206.604111, y=55.000000, z=0.001096), Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=203.604111, y=55.000000, z=0.001096), Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=207.605000, y=55.000000, z=0.001096), Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],

[Transform(Location(x=207.604111, y=55.000000, z=0.001096), Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=202.604111, y=55.000000, z=0.001096), Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=206.605000, y=55.000000, z=0.001096), Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],

[Transform(Location(x=206.604111, y=55.000000, z=0.001096), Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=203.604111, y=55.000000, z=0.001096), Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=205.605000, y=55.000000, z=0.001096), Rotation(pitch=0.500004, yaw=179.993637, roll=0.000000)),Location(x=1.000000, y=0.000000, z=0.000000)],


[Transform(Location(x=172.604065, y=195.000198, z=0.001690), Rotation(pitch=0.000034, yaw=179.997543, roll=-0.000031)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=169.604065, y=195.000198, z=0.001731), Rotation(pitch=0.000034, yaw=179.997543, roll=-0.000031)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=170.604954, y=195.000198, z=0.001690), Rotation(pitch=0.000034, yaw=179.997543, roll=-0.000031)),Location(x=1.000000, y=0.000000, z=0.000000)],

[Transform(Location(x=173.604065, y=195.000198, z=0.001697), Rotation(pitch=0.000034, yaw=179.997543, roll=-0.000031)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=170.604065, y=195.000198, z=0.001700), Rotation(pitch=0.000034, yaw=179.997543, roll=-0.000031)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=171.604954, y=195.000198, z=0.001731), Rotation(pitch=0.000034, yaw=179.997543, roll=-0.000031)),Location(x=1.000000, y=0.000000, z=0.000000)],

[Transform(Location(x=170.604065, y=195.000198, z=0.001688), Rotation(pitch=0.000034, yaw=179.997543, roll=-0.000031)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=168.604065, y=195.000198, z=0.001685), Rotation(pitch=0.000034, yaw=179.997543, roll=-0.000031)),Location(x=1.000000, y=0.000000, z=0.000000)],
[Transform(Location(x=170.604954, y=195.000198, z=0.001693), Rotation(pitch=0.000034, yaw=179.997543, roll=-0.000031)),Location(x=1.000000, y=0.000000, z=0.000000)],


[Transform(Location(x=92.781570, y=245.588165, z=0.001733), Rotation(pitch=0.000027, yaw=-89.903526, roll=0.000000)),Location(x=0.000000, y=1.000000, z=0.000000)],
[Transform(Location(x=92.781570, y=241.747772, z=0.001733), Rotation(pitch=0.000027, yaw=-89.903526, roll=0.000000)),Location(x=0.000000, y=1.000000, z=0.000000)],
[Transform(Location(x=92.781563, y=244.252222, z=0.001686), Rotation(pitch=0.000075, yaw=-89.903221, roll=0.000021)),Location(x=0.000000, y=1.000000, z=0.000000)],

]


car_pos_targets_t3 = [

    [Transform(Location(x=39.200790, y=-3.999278, z=0.031561),
               Rotation(pitch=0.000266, yaw=179.999893, roll=-0.000763)), Location(x=1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=35.200790, y=-3.999272, z=0.031731), Rotation(pitch=0.000020, yaw=179.999893, roll=0.000000)),
     Location(x=1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=40.26680, y=-3.999272, z=0.031731), Rotation(pitch=0.000020, yaw=179.999893, roll=0.000000)),
                Location(x=1.000000, y=0.000000, z=0.000000)],

    [Transform(Location(x=38.200790, y=-3.999272, z=0.001689), Rotation(pitch=0.000020, yaw=179.999893, roll=0.000000)),
     Location(x=1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=35.200790, y=-3.999272, z=0.001689), Rotation(pitch=0.000020, yaw=179.999893, roll=0.000000)),
     Location(x=1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=39.26680, y=-3.999272, z=0.001689), Rotation(pitch=0.000020, yaw=179.999893, roll=0.000000)),
     Location(x=1.000000, y=0.000000, z=0.000000)],

    [Transform(Location(x=40.200790, y=-3.999272, z=0.001729), Rotation(pitch=0.000020, yaw=179.999893, roll=0.000000)),
     Location(x=1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=37.200790, y=-3.999272, z=0.001729), Rotation(pitch=0.000020, yaw=179.999893, roll=0.000000)),
     Location(x=1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=41.26680, y=-3.999272, z=0.001729), Rotation(pitch=0.000020, yaw=179.999893, roll=0.000000)),
     Location(x=1.000000, y=0.000000, z=0.000000)],

    [Transform(Location(x=246.998764, y=-3.771326, z=0.001688),
               Rotation(pitch=0.000253, yaw=-89.498711, roll=-0.000336)), Location(x=0.000000, y=1.000000, z=0.000000)],
    [Transform(Location(x=246.998764, y=-6.771324, z=0.001685),
               Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)), Location(x=0.000000, y=1.000000, z=0.000000)],
    [Transform(Location(x=246.998764, y=-0.79, z=0.001727),
               Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)), Location(x=0.000000, y=1.000000, z=0.000000)],

    [Transform(Location(x=246.998764, y=-4.771322, z=0.001685),
               Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)), Location(x=0.000000, y=1.000000, z=0.000000)],
    [Transform(Location(x=246.998764, y=-7.771322, z=0.001730),
               Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)), Location(x=0.000000, y=1.000000, z=0.000000)],
    [Transform(Location(x=246.998764, y=-2.765, z=0.001696),
               Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)), Location(x=0.000000, y=1.000000, z=0.000000)],

    [Transform(Location(x=246.998764, y=-4.771322, z=0.001689),
               Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)), Location(x=0.000000, y=1.000000, z=0.000000)],
    [Transform(Location(x=246.998764, y=-6.771322, z=0.001684),
               Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)), Location(x=0.000000, y=1.000000, z=0.000000)],
    [Transform(Location(x=246.998764, y=-3.765, z=0.001730),
               Rotation(pitch=0.000020, yaw=-89.498711, roll=0.000002)), Location(x=0.000000, y=1.000000, z=0.000000)],

    [Transform(Location(x=246.998947, y=-34.771408, z=0.001688),
               Rotation(pitch=0.000246, yaw=-89.998703, roll=-0.000336)), Location(x=0.000000, y=1.000000, z=0.000000)],
    [Transform(Location(x=246.998947, y=-38.771404, z=0.001696),
               Rotation(pitch=0.000034, yaw=-89.998703, roll=-0.000031)), Location(x=0.000000, y=1.000000, z=0.000000)],
    [Transform(Location(x=246.998947, y=-33.670427, z=0.001732),
               Rotation(pitch=0.000034, yaw=-89.998703, roll=-0.000031)), Location(x=0.000000, y=1.000000, z=0.000000)],

    [Transform(Location(x=246.998947, y=-36.75, z=0.001685),
               Rotation(pitch=0.000034, yaw=-89.998703, roll=-0.000031)), Location(x=0.000000, y=1.000000, z=0.000000)],
    [Transform(Location(x=246.998947, y=-42.75, z=0.001732),
               Rotation(pitch=0.000034, yaw=-89.998703, roll=-0.000031)), Location(x=0.000000, y=1.000000, z=0.000000)],
    [Transform(Location(x=246.998947, y=-34.670427, z=0.001730),
               Rotation(pitch=0.000034, yaw=-89.998703, roll=-0.000031)), Location(x=0.000000, y=1.000000, z=0.000000)],


        [Transform(Location(x=33.000000, y=204.000000, z=0.000000),
                  Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)), Location(x=-1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=38.002769, y=204.000000, z=0.053115),
                  Rotation(pitch=0.299963, yaw=0.000458, roll=0.001274)),Location(x=-1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=31.899876, y=204.000000, z=0.081553),
                  Rotation(pitch=0.218842, yaw=0.000725, roll=0.001658)),Location(x=-1.000000, y=0.000000, z=0.000000)],

        [Transform(Location(x=27.999887, y=204.000000, z=0.003453),
                  Rotation(pitch=0.076109, yaw=0.001206, roll=0.000209)),Location(x=-1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=33.001118, y=204.000000, z=0.019926),
                  Rotation(pitch=0.276629, yaw=0.001283, roll=0.000855)),Location(x=-1.000000, y=0.000000, z=0.000000)],
        [Transform(Location(x=27.899876, y=204.000000, z=0.036137),
                  Rotation(pitch=0.397271, yaw=0.001687, roll=0.001021)),Location(x=-1.000000, y=0.000000, z=0.000000)],

    [Transform(Location(x=-50.795883, y=-209.999802, z=0.001729),
               Rotation(pitch=0.000027, yaw=-179.999954, roll=-0.000031)),
     Location(x=1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=-52.795883, y=-209.999802, z=0.001732),
               Rotation(pitch=0.000027, yaw=-179.999954, roll=-0.000031)),
     Location(x=1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=-48.695994, y=-209.999802, z=0.001692),
               Rotation(pitch=0.000027, yaw=-179.999954, roll=-0.000031)),
     Location(x=1.000000, y=0.000000, z=0.000000)],

    [Transform(Location(x=-52.795883, y=-209.999802, z=0.001684),
               Rotation(pitch=0.000027, yaw=-179.999954, roll=-0.000031)),
     Location(x=1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=-54.795883, y=-209.999802, z=0.001692),
               Rotation(pitch=0.000027, yaw=-179.999954, roll=-0.000031)),
     Location(x=1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=-50.695994, y=-209.999802, z=0.001729),
               Rotation(pitch=0.000027, yaw=-179.999954, roll=-0.000031)),
     Location(x=1.000000, y=0.000000, z=0.000000)],

    [Transform(Location(x=-47.795883, y=-209.999802, z=0.001689),
               Rotation(pitch=0.000027, yaw=-179.999954, roll=-0.000031)),
     Location(x=1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=-52.795883, y=-209.999802, z=0.001684),
               Rotation(pitch=0.000027, yaw=-179.999954, roll=-0.000031)),
     Location(x=1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=-47.695994, y=-209.999802, z=0.001684),
               Rotation(pitch=0.000027, yaw=-179.999954, roll=-0.000031)),
     Location(x=1.000000, y=0.000000, z=0.000000)],

    [Transform(Location(x=-88.999977, y=-65.299576, z=-0.821567),
               Rotation(pitch=0.579623, yaw=90.000168, roll=0.001613)), Location(x=0.000000, y=-1.000000, z=0.000000)],
    [Transform(Location(x=-88.999977, y=-64.299164, z=-0.812455),
               Rotation(pitch=0.666367, yaw=90.000381, roll=0.001632)), Location(x=0.000000, y=-1.000000, z=0.000000)],
    [Transform(Location(x=-88.999977, y=-65.60053, z=-0.821090),
               Rotation(pitch=0.581379, yaw=90.000458, roll=0.001621)), Location(x=0.000000, y=-1.000000, z=0.000000)],

    [Transform(Location(x=-88.999977, y=-65.299820, z=-0.820881),
               Rotation(pitch=0.582287, yaw=90.000793, roll=0.001611)), Location(x=0.000000, y=-1.000000, z=0.000000)],
    [Transform(Location(x=-88.999977, y=-65.299904, z=-0.821259),
               Rotation(pitch=0.580689, yaw=90.000946, roll=0.001628)), Location(x=0.000000, y=-1.000000, z=0.000000)],
    [Transform(Location(x=-88.999977, y=-65.60053, z=-0.811815),
               Rotation(pitch=0.665404, yaw=90.001144, roll=0.001589)), Location(x=0.000000, y=-1.000000, z=0.000000)],

    [Transform(Location(x=-88.999969, y=-61.299446, z=-0.774041),
               Rotation(pitch=0.787425, yaw=90.001801, roll=0.002151)), Location(x=0.000000, y=-1.000000, z=0.000000)],
    [Transform(Location(x=-88.999969, y=-60.299374, z=-0.760374),
               Rotation(pitch=0.833966, yaw=90.001938, roll=0.002168)), Location(x=0.000000, y=-1.000000, z=0.000000)],
    [Transform(Location(x=-88.999977, y=-64.400267, z=-0.715861),
               Rotation(pitch=0.841356, yaw=89.999886, roll=0.002327)), Location(x=0.000000, y=-1.000000, z=0.000000)],

    [Transform(Location(x=-49.304108, y=134.999924, z=0.001689), Rotation(pitch=0.000020, yaw=0.000000, roll=0.000000)),
     Location(x=-1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=-48.304104, y=134.999924, z=0.001730), Rotation(pitch=0.000020, yaw=0.000000, roll=0.000000)),
     Location(x=-1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=-50.400993, y=134.999924, z=0.001685), Rotation(pitch=0.000020, yaw=0.000000, roll=0.000000)),
     Location(x=-1.000000, y=0.000000, z=0.000000)],

    [Transform(Location(x=-53.304104, y=134.999924, z=0.001688), Rotation(pitch=0.000020, yaw=0.000000, roll=0.000000)),
     Location(x=-1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=-51.304104, y=134.999924, z=0.001730), Rotation(pitch=0.000020, yaw=0.000000, roll=0.000000)),
     Location(x=-1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=-53.400993, y=134.999924, z=0.001685), Rotation(pitch=0.000020, yaw=0.000000, roll=0.000000)),
     Location(x=-1.000000, y=0.000000, z=0.000000)],

    [Transform(Location(x=-49.304104, y=134.999924, z=0.001689), Rotation(pitch=0.000020, yaw=0.000000, roll=0.000000)),
     Location(x=-1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=-46.304104, y=134.999924, z=0.001731), Rotation(pitch=0.000020, yaw=0.000000, roll=0.000000)),
     Location(x=-1.000000, y=0.000000, z=0.000000)],
    [Transform(Location(x=-49.400993, y=134.999924, z=0.001730), Rotation(pitch=0.000020, yaw=0.000000, roll=0.000000)),
     Location(x=-1.000000, y=0.000000, z=0.000000)],

]



"""



"""
# Old Stuff 1

car_pos_translate_t3 = [
    carla.Location(x=1, y=0, z=0),
    carla.Location(x=0, y=1, z=0),
    carla.Location(x=0, y=1, z=0),
    carla.Location(x=1, y=0, z=0),
    carla.Location(x=1, y=0, z=0),
    carla.Location(x=0, y=-1, z=0),
    carla.Location(x=-1, y=0, z=0),
]

car_pos_t3 = [
    Transform(Location(x=40.600000, y=-4.000000, z=0.000000),
              Rotation(pitch=-0.500004, yaw=-179.999969, roll=0.000000)),
    Transform(Location(x=246.000000, y=-1.400000, z=0.000000), Rotation(pitch=2.499999, yaw=-89.499992, roll=0.000000)),
    Transform(Location(x=247.000000, y=-30.400000, z=0.000000),
              Rotation(pitch=2.499999, yaw=-90.000000, roll=-0.000000)),
    Transform(Location(x=34.600000, y=193.000000, z=0.000000),
              Rotation(pitch=0.000000, yaw=-179.999969, roll=0.000000)),
    Transform(Location(x=-50.400000, y=-210.000000, z=0.000000),
              Rotation(pitch=0.000000, yaw=-179.999969, roll=0.000000)),
    Transform(Location(x=-89.000000, y=-65.700000, z=-0.424789),
              Rotation(pitch=0.000000, yaw=89.999985, roll=0.000000)),
    Transform(Location(x=-48.700000, y=135.000000, z=0.000000), Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000)),
]

car_pos_translate_t1 = [
    carla.Location(x=1, y=0, z=0),
    carla.Location(x=0, y=-1, z=0),
    carla.Location(x=1, y=0, z=0),
    carla.Location(x=1, y=0, z=0),
    carla.Location(x=1, y=0, z=0),
]

car_pos_t1 = [
    Transform(Location(x=169.600000, y=-2.000000, z=0.000000), Rotation(pitch=0.000000, yaw=179.999969, roll=0.000000)),
    Transform(Location(x=-2.000000, y=176.400000, z=0.000000), Rotation(pitch=0.000000, yaw=89.999985, roll=0.000000)),

    Transform(Location(x=159.600000, y=326.000000, z=0.000000),
              Rotation(pitch=0.000000, yaw=179.999969, roll=0.000000)),
    Transform(Location(x=208.600000, y=55.000000, z=0.000000),
              Rotation(pitch=0.000000, yaw=-179.500000, roll=0.000000)),

    Transform(Location(x=173.600000, y=195.000000, z=0.000000),
              Rotation(pitch=0.000000, yaw=-179.999969, roll=0.000000)),

]


# town 3
location_town03 = [
    carla.Transform(
        carla.Location(x=246.709337, y=-13.22, z=0.09),
        carla.Rotation(pitch=0.0, yaw=-90.0, roll=0.000000)),

    carla.Transform(
        carla.Location(x=8.2, y=219.09, z=0.22),
        carla.Rotation(pitch=0.0, yaw=-90.0, roll=0.000000)),

    carla.Transform(
        carla.Location(x=-26.709337, y=172.161652, z=0.2),
        carla.Rotation(pitch=0.0, yaw=-25.0, roll=0.000000)),

    carla.Transform(
        carla.Location(x=185.98, y=-65.49, z=8.192),
        carla.Rotation(pitch=0.0, yaw=-68.0, roll=0.000000)),
]

location_town01 = [
    Transform(Location(x=186.343826, y=-1.001397, z=0.14), Rotation(pitch=-0.001250, yaw=0.0, roll=-0.000183)),

    Transform(Location(x=163.081940, y=38.575542, z=0.161928),
              Rotation(pitch=-0.108491, yaw=-0.000763, roll=-0.085236)),

    Transform(Location(x=26.201277, y=194.398102, z=0.21609), Rotation(pitch=0.003401, yaw=0.004866, roll=-0.009521)),

    Transform(Location(x=94.448357, y=132.836105, z=0.151600), Rotation(pitch=0.000915, yaw=0.000066, roll=-0.002441))
]

cam_t03_pos_1 = [
    Transform(Location(x=224.00, y=-13.22, z=12.0), Rotation(pitch=-25.0, yaw=0.0, roll=0.0)),
    Transform(Location(x=224.00, y=-13.22, z=6.00), Rotation(pitch=-7.5, yaw=0.0, roll=0.00)),
    Transform(Location(x=267.7, y=5.22, z=10.0), Rotation(pitch=-14.498592, yaw=-136.499252, roll=0.0)),
    Transform(Location(x=261.7, y=-2.22, z=5.0), Rotation(pitch=-19.498598, yaw=-142.496902, roll=0.0)),
    Transform(Location(x=248.7, y=-1.22, z=8.0), Rotation(pitch=-34.497517, yaw=-98.492928, roll=0.0)),
    Transform(Location(x=247.7, y=-2.22, z=3.0), Rotation(pitch=-12.997467, yaw=-100.494087, roll=0.0)),
    Transform(Location(x=235.7, y=-2.22, z=11.0), Rotation(pitch=-27.997374, yaw=-38.491737, roll=0.0)),
    Transform(Location(x=237.7, y=-7.22, z=3.0), Rotation(pitch=-10.997341, yaw=-32.496475, roll=0.0)),
    Transform(Location(x=238.7, y=-27.22, z=5.0), Rotation(pitch=-14.997244, yaw=59.998127, roll=0.0)),
    Transform(Location(x=240.7, y=-24.22, z=14.0), Rotation(pitch=-46.495968, yaw=62.497292, roll=0.0)),
    Transform(Location(x=247.7, y=-25.22, z=5.0), Rotation(pitch=-22.995510, yaw=97.998375, roll=0.0)),
    Transform(Location(x=245.7, y=-24.22, z=13.0), Rotation(pitch=-49.994198, yaw=87.498192, roll=0.0)),
    Transform(Location(x=252.7, y=-15.22, z=12.0), Rotation(pitch=-60.988232, yaw=163.494675, roll=0.0)),
    Transform(Location(x=258.7, y=-11.22, z=6.0), Rotation(pitch=-22.985777, yaw=-170.500793, roll=0.0)),
]

cam_t03_pos_2 = [
    Transform(Location(x=-6.719989, y=220.089996, z=11.000000),
              Rotation(pitch=-33.000061, yaw=-0.999176, roll=0.000000)),
    Transform(Location(x=-3.719988, y=220.089996, z=5.000000),
              Rotation(pitch=-18.999783, yaw=-3.999849, roll=0.000002)),
    Transform(Location(x=1.280011, y=228.089996, z=5.000000),
              Rotation(pitch=-20.499630, yaw=-51.004013, roll=0.000010)),
    Transform(Location(x=-2.719989, y=229.089996, z=3.000000),
              Rotation(pitch=-4.999630, yaw=-40.504910, roll=0.000028)),
    Transform(Location(x=4.280010, y=230.089996, z=10.000000),
              Rotation(pitch=-36.999435, yaw=-67.005013, roll=0.000041)),
    Transform(Location(x=4.280008, y=230.089996, z=3.000000), Rotation(pitch=-5.499299, yaw=-69.006653, roll=0.000061)),
    Transform(Location(x=19.280005, y=225.089996, z=10.000000),
              Rotation(pitch=-37.998466, yaw=-149.502441, roll=0.000124)),
    Transform(Location(x=21.280005, y=221.089996, z=5.000000),
              Rotation(pitch=-12.997890, yaw=-169.993607, roll=0.000140)),
    Transform(Location(x=15.280005, y=211.089996, z=12.000000),
              Rotation(pitch=-46.496037, yaw=135.002609, roll=0.000159)),
    Transform(Location(x=20.280005, y=202.089996, z=5.000000),
              Rotation(pitch=-8.995721, yaw=126.501534, roll=0.000144)),
    Transform(Location(x=0.280003, y=208.089996, z=9.000000), Rotation(pitch=-32.495483, yaw=54.000191, roll=0.000142)),
    Transform(Location(x=0.280003, y=207.089996, z=5.000000), Rotation(pitch=-13.995481, yaw=56.998905, roll=0.000153)),
]

cam_t03_pos_3 = [
    Transform(Location(x=-9.929995, y=161.239990, z=11.129997),
              Rotation(pitch=-23.999630, yaw=145.002319, roll=0.000045)),
    Transform(Location(x=-11.929968, y=162.239990, z=6.129997),
              Rotation(pitch=-13.999695, yaw=147.496933, roll=0.000001)),
    Transform(Location(x=-16.929966, y=173.239990, z=6.129997),
              Rotation(pitch=-27.499386, yaw=-170.496231, roll=0.000002)),
    Transform(Location(x=-13.929964, y=173.239990, z=3.129997),
              Rotation(pitch=-6.499389, yaw=-172.495453, roll=0.000005)),
    Transform(Location(x=-37.929958, y=174.239990, z=6.129998),
              Rotation(pitch=-23.999289, yaw=-6.991491, roll=0.000001)),
    Transform(Location(x=-34.929955, y=172.239990, z=4.129998),
              Rotation(pitch=-21.999083, yaw=3.008541, roll=0.000001)),
    Transform(Location(x=-20.929943, y=184.239990, z=10.129997),
              Rotation(pitch=-35.496910, yaw=-115.988083, roll=0.000021)),
    Transform(Location(x=-15.929942, y=171.239990, z=5.129997),
              Rotation(pitch=-23.990656, yaw=177.517990, roll=0.000118)),

]

cam_t03_pos_4 = [
    Transform(Location(x=164.959991, y=-64.439995, z=21.439997),
              Rotation(pitch=-33.499687, yaw=0.000000, roll=0.000000)),
    Transform(Location(x=164.959991, y=-68.439995, z=12.439996),
              Rotation(pitch=-9.499632, yaw=9.000124, roll=0.000000)),
    Transform(Location(x=180.959991, y=-82.439987, z=14.439996),
              Rotation(pitch=-15.999697, yaw=74.996643, roll=0.000002)),
    Transform(Location(x=179.959991, y=-78.439987, z=25.439995),
              Rotation(pitch=-49.497772, yaw=66.994850, roll=0.000016)),
    Transform(Location(x=196.959991, y=-74.439987, z=17.439995),
              Rotation(pitch=-32.492664, yaw=143.490952, roll=0.000034)),
    Transform(Location(x=207.959991, y=-62.439983, z=12.439995),
              Rotation(pitch=-10.492283, yaw=-170.507446, roll=0.000065)),
    Transform(Location(x=207.959991, y=-61.439983, z=21.439995),
              Rotation(pitch=-29.992035, yaw=-168.505432, roll=0.000074)),
    Transform(Location(x=180.959991, y=-79.439980, z=23.439995),
              Rotation(pitch=-42.990925, yaw=70.494133, roll=0.000105)),
    Transform(Location(x=178.959991, y=-42.439980, z=12.439995),
              Rotation(pitch=-7.490299, yaw=-74.504707, roll=0.000156)),
    Transform(Location(x=175.959991, y=-57.439980, z=12.439995),
              Rotation(pitch=-15.989588, yaw=-37.003525, roll=0.000124)),
]


all_cam_lists_t03 =[
cam_t03_pos_1,
cam_t03_pos_2,
cam_t03_pos_3,
cam_t03_pos_4,
]

cam_t01_pos_1 = [
    Transform(Location(x=171.343826, y=-1.001397, z=6.099999),
              Rotation(pitch=-21.501249, yaw=0.499111, roll=-0.000183)),
    Transform(Location(x=169.343826, y=-1.001397, z=3.099999), Rotation(pitch=-9.001158, yaw=0.999112, roll=-0.000183)),
    Transform(Location(x=172.343826, y=-1.001397, z=14.099998),
              Rotation(pitch=-44.998165, yaw=0.999058, roll=-0.000183)),
    Transform(Location(x=178.343826, y=-14.001397, z=13.099998),
              Rotation(pitch=-38.997128, yaw=61.498856, roll=-0.000185)),
    Transform(Location(x=179.343826, y=-14.001396, z=22.099997),
              Rotation(pitch=-53.995632, yaw=64.499809, roll=-0.000183)),
    Transform(Location(x=190.343826, y=-17.001396, z=14.099995),
              Rotation(pitch=-38.994259, yaw=105.998909, roll=-0.000180)),
    Transform(Location(x=201.343826, y=-16.001396, z=12.099994),
              Rotation(pitch=-26.994047, yaw=133.999680, roll=-0.000182)),
    Transform(Location(x=203.343826, y=-14.001396, z=25.099995),
              Rotation(pitch=-47.492825, yaw=141.999130, roll=-0.000184)),
    Transform(Location(x=200.343826, y=-2.001396, z=11.099995),
              Rotation(pitch=-37.491512, yaw=177.998016, roll=-0.000183)),
    Transform(Location(x=204.343826, y=8.998603, z=15.099995),
              Rotation(pitch=-34.990997, yaw=-148.500122, roll=-0.000183)),
    Transform(Location(x=192.343826, y=13.998602, z=9.099995),
              Rotation(pitch=-26.490471, yaw=-109.996674, roll=-0.000184)),
    Transform(Location(x=189.343826, y=20.998600, z=5.099994),
              Rotation(pitch=-11.490290, yaw=-95.496094, roll=-0.000183)),
    Transform(Location(x=187.343826, y=21.998600, z=14.099994),
              Rotation(pitch=-29.490078, yaw=-91.496086, roll=-0.000182)),
    Transform(Location(x=171.343826, y=15.998598, z=12.099995),
              Rotation(pitch=-26.489958, yaw=-45.493824, roll=-0.000184)),
    Transform(Location(x=169.343826, y=10.998589, z=9.099977),
              Rotation(pitch=-20.987455, yaw=-34.493633, roll=-0.000213)),
    Transform(Location(x=167.343826, y=10.998589, z=15.099977),
              Rotation(pitch=-35.487030, yaw=-31.995962, roll=-0.000213)),

]

cam_t01_pos_2 = [
    Transform(Location(x=144.081940, y=37.575542, z=5.161927),
              Rotation(pitch=-11.608274, yaw=3.999275, roll=-0.085236)),
    Transform(Location(x=144.081940, y=37.575542, z=13.161927),
              Rotation(pitch=-33.107784, yaw=5.499726, roll=-0.085235)),
    Transform(Location(x=141.081940, y=24.575539, z=13.161927),
              Rotation(pitch=-27.107721, yaw=33.499535, roll=-0.085236)),
    Transform(Location(x=144.081940, y=26.575539, z=5.161927),
              Rotation(pitch=-13.107392, yaw=34.001003, roll=-0.085236)),
    Transform(Location(x=151.081940, y=21.575531, z=6.161927),
              Rotation(pitch=-15.606995, yaw=55.493431, roll=-0.085236)),
    Transform(Location(x=153.081940, y=18.575531, z=3.161927),
              Rotation(pitch=-3.106992, yaw=64.493904, roll=-0.085235)),
    Transform(Location(x=164.081924, y=15.575531, z=13.161927),
              Rotation(pitch=-28.606627, yaw=94.491936, roll=-0.085237)),
    Transform(Location(x=172.081924, y=50.575531, z=9.161926),
              Rotation(pitch=-29.603146, yaw=-124.509560, roll=-0.085236)),
    Transform(Location(x=162.081924, y=60.575531, z=13.161926),
              Rotation(pitch=-29.102875, yaw=-85.506371, roll=-0.085238)),
    Transform(Location(x=157.081924, y=61.575531, z=7.161926),
              Rotation(pitch=-17.102287, yaw=-74.001778, roll=-0.085235)),
    Transform(Location(x=144.081924, y=62.575531, z=3.161926),
              Rotation(pitch=-7.102235, yaw=-50.000526, roll=-0.085235)),
    Transform(Location(x=142.081924, y=52.575531, z=12.161926),
              Rotation(pitch=-24.602053, yaw=-33.502857, roll=-0.085235)),
    Transform(Location(x=135.081924, y=48.575531, z=8.161926),
              Rotation(pitch=-14.601954, yaw=-19.502106, roll=-0.085236)),
    Transform(Location(x=141.081924, y=46.575531, z=14.161926),
              Rotation(pitch=-31.601555, yaw=-21.498489, roll=-0.085236)),
]

cam_t01_pos_3 = [
    Transform(Location(x=4.201279, y=195.398102, z=13.376090),
              Rotation(pitch=-29.496580, yaw=1.004852, roll=-0.009521)),
    Transform(Location(x=7.201277, y=195.398102, z=4.216090),
              Rotation(pitch=-10.996611, yaw=-0.495148, roll=-0.009521)),
    Transform(Location(x=5.201277, y=191.398102, z=3.216090), Rotation(pitch=-6.996456, yaw=10.005931, roll=-0.009522)),
    Transform(Location(x=7.201277, y=189.398102, z=9.216089),
              Rotation(pitch=-24.496328, yaw=17.008812, roll=-0.009521)),
    Transform(Location(x=12.201277, y=183.398102, z=9.216089),
              Rotation(pitch=-25.996176, yaw=40.008354, roll=-0.009523)),
    Transform(Location(x=17.201277, y=177.398102, z=12.216088),
              Rotation(pitch=-31.996094, yaw=64.510300, roll=-0.009523)),
    Transform(Location(x=26.201277, y=173.398102, z=21.216085),
              Rotation(pitch=-44.995594, yaw=92.010979, roll=-0.009519)),
    Transform(Location(x=36.201279, y=177.398102, z=16.216085),
              Rotation(pitch=-39.494595, yaw=122.511566, roll=-0.009521)),
    Transform(Location(x=44.201279, y=181.398102, z=9.216084),
              Rotation(pitch=-20.993589, yaw=145.011551, roll=-0.009522)),
    Transform(Location(x=47.201279, y=190.398102, z=5.216083),
              Rotation(pitch=-12.493433, yaw=169.007767, roll=-0.009521)),
    Transform(Location(x=44.201279, y=209.398102, z=4.216083),
              Rotation(pitch=-10.493444, yaw=-137.990402, roll=-0.009522)),
    Transform(Location(x=41.201279, y=208.398102, z=10.216083),
              Rotation(pitch=-25.493406, yaw=-134.989410, roll=-0.009521)),
    Transform(Location(x=28.201279, y=211.398102, z=17.216084),
              Rotation(pitch=-44.492973, yaw=-94.489006, roll=-0.009525)),
    Transform(Location(x=17.201279, y=207.398102, z=14.216084),
              Rotation(pitch=-36.491940, yaw=-55.488178, roll=-0.009522)),
]

cam_t01_pos_4 = [
    Transform(Location(x=67.448349, y=128.836105, z=13.111599),
              Rotation(pitch=-22.499229, yaw=15.001975, roll=-0.002441)),
    Transform(Location(x=64.448349, y=125.836090, z=18.111599),
              Rotation(pitch=-33.499104, yaw=17.503424, roll=-0.002441)),
    Transform(Location(x=65.448349, y=117.836090, z=20.111599),
              Rotation(pitch=-33.498810, yaw=30.004105, roll=-0.002441)),
    Transform(Location(x=76.448349, y=106.836090, z=4.111599),
              Rotation(pitch=-12.998778, yaw=54.503311, roll=-0.002441)),
    Transform(Location(x=77.448349, y=98.836090, z=4.111599), Rotation(pitch=-7.498803, yaw=65.001114, roll=-0.002441)),
    Transform(Location(x=85.448349, y=101.836090, z=12.111599),
              Rotation(pitch=-21.498867, yaw=74.496422, roll=-0.002441)),
    Transform(Location(x=94.448349, y=100.836090, z=3.111599),
              Rotation(pitch=-6.998833, yaw=91.992996, roll=-0.002441)),
    Transform(Location(x=100.448349, y=99.836090, z=5.111599),
              Rotation(pitch=-8.498838, yaw=100.993576, roll=-0.002442)),
    Transform(Location(x=102.448349, y=106.836090, z=17.111599),
              Rotation(pitch=-31.998711, yaw=106.495712, roll=-0.002442)),
    Transform(Location(x=116.448349, y=115.836090, z=6.111599),
              Rotation(pitch=-11.498439, yaw=142.993530, roll=-0.002441)),
    Transform(Location(x=125.448349, y=125.836090, z=5.111599),
              Rotation(pitch=-9.998413, yaw=163.491013, roll=-0.002441)),
    Transform(Location(x=124.448349, y=133.836090, z=16.111599),
              Rotation(pitch=-29.998156, yaw=179.990021, roll=-0.002441)),
    Transform(Location(x=116.448349, y=146.836090, z=13.111599),
              Rotation(pitch=-28.497364, yaw=-147.008560, roll=-0.002440)),
    Transform(Location(x=72.448349, y=146.836090, z=11.111599),
              Rotation(pitch=-26.496769, yaw=-33.500816, roll=-0.002441)),

]

all_cam_lists_t01 =[
cam_t01_pos_1,
cam_t01_pos_2,
cam_t01_pos_3,
cam_t01_pos_4,
]


"""








