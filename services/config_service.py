import pickle
import os
import sys

from services.logging_service import initialize_logging

log = initialize_logging()

path = os.getcwd()
savepath = os.path.join(path + "/pickles/")


def get_config(device_id):
    if not initialize_config(device_id):
        log.error("Camera {} is not yet calibrated. Please do this first. Exiting ...".format(device_id))
        sys.exit()
    filename = "device-" + str(device_id)
    infile = os.path.join(savepath + filename)
    with open(infile, "rb") as pickle_file:
        cam = pickle.load(pickle_file)
    pickle_file.close()
    return cam


def set_config(device_id, roi_pos_y, roi_height, surface_y, surface_center):
    cam = {"device_id": device_id,
           "roi_pos_y": roi_pos_y,
           "roi_height": roi_height,
           "surface_y": surface_y,
           "surface_center": surface_center
           }
    filename = "device-" + str(device_id)
    outfile = open(os.path.join(savepath + filename), 'wb')
    pickle.dump(cam, outfile)
    outfile.close()


def initialize_config(device_id):
    filename = "device-" + str(device_id)
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    if not os.path.isfile(os.path.join(savepath + filename)):
        return False
    else:
        return True
