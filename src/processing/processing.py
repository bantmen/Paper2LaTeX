import cv2
import cv2.cv as cv
import numpy as np

from edges import ImageNode

debug = 1

def get_semantics(file_name):
    """
    Detects circles in the given image and returns image nodes representing
    them.
    """
    img = cv2.imread(file_name, 0)
    img = cv2.medianBlur(img, 5)
    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    width, height = img.shape
    min_closest_dist = int(max(height, width) / 7)
    bounding_wiggle = min_closest_dist

    circles = cv2.HoughCircles(img, cv.CV_HOUGH_GRADIENT, 1, min_closest_dist,
                                param1=100, param2=30, minRadius=0, maxRadius=0)

    gimg = cv2.cvtColor(cimg, cv2.COLOR_BGR2GRAY)
    retval, thresh_img = cv2.threshold(gimg, 150, 255, cv2.THRESH_BINARY_INV)

    img_nodes = []
    circles = np.uint16(np.around(circles))
    for (x, y, r) in circles[0,:]:
        r2 = r + int(0.2*r) + 5 
        if debug:
            print x, y, r
            # draw the outer circle
            cv2.circle(thresh_img,(x,y),r,(0,255,0),2)
            # draw the center of the circle
            cv2.circle(thresh_img,(x,y),2,(0,0,255),3)
            # draw bounding box
            cv2.rectangle(thresh_img, (min(width, x+r2), min(height, y+r2)), (max(0, x-r2), max(0, y-r2)), (125, 125, 25), 2)
        img_node = ImageNode((max(0, x-r2), max(0, y-r2)), (min(width, x+r2), min(height, y+r2)), (x, y))
        img_nodes.append(img_node)

    if debug:
        cv2.namedWindow('detected circles', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('detected circles', 1280, 720)

        cv2.imshow('detected circles', thresh_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    print thresh_img.shape

    return img_nodes, thresh_img

# gray = cv2.cvtColor(cimg,cv2.COLOR_BGR2GRAY)
# edges = cv2.Canny(cimg, 200, 100, apertureSize=3)
# minLineLength = 50
# maxLineGap = 10
# lines = cv2.HoughLines(edges, 1, np.pi/180, 100, minLineLength, maxLineGap)

# print len(lines)

# for x1,y1,x2,y2 in lines[0]:
#     cv2.line(cimg, (x1,y1), (x2,y2), (0,255,0), 2)