import cv2
import numpy as np
import pandas as pd

img = cv2.imread('WYDO/IMG_1472.jpg')
gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
lines = cv2.HoughLines(edges, rho=1, theta=np.pi/180, threshold=100)
# lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)

line_list = []

for line in lines:
    print(line[0])
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    line_list.append({'rho': rho, 'theta': theta, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

df = pd.DataFrame(line_list)

# display the DataFrame
print(df)
