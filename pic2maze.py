import cv2 as cv
import numpy as np

image  = cv.imread("sudoku.jpg")
cv.imshow("Image", image)

gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
cv.imshow("gray", gray)

blur = cv.GaussianBlur(gray, (5,5), 0)
cv.imshow("blur", blur)

thresh = cv.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
cv.imshow("thresh", thresh)
contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

max_area = 0
c = 0
for i in contours:
        area = cv.contourArea(i)
        if area > 1000:
                if area > max_area:
                    max_area = area
                    best_cnt = i
                    image = cv.drawContours(image, contours, c, (0, 255, 0), 3)
        c+=1

mask = np.zeros((gray.shape),np.uint8)
cv.drawContours(mask,[best_cnt],0,255,-1)
cv.drawContours(mask,[best_cnt],0,0,2)
cv.imshow("mask", mask)

out = np.zeros_like(gray)
out[mask == 255] = gray[mask == 255]
cv.imshow("New image", out)

blur = cv.GaussianBlur(out, (5,5), 0)
cv.imshow("blur1", blur)

thresh = cv.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
cv.imshow("thresh1", thresh)

contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

c = 0
for i in contours:
        area = cv.contourArea(i)
        if area > 1000/2:
            cv.drawContours(image, contours, c, (0, 255, 0), 3)
        c+=1


cv.imshow("Final Image", image)
cv.waitKey(0)
cv.destroyAllWindows()