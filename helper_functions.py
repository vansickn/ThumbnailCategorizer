import os


def listdir_nohidden(path):
    #     # Exclude all with . in the start
    return [i for i in os.listdir(path) if i[0] != "."]
