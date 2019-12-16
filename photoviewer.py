from os import listdir
from os.path import isfile, join
import time
import os
import random
import tkinter
from PIL import Image, ImageTk

class PhotoViewer():
	def __init__(self):
		self.DOWNLOAD_DIRECTORY = os.path.join(os.path.dirname(__file__), 'images')
		self.root = tkinter.Tk()
		self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
		self.root.overrideredirect(1)
		self.root.geometry("%dx%d+0+0" % (self.w, self.h))
		self.root.focus_set()
		self.canvas = tkinter.Canvas(self.root,width=self.w,height=self.h)
		self.canvas.pack()
		self.canvas.configure(background='black', cursor='none')

	def showPIL(self):	
		filenames = [f for f in listdir(self.DOWNLOAD_DIRECTORY) if isfile(join(self.DOWNLOAD_DIRECTORY, f))]
		fullpath = os.path.join(self.DOWNLOAD_DIRECTORY, random.choice(filenames))
		print(fullpath)
		pilImage = Image.open(fullpath)		
		is_gif = pilImage.format == "GIF"
		imgWidth, imgHeight = pilImage.size
		ratio = min(self.w/imgWidth, self.h/imgHeight)
		imgWidth = int(imgWidth*ratio)
		imgHeight = int(imgHeight*ratio)
		pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)   
		self.image = ImageTk.PhotoImage(pilImage)

		if is_gif:
			imagesprite = self.canvas.create_image(self.w/2,self.h/2,image=self.image, format="gif -index 2")
		else:
			imagesprite = self.canvas.create_image(self.w/2,self.h/2,image=self.image)
		
		self.root.update_idletasks()
		self.root.update()
		self.root.after(2000, self.showPIL)

if __name__== "__main__":
    app = PhotoViewer()
    app.showPIL()
    app.root.mainloop()
    