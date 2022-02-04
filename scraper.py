from bs4 import BeautifulSoup
import requests
import json
import os
# from fer import FER
import cv2
from reportlab.pdfgen.canvas import Canvas
from tensorflow.python.framework.ops import to_raw_op
from yattag import Doc
import pdfkit
import re
import random


class Scraper:

    def __init__(self, youtube_search_string) -> None:
        self.youtube_search_string = youtube_search_string
        self.youtube_request_link = "https://www.youtube.com/results?search_query="

        # making search link
        self.search_request = self.buildLink()
        print(self.search_request)

        # make the request using beautiful soup
        self.make_soup_request()

        # create json from the correct script in the soup
        self.make_json_from_soup()

        # extract thumbnail URL and information, makes a self.thumbnail_information list in which we make the file with all of the thumbnails
        self.extract_thumbnails()

        # create folder of the titles and thumbnails within them
        self.create_file_of_thumbnails()

    def buildLink(self):
        return self.youtube_request_link + self.youtube_search_string.replace(" ", "+")

    def make_soup_request(self):
        self.soup = BeautifulSoup(requests.get(
            self.search_request, timeout=(100, 1000)).text, 'html.parser')

    def make_json_from_soup(self):
        scripts = self.soup.findAll("script")
        self.json_of_script = None
        for s in scripts:
            index = str(s).find("{\"")

            if index == 59:  # just by trial and error I know this to be the line which holds the data I need
                jsonString = (str(s)[index:]).replace(";</script>", "")
                self.json_of_script = json.loads(jsonString)
        # don't really need this return statement but I'm going to leave it
        return self.json_of_script

    def extract_thumbnails(self):
        j = self.json_of_script
        # print(j)
        jsonToVideoRenderers = self.__findVideoRenderer__(j["contents"]["twoColumnSearchResultsRenderer"][
            "primaryContents"]["sectionListRenderer"]["contents"])
        videoRendererList = []
        for i in range(len(jsonToVideoRenderers)):
            # print(str(jsonToVideoRenderers[i]) + '\n\n')
            # if jsonToVideoRenderers[i] == 'shelfRenderer':
            print(str(jsonToVideoRenderers[i])[:10])
            try:
                for j in jsonToVideoRenderers[i]['shelfRenderer']['content']['verticalListRenderer']['items']:
                    print("SHELF")
                    print(j)
                    videoRendererList.append(j)
            except:
                print("Error Occurred in Getting Shelf")
                videoRendererList.append(jsonToVideoRenderers[i])
        # print(videoRendererList)
        # print(videoRendererList)
        # Write function for this

        self.thumbnail_information = []

        # TOTALRESULTS = len(videoRendererList)
        for v in videoRendererList:
            thumbnailDict = {}
            try:
                thumbnailDict['LQ'] = v["videoRenderer"]["thumbnail"]["thumbnails"][0]["url"]
            except:
                thumbnailDict["LQ"] = None
            try:
                thumbnailDict["HQ"] = v["videoRenderer"]["thumbnail"]["thumbnails"][1]["url"]
            except:
                thumbnailDict["HQ"] = None
            try:
                thumbnailDict["Title"] = v["videoRenderer"]["title"]["runs"][0]["text"]
            except:
                thumbnailDict["Title"] = None

            self.thumbnail_information.append(thumbnailDict)
            print(thumbnailDict)

    # finds the videoRenderer objects in the script, in order to make a request for them

    def __findVideoRenderer__(self, contents):
        for c in contents:
            try:
                c["itemSectionRenderer"]["contents"][0]['videoRenderer']
                return c["itemSectionRenderer"]["contents"]
            except:
                print("Cannot find Video Renderer")
            try:
                c["itemSectionRenderer"]["contents"][1]['videoRenderer']
                return c["itemSectionRenderer"]["contents"]
            except:
                print("Still cannot find video renderer")

    def create_file_of_thumbnails(self):
        if not os.path.isdir("./" + self.youtube_search_string):
            os.makedirs("./" + self.youtube_search_string)
            for t in self.thumbnail_information:
                if t['Title'] != None:
                    print(t["Title"])
                    title = re.sub(r'[^\w]', '', t['Title'])
                    try:
                        os.makedirs(
                            "./" + self.youtube_search_string + "/"+title)
                    except:
                        # horrible hashing algorithm effectively
                        title = title+str(random.randint(0, 1000))
                        os.makedirs(
                            "./" + self.youtube_search_string + "/"+title)
                    response = requests.get(t["LQ"], stream=True)
                    # print(response)
                    with open('./' + self.youtube_search_string + '/' + title + '/LQ.png', 'wb') as out_file:
                        out_file.write(response.content)
                        # Saving reading emotion for other class
                        # readEmotion('./' + self.youtube_search_string + '/' +
                        #             title + '/LQ.png')
                    if t['HQ'] != None:
                        with open('./' + self.youtube_search_string + '/' + title + '/HQ.png', 'wb') as out_file:
                            out_file.write(response.content)
                    del response
