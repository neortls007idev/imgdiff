import sys
from PIL import Image
from PIL import ImageChops
from PIL import ImageDraw,ImageColor
import Tkinter
import ImageTk
from colorthief import ColorThief as ct

errorpixel = (255,0,255 ,255) #color of the errorpixel

def getBrightness(p): #calculating alpha value from rgb
	return int(0.3*p[0]+0.59*p[1]+0.11*p[2])

def diffpix(p1,p2):
	r=abs(p1[0]-p2[0])
	g=abs(p1[1]-p2[1])
	b=abs(p1[2]-p2[2])
	a = getBrightness((r,g,b))
	return (r,g,b,a)

def diffTransImage(img1,img2):
	imNew = Image.new('RGBA',(img1.size),'white')
	for i in range(img1.size[0]):
		for j in range(img1.size[1]):
			imNew.putpixel((i,j),diffpix(img1.getpixel((i,j)),img2.getpixel((i,j))))
	return imNew		

def diffError(img1,img2,tolerance):
	imNew = Image.new('RGBA',(img1.size),'white')
	for i in range(img1.size[0]):
		for j in range(img1.size[1]):
			a = reduce(lambda x,y:x+y ,diffpix(img1.getpixel((i,j)),img2.getpixel((i,j))))
			if a/3 > tolerance:
				imNew.putpixel((i,j),errorpixel)
	return imNew		

def diffErrorOverlay(img1,img2,tolerance):
	imNew = Image.new('RGBA',(img1.size),'white')
	for i in range(img1.size[0]):
		for j in range(img1.size[1]):
			a = reduce(lambda x,y:x+y ,diffpix(img1.getpixel((i,j)),img2.getpixel((i,j))))
			if a/3 > tolerance:
				imNew.putpixel((i,j),errorpixel)
			else:
				imNew.putpixel((i,j),img1.getpixel((i,j)))	
	return imNew
def overlayImage(img1,img2,alpha):
	try:
		return Image.blend(img1, img2, float(alpha)/100)
	except ValueError:
		return Image.blend(img1.convert('RGB'), img2.convert('RGB'), float(alpha)/100)

def slideImage(img1,img2,percent):
	imNew = Image.new('RGB',(img1.size),'white')
	sizex=img1.size[0]
	sizey=img1.size[1]
	x = (sizex*percent)/100
	img1crop = img1.crop((x,0,sizex,sizey))
	img2crop = img2.crop((0,0,x,sizey))
	imNew.paste(img1crop,(x,0))
	imNew.paste(img2crop,(0,0))
	return imNew

oldval=(0,0)

def displayDiff(val):
	global oldval
	newval=(val,my_var.get())
	if newval[0]!=oldval[0] or newval[1]!=oldval[1]:
		if my_var.get()==0:
			if newval[1]!=oldval[1]:
				imD=diffTransImage(img1,img2)
				scaletext.config(text="\nSlider has no Affect\n")

		elif my_var.get()==1:
			imD=diffError(img1,img2,int(val))
			scaletext.config(text="\nChange Tolerance\n")

		elif my_var.get()==2:
			imD=diffErrorOverlay(img1,img2,int(val))
			scaletext.config(text="\nChange Tolerance\n")
		elif my_var.get()==3:
			imD= overlayImage(img1,img2,int(val))
			scaletext.config(text="\nChange Image2 Transparency\n")

		else:
			imD=slideImage(img1,img2,int(val))		
			scaletext.config(text="\nSlide to Change Images\n")

		try:
			imD=imD.convert('RGB')
		except:
			pass		
		try:	
			img = ImageTk.PhotoImage(imD)
			panel.config(image=img)
			panel.image=img
		except UnboundLocalError:
			pass	
		oldval=newval

def refresh():
	z=scale.get()
	displayDiff(z)

def resize(img1,img2):
	basewidth = min(img1.size[0],img2.size[0])
	wpercent = (basewidth/float(img1.size[0]))
	hsize = int((float(img1.size[1])*float(wpercent)))
	img = img1.resize((basewidth,hsize), Image.ANTIALIAS)
	return img


class Pallete:

	def __init__(self,val,path,parent):
		self.val = int(val)
		self.pallete = self.getProminent(path,self.val)
		self.Tkimg = ImageTk.PhotoImage(self.pallete)
		self.TkL = Tkinter.Label(parent, image = self.Tkimg)
		self.TkL.pack(side = "left", fill = "both", expand = "yes")

	def getProminent(self,img,val=1):
		z=int(200/int(val))
		imNew = Image.new('RGB',(z*val,60),'white')
		a = [i for i in range(0,z*val,z)]
		ctimg=ct(img)
		if val>1:
			pallete = ctimg.get_palette(color_count=val)
			for i in range(val):
				imTemp = Image.new('RGB',(z,60),pallete[i])
				imNew.paste(imTemp,(z*i,0))
		else:
			pallete = ctimg.get_color()
			imTemp = Image.new('RGB',(z,60),pallete)
			imNew.paste(imTemp,(0,0))
		return imNew	
	
parameters=sys.argv
num = len(parameters)
img1 = Image.open(sys.argv[1])
img2 = Image.open(sys.argv[2])

sizeDiff=0
if img1.size!=img2.size:
	img1 = resize(img1,img2)
	img2 = resize(img2,img1)
	sizeDiff=1


root = Tkinter.Tk()
root.title("imgDiff")
my_var = Tkinter.IntVar()
my_var.set(4)


img = ImageTk.PhotoImage(img1)
if sizeDiff:
	sizeError = Tkinter.Label(root, text="\nThe Images are of different sizes.\n They have been resized to the smaller one\n")
	sizeError.pack()

diffBox = Tkinter.Label(root)
diffBox.pack(side="top")

imgBox = Tkinter.Label(diffBox)
imgBox.pack(side="left")

panel = Tkinter.Label(imgBox, image = img)
panel.pack(side = "top", fill = "both", expand = "yes")

scale = Tkinter.Scale(imgBox,orient='horizontal', from_=0, to=100, showvalue=0,command=displayDiff,length=min(img1.size[0],img2.size[0]))
scale.pack(side = "top")
scaletext = Tkinter.Label(imgBox, text="\nSlide to Change Images\n")
scaletext.pack(side="top")

radioBox = Tkinter.Label(diffBox)
radioBox.pack(side="left")
radioarr = ['Differences Only','Differences as ErrorPixels','ErrorPixels Overlay','Image Overlay','Slide Difference']
for i , j in enumerate(radioarr):
	rb = Tkinter.Radiobutton(radioBox, text=j, variable=my_var, value=i,command=refresh)
	rb.pack(anchor='w')


palleteBox = Tkinter.Label(root)
palleteBox.pack(side="top")
pallete1 = Pallete(sys.argv[3],sys.argv[1],palleteBox)
gap = Tkinter.Label(palleteBox,width=5)
gap.pack(side="left")
pallete2 = Pallete(sys.argv[3],sys.argv[2],palleteBox)

root.mainloop()

