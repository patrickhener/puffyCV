import cv2
import sys

from puffyCV.args import args
from services.draw_service import draw_line, draw_rectangle, Board
from services.logging_service import initialize_logging

log = initialize_logging()

dart_axis_color = (0, 255, 0)
dart_axis_thickness = 3
pointer_color = (0, 0, 255)
needle_thickness = 1
pin_thickness = 10
bounding_box_color = (0, 255, 0)
bounding_box_thickness = 1
dartboard_level_color = (255, 0, 0)
dartboard_level_thickness = 5
roi_color = (0, 255, 255)
roi_thickness = 5
line_type = cv2.LINE_AA
text_type = cv2.FONT_HERSHEY_SIMPLEX
text_thickness = 1
text_color = (255, 255, 255)


def display_with_information(processed_image):
    """
    Displays a processed image with all additional information (like dartboard level, darts axis etc.) in a
    seperate window. Also displays Board for ray projection

    :param processed_image: The processed image which wraps the image itself and all additional information
    :type processed_image: ProcessedImage
    :return: None
    :rtype: None
    """
    if processed_image.image is not None:
        image_to_display = processed_image.image

        line = processed_image.darts_axis
        x = processed_image.bounding_box.x
        y = processed_image.bounding_box.y
        w = processed_image.bounding_box.w
        h = processed_image.bounding_box.h
        dartboard_level_x = (0, processed_image.darts_board_offset)
        dartboard_level_y = (processed_image.image_width, processed_image.darts_board_offset)
        roi_box_top_left = (0, processed_image.roi_offset + processed_image.roi_height)
        roi_box_bottom_right = (processed_image.image_width, processed_image.roi_offset)

        # draw darts axis
        if line is not None:
            # intersection dart with dart board
            x_value = int(x + processed_image.darts_axis[len(processed_image.darts_axis) - 1])

            image_to_display = draw_line(image_to_display, (int(x + line[0]), y), (x_value,
                                         processed_image.darts_board_offset), dart_axis_color, dart_axis_thickness)

            image_to_display = draw_line(image_to_display, (x_value, processed_image.darts_board_offset + 70),
                                         (x_value, processed_image.darts_board_offset - 20), pointer_color,
                                         needle_thickness)

            image_to_display = draw_line(image_to_display, (x_value, processed_image.darts_board_offset + 30),
                                         (x_value, processed_image.darts_board_offset + 70),pointer_color,
                                         pin_thickness)

            # If debug put some text to the image as well
            if args.DEBUG:
                intersection = "intersection at: {}".format(x_value)
                dart_board_center = "dartboard center at: {}".format(processed_image.darts_board_center)
                distance = processed_image.darts_board_center - x_value
                if distance < 0:
                    distance = distance * -1
                pixel_distance = "pixeldistance (intersection - center): {}".format(distance)
                cv2.putText(image_to_display, intersection, (50, 50), text_type, text_thickness, text_color,
                            lineType=line_type)
                cv2.putText(image_to_display, dart_board_center, (50, 80), text_type, text_thickness, text_color,
                            lineType=line_type)
                cv2.putText(image_to_display, pixel_distance, (50, 110), text_type, text_thickness, text_color,
                            lineType=line_type)

        # draw dart board level
        image_to_display = draw_line(image_to_display, dartboard_level_x, dartboard_level_y, dartboard_level_color,
                                     dartboard_level_thickness)

        # draw roi
        # TODO Does not yet work. Is off and I don't know why. Postponed as ROI is not used yet anyways
        # image_to_display = draw_rectangle(image_to_display, roi_box_top_left, roi_box_bottom_right, roi_color,
        #                                  roi_thickness)

        # draw bounding box
        image_to_display = draw_rectangle(image_to_display, (x, y), (x + w, y + h), bounding_box_color,
                                          bounding_box_thickness)

        # show images
        cv2.imshow('device_' + str(processed_image.device_number), image_to_display)
        c = cv2.waitKey(1)
        if 'q' == chr(c & 255):
            log.info("Caught pressing 'q', exiting ...")
            sys.exit()


def display_board(image):
    # show images
    cv2.imshow('projection', image)
    c = cv2.waitKey(1)
    if 'q' == chr(c & 255):
        log.info("Caught pressing 'q', exiting ...")
        sys.exit()
