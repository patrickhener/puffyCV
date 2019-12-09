import numpy as np

from services.logging_service import initialize_logging
from services.measuring_service import find_lines_intersection, find_angle, find_distance
from services.draw_service import projection_center_point, projection_coefficient

log = initialize_logging()

pi = np.pi


class ThrowService(object):
    """

    """
    def __init__(self):
        self.rays = []

    def calculate_poi(self):
        if len(self.rays) < 2:
            log.debug("Rays count < 2. Not calculating")

        # TODO find a way to determine best rays or process all rays provided
        first_best_ray = self.rays[0]
        second_best_ray = self.rays[1]

        poi = find_lines_intersection(first_best_ray.cam_setup_point, first_best_ray.ray_point,
                                          second_best_ray.cam_setup_point, second_best_ray.ray_point)
        return poi

    def calculate_value(self, poi):
        sectors = [
            14, 9, 12, 5, 20,
            1, 18, 4, 13, 6,
            10, 15, 2, 17, 3,
            19, 7, 16, 8, 11
        ]

        angle = find_angle(projection_center_point, poi)
        distance = find_distance(projection_center_point, poi)
        sector = 0
        multiplier = "single"

        # find multiplier
        if projection_coefficient * 95 <= distance <= projection_coefficient * 105:
            multiplier = "triple"
        elif projection_coefficient * 160 <= distance <= projection_coefficient * 170:
            multiplier = "double"

        # find sector
        if distance <= projection_coefficient * 7:
            sector = 50
            multiplier = "bull"
        elif projection_coefficient * 7 < distance <= projection_coefficient * 17:
            sector = 25
            multiplier = "singlebull"
        elif distance > projection_coefficient * 170:
            sector = 0
            multiplier = "zero"
        else:
            start_rad_sector = -2.9845105
            rad_sector_step = pi / 10
            rad_sector = start_rad_sector
            for proceed_sector in sectors:
                if rad_sector <= angle < rad_sector + rad_sector_step:
                    sector = proceed_sector

                rad_sector += rad_sector_step

        return sector, multiplier

    def clear_rays(self):
        self.rays = []

    def save_ray(self, ray):
        self.rays.append(ray)
