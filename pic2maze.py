import cv2 as cv
import numpy as np
image  = cv.imread("sudoku.jpg")

gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

blur = cv.GaussianBlur(gray, (5,5), 0)

thresh = cv.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
max_area = 0
c = 0
for i in contours:
        area = cv.contourArea(i)
        if area > 1000:
                if area > max_area:
                    max_area = area
                    best_cnt = i
                #    image = cv.drawContours(image, contours, c, (0, 255, 0), 3)
        c+=1
lowest = 10000000000
highest = 0
rectcoords = [[],[]]
for i in best_cnt:
    if not i[0][1]:
        continue
    if i[0][0] + i[0][1] < lowest:
        rectcoords[0] = [i[0][0],i[0][1]]
        lowest = i[0][0] + i[0][1]
    elif i[0][0] + i[0][1] > highest:
        rectcoords[1] = [i[0][0],i[0][1]]
        highest = i[0][0] + i[0][1]
cv.rectangle(image,(rectcoords[0][0], rectcoords[0][1]),(rectcoords[1][0],rectcoords[1][1]),3, 4)

mask = np.zeros((gray.shape),np.uint8)
cv.drawContours(mask,[best_cnt],0,255,-1)
cv.drawContours(mask,[best_cnt],0,0,2)

out = np.zeros_like(gray)
out[mask == 255] = gray[mask == 255]

blur = cv.GaussianBlur(out, (5,5), 0)

thresh = cv.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

c = 0
for i in contours:
        area = cv.contourArea(i)
        if area > 1000/2:
            cv.drawContours(image, contours, c, (0, 255, 0), 3)
        c+=1
print(rectcoords)
image = image[rectcoords[0][0]:rectcoords[1][0],rectcoords[0][1]:rectcoords[1][1]]
cv.imshow("Final Image", image)
cv.waitKey(0)
cv.destroyAllWindows()