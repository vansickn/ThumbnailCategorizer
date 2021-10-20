import os
import ast
import pandas as pd
from yattag import Doc
import pdfkit
import re
import helper_functions


class CreateTable:

    def __init__(self, youtube_search_string) -> None:
        self.youtube_search_string = youtube_search_string

        # can get totals by measuring length of arrays
        self.f_sm = []
        self.f_md = []
        self.f_lg = []
        self.f_xl = []

        self.a_low = []
        self.a_mid = []
        self.a_high = []
        self.a_hot = []

        self.create_categories()

        results = {
            'face_sm': len(self.f_sm),
            'face_md': len(self.f_md),
            'face_lg': len(self.f_lg),
            'face_xl': len(self.f_xl),
            'a_low': len(self.a_low),
            'a_mid': len(self.a_mid),
            'a_high': len(self.a_high),
            'a_hot': len(self.a_hot),
        }
        # print(results)
        self.create_pandas_df()

    def create_categories(self):
        # create categories
        self.dict_data = {}
        for folder in helper_functions.listdir_nohidden(self.youtube_search_string):
            # making the analyzer data workable in python
            analyzer_data = open(self.youtube_search_string +
                                 '/' + folder + "/img_analyzer_data.txt", "r").read()
            analyzer_data = analyzer_data.replace(
                'false', "False").replace('true', 'True')
            analyzer_data = ast.literal_eval(analyzer_data)
            # grabbing the faceism ratio
            try:
                faceism_ratio = ast.literal_eval(open(
                    self.youtube_search_string + '/' + folder + "/faceismRatio.txt", "r").read())
            except:
                faceism_ratio = None
            if len(analyzer_data['people']) != 1 or faceism_ratio == None:
                print("More or less than 1 person in thumbnail")
            else:
                # getting emotions
                emotions_dict = analyzer_data['people'][0]['emotion']['emotions']
                print(emotions_dict)
                print(faceism_ratio)
                print(analyzer_data['people'][0]['attractiveness'])
                self.dict_data[folder] = []
                self.dict_data[folder].append(self.evaluate_category_attractiveness(
                    analyzer_data['people'][0]['attractiveness'], self.youtube_search_string + '/' + folder))
                self.dict_data[folder].append(self.evaluate_category_faceism(
                    faceism_ratio, self.youtube_search_string + '/' + folder))
                if len(emotions_dict) != 0:
                    self.dict_data[folder].append(
                        max(emotions_dict, key=emotions_dict.get))
                else:
                    self.dict_data[folder].append(None)
        print(self.dict_data)

    def evaluate_category_faceism(self, ratio, path):
        if ratio < .25:
            self.f_sm.append(path)
            return 'sm'
        if ratio >= .25 and ratio < .5:
            self.f_md.append(path)
            return 'md'
        if ratio >= .5 and ratio < .75:
            self.f_lg.append(path)
            return 'lg'
        if ratio >= .75:
            self.f_xl.append(path)
            return 'xl'

    def evaluate_category_attractiveness(self, attractiveness, path):
        if attractiveness < 2.5:
            self.a_low.append(path)
            return 'low'
        if attractiveness >= 2.5 and attractiveness < 5:
            self.a_mid.append(path)
            return 'mid'
        if attractiveness >= 5 and attractiveness < 7.5:
            self.a_high.append(path)
            return 'high'
        if attractiveness >= 7.5:
            self.a_hot.append(path)
            return 'hot'

    def create_pandas_df(self):
        df = pd.DataFrame.from_dict(self.dict_data, orient='index',
                                    columns=['attractiveness', 'faceism ratio', 'emotion'])
        print(df)
        attractive = [self.dict_data[k][0] for k in self.dict_data.keys()]
        faceism = [self.dict_data[k][1] for k in self.dict_data.keys()]
        emotion = [self.dict_data[k][2] for k in self.dict_data.keys()]

        ct = pd.crosstab(index=[attractive], columns=[faceism, emotion])
        print(ct)

        continue_report = True
        report_no = 1
        while continue_report:
            report_info = input("Do you want to make a report? Y or N: ")
            if report_info == 'N' or report_info == 'n':
                continue_report = False
            if report_info == 'Y' or report_info == 'y':
                print("Enter Report Parameters: \n")
                a = input("Attractiveness (low,mid,high,hot): ")
                f = input("Faceism (sm,md,lg,xl): ")
                e = input("Emotion (happy,surprised,judging,afraid,neutral): ")
                file_names = []
                for index, row in df.iterrows():
                    if row['attractiveness'] == a and row['faceism ratio'] == f and row['emotion'] == e:
                        print(row.name)
                        file_names.append(row.name)
                self.sendFilesToPDF(file_names, a, f, e, report_no)
                report_no += 1
                print(ct)

    def sendFilesToPDF(self, file_names, a, f, e, report_no):
        print(file_names)
        options = {
            "enable-local-file-access": None,
        }

        doc, tag, text = Doc().tagtext()
        with tag('html'):
            with tag('body', id='hello'):
                with tag('h1'):
                    text('Report for Search: ' + self.youtube_search_string)
                    doc.stag('br')
                    text('Parameters held constant: Attractiveness: ' +
                         a + " Faceism: " + f + " Emotion: " + e)
                    for folder in file_names:
                        with tag('div'):
                            with tag('h3'):
                                text(folder)
                                doc.stag('br')
                                doc.stag(
                                    'img', src=(folder + '/LQ.png'))
                                try:
                                    doc.stag('img', src=(
                                        folder + '/with_bounding_boxes.png'))
                                    doc.stag('br')
                                    # logFile = open(self.youtube_search_string + '/' +
                                    #                folder + '/log.txt', 'r')
                                    # text(logFile.read())
                                except:
                                    text("No face detected")
                # with tag('div'):
                #     with tag('h1'):
                #         text("Number of Thumbnail Results: " +
                #              str(len(total_results)))
                #         doc.stag('br')
                #         text("Number of Faces Detected: " +
                #              str(len(aggregateEmotionData)))
                #         doc.stag('br')
                #         text("Percentage with Faces: " +
                #              str(len(aggregateEmotionData)/len(total_results)*100) + "%")
                #         doc.stag('br')
                # with tag('div'):
                #     with tag('h1'):
                #         if emotion_dict['total'] != 0:
                #             text("Angry Faces: " + str(emotion_dict['angry']))
                #             text(
                #                 " or " + str(emotion_dict['angry']/emotion_dict['total']*100) + "%")
                #             doc.stag('br')
                #             text("Sad Faces: " + str(emotion_dict['sad']))
                #             text(
                #                 " or " + str(emotion_dict['sad']/emotion_dict['total']*100) + "%")
                #             doc.stag('br')
                #             text("Disgusted Faces: " +
                #                  str(emotion_dict['disgust']))
                #             text(
                #                 " or " + str(emotion_dict['disgust']/emotion_dict['total']*100) + "%")
                #             doc.stag('br')
                #             text("Happy Faces: " + str(emotion_dict['happy']))
                #             text(
                #                 " or " + str(emotion_dict['happy']/emotion_dict['total']*100) + "%")
                #             doc.stag('br')
                #             text("Surprised Faces: " +
                #                  str(emotion_dict['surprise']))
                #             text(
                #                 " or " + str(emotion_dict['surprise']/emotion_dict['total']*100) + "%")
                #             doc.stag('br')
                #             text("Fear Faces: " + str(emotion_dict['fear']))
                #             text(
                #                 " or " + str(emotion_dict['fear']/emotion_dict['total']*100) + "%")
                #             doc.stag('br')
                #             text("Neutral Faces: " +
                #                  str(emotion_dict['neutral']))
                #             text(
                #                 " or " + str(emotion_dict['neutral']/emotion_dict['total']*100) + "%")
                #             doc.stag('br')
        print(doc.getvalue())
        htmlFile = open(self.youtube_search_string + '/' +
                        f'report_no_{report_no}.html', 'w')
        htmlFile.write(doc.getvalue())
        htmlFile.close()
        pdfkit.from_file(self.youtube_search_string + '/' +
                         f'report_no_{report_no}.html', self.youtube_search_string + '/' + f'{a}_{f}_{e}.pdf', options=options)
