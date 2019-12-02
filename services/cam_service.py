import cv2
from services.draw_service import draw_rectangle, draw_line
from services.logging_service import initialize_logging

log = initialize_logging()


roi_rectangle_color = (0, 255, 0)  # green
roi_rectanlge_thickness = 3
surface_line_color = (0, 0, 255)  # red
surface_line_thickness = 3


class CamService(object):
    """

    """

    def __init__(self, device_id, roi_pos_y, roi_height, surface_y, surface_center,
                 resolution_width=1280, resolution_height=720):
        self.device_id = device_id
        self.resolution_width = resolution_width
        self.resolution_height = resolution_height
        self.roi_pos_y = roi_pos_y
        self.roi_height = roi_height
        self.surface_y = surface_y
        self.surface_center = surface_center

        self.video_capture = cv2.VideoCapture(self.device_id)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution_width)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution_height)

    def release(self):
        self.video_capture.release()

    def draw_setup_lines(self, roi_pos_y, roi_height, surface_y, surface_center):
        ret, origin_frame = self.video_capture.read()
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
