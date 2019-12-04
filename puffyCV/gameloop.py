import time
import asyncio
import cv2

from services.detector_service import has_new_images
from services.processor_service import erode, segment, find_darts_axis
from services.data_service import ProcessedImage
from services.display_service import display_with_information


def process_input(processed_image):
    processed_image.image = erode(processed_image)
    processed_image.set_bounding_box(segment(processed_image))
    processed_image.set_darts_axis(find_darts_axis(processed_image))
    display_with_information(processed_image)


class GameLoop:
    """
    GameLoop controls the application flow. It provides the clock speed of the application by setting a frame rate
    for the capturing devices. While running, the game loop queries the devices in the resulting time periods and
    delegates the results from the capturing devices to the processing functions.
    """

    def __init__(self, devices):
        """
        :param devices: capturing devices (e.g. web cams) for capturing visual input
        :type devices: list of CapturingDevice
        """
        self.devices = devices
        self.capturing = True

    def run(self):
        """
        runs the game loop as asynchronous task
        """
        asyncio.run(self.async_run())

    async def async_run(self):
        """
        asynchronous task
        """

        while self.capturing:
            self.process()

        # When everything done, release the capture devices
        for captured_input in self.devices:
            captured_input.release()

        cv2.destroyAllWindows()

    def process(self):
        for device in self.devices:
            device.process_image()

        if has_new_images(self.devices):
            for device in self.devices:
                latest_frame = device.fetch_latest_frame()
                if not latest_frame.all():
                    # set image and image metadata
                    processed_image = ProcessedImage(latest_frame,
                                                     device.resolution_width,
                                                     device.resolution_height,
                                                     device.device_id)
                    # set the dart board level obtained from the device
                    processed_image.set_darts_board_offset(device.surface_y)
                    # do image processing
                    process_input(processed_image)
