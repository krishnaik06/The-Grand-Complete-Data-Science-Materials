import matplotlib.pyplot as plt

import numpy as np
import cv2
import os
import matplotlib.image as mpimg
from moviepy.editor import VideoFileClip
import math

def interested_region(img, vertices):
    if len(img.shape) > 2: 
        mask_color_ignore = (255,) * img.shape[2]
    else:
        mask_color_ignore = 255
        
    cv2.fillPoly(np.zeros_like(img), vertices, mask_color_ignore)
    return cv2.bitwise_and(img, np.zeros_like(img))

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    # print(lines)
    lines_drawn(line_img,lines)
    return line_img
    
def lines_drawn(img, lines, color=[255, 0, 0], thickness=6):
    global cache
    global first_frame
    slope_l, slope_r = [],[]
    lane_l,lane_r = [],[]

    α =0.2 
    
    
    for line in lines:
        for x1,y1,x2,y2 in line:
            slope = (y2-y1)/(x2-x1)
            if slope > 0.4:
                slope_r.append(slope)
                lane_r.append(line)
            elif slope < -0.4:
                slope_l.append(slope)
                lane_l.append(line)
        #2
        img.shape[0] = min(y1,y2,img.shape[0])
    
    # to prevent errors in challenge video from dividing by zero
    if((len(lane_l) == 0) or (len(lane_r) == 0)):
        print ('no lane detected')
        return 1
        
    #3
    slope_mean_l = np.mean(slope_l,axis =0)
    slope_mean_r = np.mean(slope_r,axis =0)
    mean_l = np.mean(np.array(lane_l),axis=0)
    mean_r = np.mean(np.array(lane_r),axis=0)
    
    if ((slope_mean_r == 0) or (slope_mean_l == 0 )):
        print('dividing by zero')
        return 1
    
    x1_l = int((img.shape[0] - mean_l[0][1] - (slope_mean_l * mean_l[0][0]))/slope_mean_l) 
    x2_l = int((img.shape[0] - mean_l[0][1] - (slope_mean_l * mean_l[0][0]))/slope_mean_l)   
    x1_r = int((img.shape[0] - mean_r[0][1] - (slope_mean_r * mean_r[0][0]))/slope_mean_r)
    x2_r = int((img.shape[0] - mean_r[0][1] - (slope_mean_r * mean_r[0][0]))/slope_mean_r)
    
    #6
    if x1_l > x1_r:
        x1_l = int((x1_l+x1_r)/2)
        x1_r = x1_l
        y1_l = int((slope_mean_l * x1_l ) + mean_l[0][1] - (slope_mean_l * mean_l[0][0]))
        y1_r = int((slope_mean_r * x1_r ) + mean_r[0][1] - (slope_mean_r * mean_r[0][0]))
        y2_l = int((slope_mean_l * x2_l ) + mean_l[0][1] - (slope_mean_l * mean_l[0][0]))
        y2_r = int((slope_mean_r * x2_r ) + mean_r[0][1] - (slope_mean_r * mean_r[0][0]))
    else:
        y1_l = img.shape[0]
        y2_l = img.shape[0]
        y1_r = img.shape[0]
        y2_r = img.shape[0]
      
    present_frame = np.array([x1_l,y1_l,x2_l,y2_l,x1_r,y1_r,x2_r,y2_r],dtype ="float32")
    
    if first_frame == 1:
        next_frame = present_frame        
        first_frame = 0        
    else :
        prev_frame = cache
        next_frame = (1-α)*prev_frame+α*present_frame
             
    cv2.line(img, (int(next_frame[0]), int(next_frame[1])), (int(next_frame[2]),int(next_frame[3])), color, thickness)
    cv2.line(img, (int(next_frame[4]), int(next_frame[5])), (int(next_frame[6]),int(next_frame[7])), color, thickness)
    
    cache = next_frame
    

# def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
#     lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
#     line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
#     lines_drawn(line_img,lines)
#     return line_img

def weighted_img(img, initial_img, α=0.8, β=1., λ=0.):
    return cv2.addWeighted(initial_img, α, img, β, λ)


def process_image(image):

	global first_frame

	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	img_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)


	lower_yellow = np.array([20, 100, 100], dtype = "uint8")
	upper_yellow = np.array([30, 255, 255], dtype="uint8")

	mask_yellow = cv2.inRange(img_hsv, lower_yellow, upper_yellow)
	mask_white = cv2.inRange(gray_image, 200, 255)
	mask_yw = cv2.bitwise_or(mask_white, mask_yellow)
	mask_yw_image = cv2.bitwise_and(gray_image, mask_yw)

	gauss_gray= cv2.GaussianBlur(mask_yw_image, (5, 5), 0)


	canny_edges=cv2.Canny(gauss_gray, 50, 150)

	imshape = image.shape
	lower_left = [imshape[1]/9,imshape[0]]
	lower_right = [imshape[1]-imshape[1]/9,imshape[0]]
	top_left = [imshape[1]/2-imshape[1]/8,imshape[0]/2+imshape[0]/10]
	top_right = [imshape[1]/2+imshape[1]/8,imshape[0]/2+imshape[0]/10]
	vertices = [np.array([lower_left,top_left,top_right,lower_right],dtype=np.int32)]
	roi_image = interested_region(canny_edges, vertices)

	theta = np.pi/180

	line_image = hough_lines(roi_image, 4, theta, 30, 100, 180)
	result = weighted_img(line_image, image, α=0.8, β=1., λ=0.)
	return result

if __name__ == "__main__":
    first_frame = 1
    white_output = './output.mp4'
    clip1 = VideoFileClip(filename='test2.mp4')
    white_clip = clip1.fl_image(process_image)
    white_clip.write_videofile(white_output, audio=False)