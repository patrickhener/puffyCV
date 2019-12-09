import cv2


def test_for_cams():
    result = {}
    cam_test = 10
    for i in range(0, cam_test):
        cap = cv2.VideoCapture(i)
        test, frame = cap.read()
        result[str(i)] = test

    return result
