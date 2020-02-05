# System libs
import os
import argparse
from distutils.version import LooseVersion
# Numerical libs
import numpy as np
import torch
import torch.nn as nn
from torchvision import transforms
from scipy.io import loadmat
import csv
import cv2
# Our libs
from dataset import TestDataset
from models import ModelBuilder, SegmentationModule
from utils import colorEncode, find_recursive, setup_logger
from lib.nn import user_scattered_collate, async_copy_to
from lib.utils import as_numpy
from PIL import Image
from config import cfg
from lib.segmentation import hand_segmentation, module_init

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "240p": (352, 240),
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160)
}


def set_resolution(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

def main(cfg, gpu, visualise, resolution):
    torch.cuda.set_device(gpu)
    segmentation_module = module_init(cfg)

    print('Successfully initialised segmentation module')
    # Load color map
    colors = loadmat('data/matlab.mat')['colors']

    # Setup the webcam
    cap = cv2.VideoCapture(0)
    width, height = STD_DIMENSIONS[resolution]
    set_resolution(cap, width, height)
    print('Successfully set up camera')

    fps = 0

    while True:
        fps += 1
        ret, frame = cap.read() #Capture each frame
        # Convert to numpy.ndarray
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Hand segmentation API
        pred = hand_segmentation(frame, segmentation_module)

        # Visualisation
        if visualise:
            pred_color = colorEncode(pred, colors).astype(np.uint8)
            im_vis = np.concatenate((frame,pred_color), axis=1)
            im_vis = cv2.cvtColor(im_vis, cv2.COLOR_RGB2BGR)
            cv2.imshow("INFERENCE",im_vis)
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.imshow("INFERENCE", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyWindow("INFERENCE")


if __name__ == '__main__':
    assert LooseVersion(torch.__version__) >= LooseVersion('0.4.0'), \
        'PyTorch>=0.4.0 is required'

    parser = argparse.ArgumentParser(
        description="Hand Segmentation Inference"
    )

    parser.add_argument(
        "--cfg",
        default="config/ade20k-resnet50dilated-ppm_deepsup.yaml",
        metavar="FILE",
        help="path to config file",
        type=str,
    )

    parser.add_argument(
        "--resolution",
        default="480p",
        help="camera resolution",
        type=str,
    )

    parser.add_argument(
        "--gpu",
        default=0,
        type=int,
        help="gpu id for evaluation"
    )

    parser.add_argument('--visualise', action='store_true', help='Visualisation')
    parser.set_defaults(visualise=False)

    parser.add_argument(
        "opts",
        help="Modify config options using the command-line",
        default=None,
        nargs=argparse.REMAINDER,
    )
    args = parser.parse_args()

    cfg.merge_from_file(args.cfg)
    cfg.merge_from_list(args.opts)
    # cfg.freeze()

    logger = setup_logger(distributed_rank=0)   # TODO
    logger.info("Loaded configuration file {}".format(args.cfg))
    #logger.info("Running with config:\n{}".format(cfg))

    cfg.MODEL.arch_encoder = cfg.MODEL.arch_encoder.lower()
    cfg.MODEL.arch_decoder = cfg.MODEL.arch_decoder.lower()

    # absolute paths of model weights
    cfg.MODEL.weights_encoder = os.path.join(
        cfg.DIR, 'encoder_' + cfg.TEST.checkpoint)
    cfg.MODEL.weights_decoder = os.path.join(
        cfg.DIR, 'decoder_' + cfg.TEST.checkpoint)

    assert os.path.exists(cfg.MODEL.weights_encoder) and \
        os.path.exists(cfg.MODEL.weights_decoder), "checkpoint does not exitst!"

    if not os.path.isdir(cfg.TEST.result):
        os.makedirs(cfg.TEST.result)

    main(cfg, args.gpu, args.visualise, args.resolution)
