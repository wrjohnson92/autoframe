from os import listdir
from os.path import isfile, join
import time
import os
import random
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from itertools import count
from GifResize import FullscreenGifFrames

class ImageLabel(tk.Label):
	"""a label that displays images, and plays them if they are gifs"""
	def load(self, im, w, h):
		if isinstance(im, str):
			im = Image.open(im)
			imgWidth, imgHeight = im.size
			ratio = min(w/imgWidth, h/imgHeight)
			self.imgWidth = int(imgWidth*ratio)
			self.imgHeight = int(imgHeight*ratio)
		self.loc = 0

		if im.format == "GIF":
			print("makin frames")
			self.frames = list(map(lambda x: ImageTk.PhotoImage(x), FullscreenGifFrames(im.filename, (self.imgWidth, self.imgHeight))))
			print("frames is done")
		else:
			self.frames = [ImageTk.PhotoImage(im.copy())]

		try:
			self.delay = im.info['duration']
		except:
			self.delay = 100

		if len(self.frames) == 1:
			self.config(image=self.frames[0], background="black", width=self.imgWidth, height=self.imgHeight)
		else:
			self.next_frame()

	def unload(self):
		self.config(image=None)
		self.frames = None
		self.destroy()

	def next_frame(self):
		if self.frames:
			self.loc += 1
			self.loc %= len(self.frames)
			self.config(image=self.frames[self.loc], background="black")
			self.after(self.delay, self.next_frame)

class PhotoViewer():
	def __init__(self):
		self.DOWNLOAD_DIRECTORY = os.path.join(os.path.dirname(__file__), 'images')
		self.root = tk.Tk()
		self.root.attributes("-fullscreen", True)
		self.root.configure(background='black')
		self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
		self.root.focus_set()

	def showPIL(self):
			if hasattr(self, 'lbl'):
				self.lbl.unload()

			filenames = [f for f in listdir(self.DOWNLOAD_DIRECTORY) if isfile(join(self.DOWNLOAD_DIRECTORY, f))]
			fullpath = os.path.join(self.DOWNLOAD_DIRECTORY, random.choice(filenames))
			print(fullpath)
			self.lbl = ImageLabel(self.root)
			self.lbl.pack()
			self.lbl.load(fullpath, self.w, self.h)
			self.root.after(2000, self.showPIL)

if __name__== "__main__":
    app = PhotoViewer()
    app.showPIL()
    app.root.mainloop()