import os
from measure_face import *
import helper_functions


class faceismCalculator:

    def __init__(self, youtube_search_string) -> None:
        self.youtube_search_string = youtube_search_string
        self.list_of_image_paths = []

        # generates list of image paths for the MeasureFace function
        self.generate_list_of_image_paths()

        MeasureFace(self.list_of_image_paths).measure_picture_list()

    def generate_list_of_image_paths(self):
        for folder in helper_functions.listdir_nohidden(self.youtube_search_string):
            self.list_of_image_paths.append(
                self.youtube_search_string + '/' + folder + '/LQ.png')

    # def listdir_nohidden(path):
    #     # Exclude all with . in the start
    #     return [i for i in os.listdir(path) if i[0] != "."]


# To configure, add a list of image paths into List_images, and the while loop and imgViewer will do the rest
# List_images = []
# for p in listdir_nohidden('../FaceismRatioCalculator'):
#     if os.path.isdir(p):
#         for folder in listdir_nohidden(p):
#             print(folder)
#             for file in listdir_nohidden('../FaceismRatioCalculator' + '/' + p + '/' + folder):
#                 print(file)
#                 if file == 'LQ.png':
#                     List_images.append(
#                         '../FaceismRatioCalculator' + '/' + p + '/' + folder + '/' + file)
