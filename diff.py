import sys
from PIL import Image
from PIL import ImageChops
from PIL import ImageDraw,ImageColor
import Tkinter
import ImageTk

errorpixel = (255,0,255,255) #color of the errorpixel

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

def displayError(val):
	global oldval
	newval=(val,my_var.get())
	if newval[0]!=oldval[0] or newval[1]!=oldval[1]:
		if my_var.get()==0:
			if newval[1]!=oldval[1]:
				imD=diffTransImage(img1,img2)
		elif my_var.get()==1:
			imD=diffError(img1,img2,int(val))
		elif my_var.get()==2:
			imD=diffErrorOverlay(img1,img2,int(val))
		elif my_var.get()==3:
			imD= overlayImage(img1,img2,int(val))
		else:
			imD=slideImage(img1,img2,int(val))		
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
	displayError(z)

def resize(img1,img2):
	basewidth = min(img1.size[0],img2.size[0])
	wpercent = (basewidth/float(img1.size[0]))
	hsize = int((float(img1.size[1])*float(wpercent)))
	img = img1.resize((basewidth,hsize), Image.ANTIALIAS)
	return img


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
my_var = Tkinter.IntVar()
my_var.set(4)


img = ImageTk.PhotoImage(img1)
if sizeDiff:
	sizeError = Tkinter.Label(root, text="\nThe Images are of different sizes.\n They have been resized to the smaller one\n")
	sizeError.pack()

scale = Tkinter.Scale(orient='horizontal', from_=0, to=100, showvalue=0,command=displayError)
scale.pack()

panel = Tkinter.Label(root, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")

rb0 = Tkinter.Radiobutton(root, text='Differences Only(Slider has no affect)', variable=my_var, value=0,command=refresh)
rb1 = Tkinter.Radiobutton(root, text='Differences as ErrorPixels(Slider for Tolerance Level)', variable=my_var, value=1,command=refresh)
rb2 = Tkinter.Radiobutton(root, text='ErrorPixels Overlay(Slider for Tolerance Level)', variable=my_var, value=2,command=refresh)
rb3 = Tkinter.Radiobutton(root, text='Image Overlay', variable=my_var, value=3,command=refresh)
rb4 = Tkinter.Radiobutton(root, text='Slide Difference', variable=my_var, value=4,command=refresh)

rb0.pack(anchor='w')
rb1.pack(anchor='w')
rb2.pack(anchor='w')
rb3.pack(anchor='w')
rb4.pack(anchor='w')

root.mainloop()

