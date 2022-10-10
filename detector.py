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


# experimentel modifiziertes detector skript

@smart_inference_mode()
def run(
    source,
    weights,
    data,
    conf_thres,
    iou_thres ,
    device,
):

    print(source)
    print(weights)
    print(data)
    print("--")
    print(conf_thres)
    print("--")
    print("dev "+device)


    """
    source = "0" # webcam
    weights = "best.pt"
    data = 'data/vehicle_data.yaml'  # wichtig: wegen den klassen
    conf_thres = 0.5
    iou_thres = 0.45
    device = "cpu"

    """
    augment = False

    classes = None  # filter by class: --class 0, or --class 0 2 3
    imgsz = (640, 640)
    max_det = 1000
    agnostic_nms = False
    half = False  # use FP16 half-precision inference
    dnn = False



    source = str(source)

    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
    is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
    webcam = source.isnumeric() or source.endswith('.txt') or (is_url and not is_file)

    # Load model
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Dataloader
    if webcam:
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt)
        bs = len(dataset)  # batch_size
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)
        bs = 1  # batch_size
    vid_path, vid_writer = [None] * bs, [None] * bs

    # Run inference
    model.warmup(imgsz=(1 if pt else bs, 3, *imgsz))  # warmup
    seen, windows, dt = 0, [], [0.0, 0.0, 0.0]
    for path, im, im0s, vid_cap, s in dataset:
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

        prediction_values = [ 0 for ele in names  ]
        # Process predictions

        for i, det in enumerate(pred):  # per image
            seen += 1
            if webcam:  # batch_size >= 1
                p, im0, frame = path[i], im0s[i].copy(), dataset.count
                s += f'{i}: '
            else:
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

            s += '%gx%g ' % im.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                    prediction_values[int(c)]+=int(n)  # my own: sum up predictions


        # Print time (inference-only)
        print("")
        print("")
        LOGGER.info(f'{s}Done. ({t3 - t2:.3f}s)')

        # do stuff:

        res = [ [names[int(val)] , int(val) ] for val in prediction_values if val!= 0 ]
        res_name = [names[int(val)] + " Erkennungen: " + str(val) for val in prediction_values if val != 0]
        print(res_name)

        maximum  = 0
        for val in res:
            if val[1] > maximum:
                maximum=val[1]

        print("Maximuma:")
        empty=True
        max_classes = []
        for val in res:
            if val[1] ==maximum:
                print(str(val[1])+" "+str(val[0])+" Erkennungen")
                max_classes.append(val[0])
                empty=False

        if empty:
            print("Zero")

        # send data somewhere with max_classes or pre filter earlier or take a random from it.

    print("exit")




def parse_opt():

    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', default= "best.pt", type=str, help='model path(s)')
    parser.add_argument('--source', type=str,  default= "0",help='file/dir/URL/glob, 0 for webcam')
    parser.add_argument('--data', type=str,  default= "data/vehicle_data.yaml",help='(optional) dataset.yaml path')
    parser.add_argument('--conf-thres', type=float, default=0.5, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float,  default= 0.45,help='NMS IoU threshold')
    parser.add_argument('--device', default='cpu', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')

    opt = parser.parse_args()
    print_args(vars(opt))
    return opt



if __name__ == "__main__":
    opt = parse_opt()
    run(**vars(opt))
