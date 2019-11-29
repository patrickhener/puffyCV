import pickle
import os


def get_config(device_id):
    filename = "device-" + str(device_id)
    infile = open('./pickles/' + filename, 'r')
    device = pickle.load(infile)
    infile.close()
    return device


def set_config(device_id, device_object):
    filename = "device-" + str(device_id)
    outfile = open('./pickles/' + filename, 'wb')
    pickle.dump(device_object, outfile)
    outfile.close()


def initialize_config(device_id):
    filename = "device-" + str(device_id)
    if not os.path.isfile('./pickles/' + filename):
        return False
    else:
        return True
