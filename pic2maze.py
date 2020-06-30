import cv2
from imutils import contours
import numpy as np
import time
def isObstacle(img): ## actually write this lol
	grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	(thresh, blackAndWhiteImage) = cv2.threshold(grayimg, 20, 255, cv2.THRESH_BINARY)
	cv2.imwrite('Blackwhiteimage.jpg', blackAndWhiteImage)
	cv2.waitKey(175)
	print(np.mean(blackAndWhiteImage))
	if np.mean(blackAndWhiteImage) > 254.9:
		return False
	else: 
		return True
def p2m(img,height):
	# Load image, grayscale, and adaptive threshold
	image = cv2.imread(img)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,57,5)

	# Filter out all numbers and noise to isolate only boxes
	cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if len(cnts) == 2 else cnts[1]
	for c in cnts:
		area = cv2.contourArea(c)
		if area < 1000:
			cv2.drawContours(thresh, [c], -1, (0,0,0), -1)

	# Fix horizontal and vertical lines
	vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,5))
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, vertical_kernel, iterations=9)
	horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,1))
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, horizontal_kernel, iterations=4)

	# Sort by top to bottom and each row by left to right
	invert = 255 - thresh
	cnts = cv2.findContours(invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if len(cnts) == 2 else cnts[1]
	(cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")

	rows = []
	row = []
	cnts = cnts[2:]
	for (i, c) in enumerate(cnts, 1):
		area = cv2.contourArea(c)
		if True:
			row.append(c)
			if i % height == 0:  
				(cnts, _) = contours.sort_contours(row, method="left-to-right")
				rows.append(cnts)
				row = []
	cv2.imwrite('thresh.jpg',thresh)
	cv2.imwrite('invert.jpg',invert)
	return(rows)
def checkobs(img,rows):
	image = cv2.imread(img)
	pos = 0
	obs = []
	for row in rows:
		for c in row:
			pos += 1
			mask = np.zeros(image.shape, dtype=np.uint8)
			cv2.drawContours(mask, [c], -1, (255,255,255), -1)
			result = cv2.bitwise_and(image, mask)
			result[mask==0] = 255
			cv2.imwrite('hel.jpg',result)
			if isObstacle(result):
				obs.append(pos)
	return(pos, obs)
def main(blank,obs,width):
	return(checkobs('obsmaze.png',p2m('IMG_0954.JPG',width)))