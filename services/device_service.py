import cv2
import numpy as np

from services.draw_service import draw_rectangle, draw_line

roi_rectangle_color = (0, 255, 0)  # green
roi_rectanlge_thickness = 3
surface_line_color = (0, 0, 255)  # red
surface_line_thickness = 3

# Threshold for the image difference of two frames. Value between 0 and 255. 0 means that there needs to be no
# difference between two successive frames (which is obviously a bad idea), 255 is the biggest possible difference.
IMAGE_DIFFERENCE_THRESHOLD = 20


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

    """

    def __init__(self, device_id, roi_pos_y, roi_height, surface_y, surface_center, threshold, fov, bull_distance,
                 position, resolution_width=1280, resolution_height=720):
        self.device_id = device_id
        self.resolution_width = resolution_width
        self.resolution_height = resolution_height
        self.roi_pos_y = roi_pos_y
        self.roi_height = roi_height
        self.surface_y = surface_y
        self.surface_center = surface_center
        self.threshold = threshold
        self.fov = fov
        self.bull_distance = bull_distance
        self.position = position
        self.capture_device = get_capture_device(device_id, resolution_width, resolution_height)
        self.previous_frame = []
        self.recorded_frame = []

    def release(self):
        self.capture_device.release()

    def has_new_frame(self):
        return self.recorded_frame != []

    def fetch_latest_frame(self):
        recent_frame = self.recorded_frame
        self.recorded_frame = []
        return recent_frame

    def process_image(self):
        _, frame = self.capture_device.read()
        diff = self.get_difference(frame)

        white_pixels = np.sum(diff > IMAGE_DIFFERENCE_THRESHOLD)

        sixty_percent_of_all_pixels = (self.resolution_width * self.resolution_height) * 0.6
        minimum_changed_pixels_threshold = (self.resolution_width * self.resolution_height) * 0.015

        if minimum_changed_pixels_threshold < white_pixels < sixty_percent_of_all_pixels:
            self.recorded_frame = diff

        self.previous_frame = frame

    def get_difference(self, frame):
        has_previous_frame = len(self.previous_frame) > 0
        if has_previous_frame:
            return cv2.subtract(self.previous_frame, frame)
        else:
            return frame

    def draw_setup_lines(self, roi_pos_y, roi_height, surface_y, surface_center):
        ret, origin_frame = self.capture_device.read()
        lined_frame = origin_frame

        # Draw ROI rectangle
        top_left = (0, roi_pos_y - roi_height)
        bottom_right = (self.resolution_width, roi_pos_y)
        lined_frame = draw_rectangle(lined_frame, top_left, bottom_right, roi_rectangle_color, roi_rectanlge_thickness)
        # Draw surface line
        line_x = (0, surface_y)
        line_y = (self.resolution_width, surface_y)
        lined_frame = draw_line(lined_frame, line_x, line_y, surface_line_color, surface_line_thickness)
        # Draw Bull orientation line
        center_line_1 = (surface_center, surface_y)
        center_line_2 = (center_line_1[0], surface_y - 50)
        lined_frame = draw_line(lined_frame, center_line_1, center_line_2, surface_line_color, surface_line_thickness)

        return lined_frame

    def show_threshold(self, threshold):
        ret, origin_frame = self.capture_device.read()
        _, binary = cv2.threshold(origin_frame, threshold, 255, cv2.THRESH_BINARY)

        return binary
