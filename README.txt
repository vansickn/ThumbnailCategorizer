# this program uses a series of sub-systems to categorize thumbnails among three variables, Attractiveness, Faceism ratio, and Facial Emotion #

# Scraper #
This is a webscraping tool which is also found in a seperate repository on my github, but this one is much more modular.
It takes a youtube search link, and scrapes a specific script to return about 30-40 video thumbnails

# HaystackAPI #
Using the HaystackAPI, I determine the emotions displayed on the face, as well as the attractiveness of the person

# Faceism Calculator #
Also found in a seperate repository, a simple GUI make with python tkinter.
User clicks three points on the thumbnail. The Top of the face, the bottom of the chin, and the bottom of the torso.
This generates the faceism ratio of the person. (The size of the face compared to the rest of the body)

# Create Table #
Using pandas, I create a three variable crosstab which finds the number of thumbnails held constant for three specific variables.
Then, the program asks for three variables you wish to create a report of. Using those variables, we can find all the thumbnails which hold those variables constant.

Refer questions to vansickn@union.edu