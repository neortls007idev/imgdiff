import sys
from PIL import Image
from PIL import ImageChops
from PIL import ImageDraw,ImageColor

errorpixel = (255,0,255,255) #color of the errorpixel

def getBrightness(p):
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
			if a > tolerance:
				imNew.putpixel((i,j),errorpixel)
	return imNew		

def diffErrorOverlay(img1,img2,tolerance):
	imNew = Image.new('RGBA',(img1.size),'white')
	for i in range(img1.size[0]):
		for j in range(img1.size[1]):
			a = reduce(lambda x,y:x+y ,diffpix(img1.getpixel((i,j)),img2.getpixel((i,j))))
			if a > tolerance:
				imNew.putpixel((i,j),errorpixel)
			else:
				imNew.putpixel((i,j),img1.getpixel((i,j)))	
	return imNew

parameters=sys.argv
num = len(parameters)
img1 = Image.open(sys.argv[1])
img2 = Image.open(sys.argv[2])
if num>3:
	mode = sys.argv[3]
if num>4:
	tolF= int(sys.argv[4])

if num==3:
	imDisplay=diffTransImage(img1,img2)	

if num==4:
	if mode=="E":
		imDisplay=diffError(img1,img2,20)
	if mode=="ET":
		imDisplay=diffErrorOverlay(img1,img2,20)
	else:
		imDisplay=diffTransImage(img1,img2)	

elif num==5:	
	if mode=="E":
		imDisplay=diffError(img1,img2,tolF)
	elif mode=="ET":
		imDisplay=diffErrorOverlay(img1,img2,tolF)	
	
imDisplay.show()