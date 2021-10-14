from create_table import CreateTable
from facesim_calculator import faceismCalculator
from scraper import *
from read_emotion_attractiveness import *


print("Make sure if you run an operation that isn't all, there must be a folder with thumbnails first")
operation = input(
    "What operation do you want to run? All(1) ReadEmotion(2) Faceism(3) CreateTable(4)")
input = input("Write Youtube Search Here: ")


if operation == '1':
    # scrape the thumbnails and insert them into a folder
    s = Scraper(input)

    # read the emotions / if face exists in the thumbnail
    r = ReadEmotion(input)

    # run through the faceism ratio program, calculate faceism ratio, and override emotion if neccessary
    m = faceismCalculator(input)

    # calculate table which keeps faceism ratio, attractiveness constant
    t = CreateTable(input)


elif operation == '2':
    r = ReadEmotion(input)
elif operation == '3':
    f = faceismCalculator(input)
elif operation == '4':
    t = CreateTable(input)
else:
    print("Not a valid input")
