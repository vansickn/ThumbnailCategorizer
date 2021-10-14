import ast
import os
import cv2


class tester:

    def __init__(self, youtube_search_string) -> None:
        self.youtube_search_string = youtube_search_string

        self.create_bounding_boxes()

    def create_bounding_boxes(self):
        for folder in os.listdir(self.youtube_search_string):
            img = cv2.imread(self.youtube_search_string +
                             '/' + folder + '/LQ.png')
            analyzer_data = open(self.youtube_search_string +
                                 '/' + folder + "/img_analyzer_data.txt", "r").read()
            analyzer_data = analyzer_data.replace(
                'false', "False").replace('true', 'True')
            print(analyzer_data)
            analyzer_data = ast.literal_eval(analyzer_data)
            bounding_boxes = []
            for p in analyzer_data['people']:
                location_dict = {
                    'x': p['location']['x'],
                    'y': p['location']['y'],
                    'width': p['location']['width'],
                    'height': p['location']['height']
                }
                bounding_boxes.append(location_dict)
            if len(bounding_boxes) != 0:
                self.draw_bounding_boxes(bounding_boxes, img, folder)

    def draw_bounding_boxes(self, bounding_boxes, img, folder):
        for i in range(len(bounding_boxes)):
            # top left corner
            tc = (bounding_boxes[i]['x'], bounding_boxes[i]['y'])
            # bottom right corner
            bc = (bounding_boxes[i]['x']+bounding_boxes[i]['width'],
                  bounding_boxes[i]['y']+bounding_boxes[i]['height'])
            # text position, 5px above bounding box
            tp = (bounding_boxes[i]['x'], bounding_boxes[i]['y']-5)
            font = cv2.FONT_HERSHEY_PLAIN
            cv2.rectangle(img, tc, bc, (0, 255, 0), 2)
            cv2.putText(img, str(i), tp, font, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.imwrite(self.youtube_search_string + '/' +
                    folder + '/with_bounding_boxes.png', img)


t = tester("how to write a resume")
