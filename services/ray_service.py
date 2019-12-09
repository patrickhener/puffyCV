class Ray(object):
    """
    Class will represent a ray for projection and calculation of throw destination
    """
    def __init__(self, device_id, cam_setup_point, ray_point):
        self.device_id = device_id
        self.cam_setup_point = cam_setup_point
        self.ray_point = ray_point
