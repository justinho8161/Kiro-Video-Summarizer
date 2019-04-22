import multidict as multidict
import numpy as np
import os
import re
from PIL import Image, ImageChops
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pickle
import random

class wordCloud:

    def __init__(self,  words, title, run=False):
        self.words = words
        self.title = title[:-4]
        if run:
            self.makeImage(self.getFrequencyDictForText("".join(self.words)), self.title)

    def getFrequencyDictForText(self,sentence):
        fullTermsDict = multidict.MultiDict()
        tmpDict = {}

        # making dict for counting frequencies
        for text in sentence.split(" "):
            if re.match("a|the|an|the|to|in|for|of|or|by|with|is|on|that| |be", text):
                continue
            val = tmpDict.get(text, 0)
            tmpDict[text.lower()] = val + 1
        for key in tmpDict:
            fullTermsDict.add(key, tmpDict[key])
        return fullTermsDict

    def grey_color_func(self, word, font_size, position, orientation, random_state=None,**kwargs):
        return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

    def trim(self, im):
        bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return im.crop(bbox)

    def makeImage(self, text, input_file):
        cloud_mask = np.array(Image.open("word1.png"))
        wc = WordCloud(background_color="#5603ad", max_words=1000, mask=cloud_mask)
        # generate word cloud
        wc.generate_from_frequencies(text)

        # show
        fig = plt.figure()
        plt.imshow(wc.recolor(color_func=self.grey_color_func), interpolation="bilinear")
        plt.axis("off")
        fig.savefig("{}.png".format(input_file))
        plt.close(fig)

        im = Image.open("{}.png".format(input_file))
        im = self.trim(im)
        im = im.resize((700, 500), Image.ANTIALIAS)
        im.save("{}s.png".format(input_file))
