import cv2
import numpy as np

# Threshold for the image difference of two frames. Value between 0 and 255. 0 means that there needs to be no
# difference between two successive frames (which is obviously a bad idea), 255 is the biggest possible difference.
IMAGE_DIFFERENCE_THRESHOLD = 100


def get_capture_device(device_number, image_width, image_height):
    capture_device = cv2.VideoCapture(device_number)
    capture_device.set(cv2.CAP_PROP_FRAME_WIDTH, image_width)
    capture_device.set(cv2.CAP_PROP_FRAME_HEIGHT, image_height)
    return capture_device


class CapturingDevice(object):
    """
    Capturing device superclass represents devices which capture visual input. These will be cameras in most cases.
    """


class WebCamCapturingDevice(CapturingDevice):
    """
    WebcamCapturingDevice represents a device for capturing the darts visually (i.e. a web cam). It captures frames
    when the captured image changes. The latest captured image can be fetched from the device.
    """

    def __init__(self, device_number, dartboard_level, image_width=1280, image_height=720):
        """
        :param device_number: numeric identifier of the device
        :type device_number: int
        :param image_width: y-pixel count of the capturing device
        :type image_width: int
        :param image_height: x-pixel count of the capturing device
        :type image_height: int
        """
        self.image_width = image_width
        self.image_height = image_height
        self.device_number = device_number
        self.dartboard_level = dartboard_level
        self.capture_device = get_capture_device(device_number, image_width, image_height)
        self.previous_frame = []
        self.recorded_frame = []

    def release(self):
        self.capture_device.release()

    def has_new_frame(self):
        return self.recorded_frame != []

    def fetch_latest_frame(self):
        """
        Gets the latest frame that was captured.
        :return: returns the latest captured frame from the device.
        :rtype: UMat
        """
        recent_frame = self.recorded_frame
        self.recorded_frame = []
        return recent_frame

    def process_image(self):
        _, frame = self.capture_device.read()
        diff = self.get_difference(frame)

        white_pixels = np.sum(diff > IMAGE_DIFFERENCE_THRESHOLD)

        sixty_percent_of_all_pixels = (self.image_width * self.image_height) * 0.6
        minimum_changed_pixels_threshold = (self.image_width * self.image_height) * 0.015

        if minimum_changed_pixels_threshold < white_pixels < sixty_percent_of_all_pixels:
            self.recorded_frame = diff

        self.previous_frame = frame

    def get_difference(self, frame):
        has_previous_frame = len(self.previous_frame) > 0
        if has_previous_frame:
            return cv2.subtract(self.previous_frame, frame)
        else:
            return frame

    def configure(self, initial_level=0):
        dartboard_level = int(self.image_height / 3) * 2
        if initial_level != 0:
            dartboard_level = initial_level

        while True:
            # Capture frame-by-frame
            ret, frame = self.capture_device.read()

            # Our operations on the frame come here
            image = cv2.cvtColor(frame, 0)

            image = cv2.line(image, (0, dartboard_level), (self.image_width, dartboard_level), (0, 255, 0), 1)

            # Display the resulting frame
            cv2.imshow('frame', image)
            c = cv2.waitKey(1)
            if 'q' == chr(c & 255):
                break
            elif 'j' == chr(c & 255):
                if dartboard_level < self.image_height - 1:
                    dartboard_level += 5
            elif 'k' == chr(c & 255):
                if dartboard_level > 0:
                    dartboard_level -= 5
        return dartboard_level
