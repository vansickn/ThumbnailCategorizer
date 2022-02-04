import cv2
import os
import requests
import ast
import apikey
import helper_functions


class ReadEmotion:

    def __init__(self, youtube_search_string) -> None:
        # initial variables
        self.youtube_search_string = youtube_search_string
        self.API_KEY = apikey.API_KEY
        self.request_link = f"https://api.haystack.ai/api/image/analyze?output=json&apikey={self.API_KEY}"

        # call API, creates a log of the result in the folder for each respective thumbnail
        self.call_api()

        # runs through each folder, takes the API result data and creates a separate image with the bounding boxes applied
        self.create_bounding_boxes()

        # writes the faceism ratio of the image if there is only one person in the image
        self.determine_faceism_ratio()

    def call_api(self):
        # each folder (youtube video) -> gets the LQ picture, and then runs it to the API, then creates a file which is the json output from the API
        for folder in helper_functions.listdir_nohidden(self.youtube_search_string):
            picture_data = open(self.youtube_search_string +
                                '/' + folder + '/LQ.png', "rb")
            r = requests.post(self.request_link, data=picture_data)
            print(r.text)
            f = open(self.youtube_search_string +
                     '/' + folder + "/img_analyzer_data.txt", "w")
            f.write(r.text)
            f.close()

    def determine_faceism_ratio(self):
        for folder in helper_functions.listdir_nohidden(self.youtube_search_string):
            #    Make analyzer data readable, cause the json they give back is not fun, basically just turns it into an object. Could probably make this a helper function
            analyzer_data = open(self.youtube_search_string +
                                 '/' + folder + "/img_analyzer_data.txt", "r").read()
            analyzer_data = analyzer_data.replace(
                'false', "False").replace('true', 'True')
            analyzer_data = ast.literal_eval(analyzer_data)

            if len(analyzer_data['people']) != 1:
                print("More or less than 1 person in thumbnail")
            else:
                # takes the height of the face and divides it by the number of y pixels, gives rough estimate of the faceism ratio
                faceism_ratio = (
                    analyzer_data['people'][0]['location']['height'])/202
                f = open(self.youtube_search_string +
                         '/' + folder + "/faceismRatio.txt", "w")
                f.write(str(faceism_ratio))
                f.close()

    def create_bounding_boxes(self):
        for folder in helper_functions.listdir_nohidden(self.youtube_search_string):
            img = cv2.imread(self.youtube_search_string +
                             '/' + folder + '/LQ.png')
            analyzer_data = open(self.youtube_search_string +
                                 '/' + folder + "/img_analyzer_data.txt", "r").read()
            analyzer_data = analyzer_data.replace(
                'false', "False").replace('true', 'True')
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
            cv2.putText(img, str(i), tp, font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imwrite(self.youtube_search_string + '/' +
                    folder + '/with_bounding_boxes.png', img)

        # sample result
        # result = str({"result": "success", "adultContent": {"isAdultContent": 'false', "isAdultContentConfidence": 0.0411, "adultContentType": "", "adultContentTypeConfidence": 0}, "people": [{"index": 0, "gender": {"gender": "male", "confidence": 0.9969}, "age": 25.3, "attractiveness": 6.2655, "location": {"x": 176, "y": 37, "width": 51, "height": 52}, "ethnicity": {"ethnicity": "White_Caucasian", "confidence": 0.88}, "emotion": {"emotions": {"happy": 0.922109663, "judging": 0.07239496}, "attributes": {
        # }}}], "containsNudity": 'false', "colors": [{"hex": "#B0B1AB", "percentage": 0.3335}, {"hex": "#10120D", "percentage": 0.0775}, {"hex": "#2E3226", "percentage": 0.1176}, {"hex": "#6F716D", "percentage": 0.0983}, {"hex": "#F8FBF8", "percentage": 0.0963}, {"hex": "#1A3859", "percentage": 0.0904}, {"hex": "#7AA6AA", "percentage": 0.0415}, {"hex": "#DFB2A1", "percentage": 0.0665}, {"hex": "#573A29", "percentage": 0.0282}, {"hex": "#3C6383", "percentage": 0.027}, {"hex": "#A26D5F", "percentage": 0.0231}]})
        # result = result.replace('false', "False").replace('true', 'True')
        # result = ast.literal_eval(result)
        # boundingBoxes = []
        # for p in result['people']:
        #     location_dict = {
        #         'x': p['location']['x'],
        #         'y': p['location']['y'],
        #         'width': p['location']['width'],
        #         'height': p['location']['height']
        #     }
        #     boundingBoxes.append(location_dict)
        # print(boundingBoxes)
