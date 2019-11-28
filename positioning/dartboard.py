import math

"""
This class represents a dart board with scores and the arrangement of the fields. A dart board is represented by a list
of board fields. A regular dart board consists of 20 fields. Each board field has a score and an angle. The angle runs 
through the center axis of the board field. 
The angle is measured clockwise. 0 degrees is the axis of the 6-points field, so it is on the horizontal axis to the 
right.



-1,-1 ---------------- X ---------------> 1,-1
      
 |                    20
 |                %%%    %%%
 |           %%%              %%%
   
 Y       %%%                      %%%
   
 |      %%%                         %%%
 |  11                o------ 0° ----  6
 |      %%%           |  |          %%%
 |                    |_/
 |      %%%           |            %%%
 |                    |
 |         %%%       90 °       %%%
 |                    |
\|/              %%%     %%%
 v                    3
 
-1, 1                                     1, 1

"""


class Board(object):

    def __init__(self):
        self.fields = [
            BoardField(score=20, angle=270),
            BoardField(score=1, angle=288),
            BoardField(score=18, angle=306),
            BoardField(score=4, angle=324),
            BoardField(score=13, angle=342),
            BoardField(score=6, angle=0),
            BoardField(score=10, angle=18),
            BoardField(score=15, angle=36),
            BoardField(score=2, angle=54),
            BoardField(score=17, angle=72),
            BoardField(score=3, angle=90),
            BoardField(score=19, angle=108),
            BoardField(score=7, angle=126),
            BoardField(score=16, angle=144),
            BoardField(score=8, angle=162),
            BoardField(score=11, angle=180),
            BoardField(score=14, angle=198),
            BoardField(score=9, angle=216),
            BoardField(score=12, angle=234),
            BoardField(score=5, angle=252)
        ]

    def print(self):
        print("-----------")
        for f in self.fields:
            print("Segment: {}".format(f.score))

            x_left, y_left = f.get_coordinates_top_left()
            x_right, y_right = f.get_coordinates_top_right()
            x_center, y_center = f.get_coordinates_top_center()

            print("Left Angle: " + str(f.left_angle()))
            print("Center Angle: " + str(f.center_angle()))
            print("Right Angle: " + str(f.right_angle()))
            print("Coordinates Top Left")
            print("X: " + str(x_left))
            print("Y: " + str(y_left))
            print("Coordinates Top Center")
            print("X: " + str(x_center))
            print("Y: " + str(y_center))
            print("Coordinates Top Right")
            print("X: " + str(x_right))
            print("Y: " + str(y_right))
            print("-----------")


class BoardField(object):
    def __init__(self, score, angle):
        self.score = score
        self.angle = angle

    def left_angle(self):
        result = self.angle - 9
        if result < 0:
            result += 360
        return result

    def center_angle(self):
        return self.angle

    def right_angle(self):
        result = self.angle + 9
        if result > 360:
            result -= 360
        return result

    def get_coordinates_top_left(self):
        angle = self.left_angle()
        return round(math.cos(math.radians(angle)), 4), round(math.sin(math.radians(angle)), 4)

    def get_coordinates_top_center(self):
        angle = self.center_angle()
        return round(math.cos(math.radians(angle)), 4), round(math.sin(math.radians(angle)), 4)

    def get_coordinates_top_right(self):
        angle = self.right_angle()
        return round(math.cos(math.radians(angle)), 4), round(math.sin(math.radians(angle)), 4)
