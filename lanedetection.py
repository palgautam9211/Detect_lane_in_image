import cv2
import matplotlib.pyplot as pt
import numpy as np

def make_cordinates(image,line_parameters):
    slope,intercept=line_parameters
    y1=image.shape[0]
    y2 = int(y1 * (3/5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1,y1,x2,y2])
def average_slope_intercept(image,lines):
    left_fit=[]
    right_fit=[]
    for line in lines:
        x1,y1,x2,y2=line.reshape(4)
        parameters=np.polyfit((x1,x2),(y1,y2),1)
        slope=parameters[0]
        intercept=parameters[1]
        if slope<0:
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope,intercept))
    left_fit_average=np.average(left_fit, axis=0)
    right_fit_average=np.average(right_fit, axis=0)
    left_line=make_cordinates(image,left_fit_average)
    right_line=make_cordinates(image,right_fit_average)
    return np.array([left_line,right_line])


def canny(image):

    #convert in gray color to get  the gradient form of image
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    #call the canny method for identifying the edges of blur image
    canny = cv2.Canny(blur, 50, 150)
    return canny

def display_lines(image,lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2= line.reshape(4)
            cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)
    return line_image


    
def region_of_interest(image):

    #vertices of region that we are selected
    polygons=np.array([
        [(200,700),(1100,700),(550,250)]
    ])

    #mask:  simply display the part of the image that we are interested in
    #set the image as zeros(black) color
    mask=np.zeros_like(image)

    #This function fills the polygon with color(255) on the mask
    cv2.fillPoly(mask,polygons,255)

    #masked_image = cv2.bitwise_and(originalImage,maskedImage ) performs a bitwise AND operation
    # between the original image and a mask. This operation is useful for isolating
    # or highlighting specific regions of interest in an image based on the mask you’ve created
    masked_image=cv2.bitwise_and(image,mask)
    return masked_image

image=cv2.imread('test_image.jpg')
lane_image=np.copy(image)
cannyedge=canny(lane_image)
cropped_image=region_of_interest(cannyedge)
#The Hough transform is a computer vision algorithm that can detect lines, circles, and other shapes in an image.
#it has a two parameter r and theta
lines=cv2.HoughLinesP(cropped_image,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=4)
averaged_lines=average_slope_intercept(lane_image,lines)
line_image=display_lines(lane_image,averaged_lines)
combo_image=cv2.addWeighted(lane_image,0.8,line_image,1,1)
cv2.imshow("Result" , combo_image)
cv2.waitKey(0)