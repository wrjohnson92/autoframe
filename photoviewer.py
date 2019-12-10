from os import walk
import time
import os
import random
from PIL import Image

DOWNLOAD_DIRECTORY = os.path.join(os.path.dirname(__file__), 'images')

while(True):
	f = []
	for (dirpath, dirnames, filenames) in walk(DOWNLOAD_DIRECTORY):
		image = Image.open(os.path.join(DOWNLOAD_DIRECTORY, random.choice(filenames)))
		image.show()
		time.sleep(3)