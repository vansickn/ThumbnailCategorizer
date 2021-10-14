from img_viewer import *
from tkinter import *
from PIL import ImageTk, Image
import os


class MeasureFace:

    def __init__(self, list_of_paths) -> None:
        self.list_of_paths = list_of_paths
        print(list_of_paths)

    def measure_picture_list(self):
        i = 0
        while i < len(self.list_of_paths):
            t = imgViewer(self.list_of_paths[i])
            t.createFrame()
            if t.face_exists():
                points = t.get_face_points()
                print(points)
                top_head = points[0]
                bottom_chin = points[1]
                bottom_torso = points[2]
                # [] is x value [1] is y value
                ratio = (bottom_chin[1] - top_head[1]) / \
                    (bottom_torso[1] - top_head[1])
                # for pictures that aren't in my use case, remove the file name and replace it with faceismRatio.txt
                f = open(str(self.list_of_paths[i]).replace(
                    "LQ.png", "") + 'faceismRatio.txt', "w")
                f.write(str(ratio))
                f.close()
            i += 1
        print("Completed!")
