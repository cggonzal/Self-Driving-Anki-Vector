import anki_vector
import time
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt

with anki_vector.Robot(enable_camera_feed=True) as robot:
    robot.motors.set_head_motor(-5.0) # move head to look at ground
    robot.motors.set_wheel_motors(10, 10) # set initial driving direction
    for count in range(25):
        while not robot.camera.latest_image:
            time.sleep(1.0)

        imageFromVector = robot.camera.latest_image
        image = cv2.cvtColor(np.array(imageFromVector),cv2.COLOR_RGB2GRAY) #convert image to gray

        maskArea = np.array([[(125, 200),(175,100), (450, 100), (500, 225)]], dtype=np.int32)

        blank = np.zeros_like(image)

        mask = cv2.fillPoly(blank, maskArea, 255)

        maskedImage = cv2.bitwise_and(image, mask)

        image_canny = cv2.Canny(maskedImage,50,200,apertureSize=3)

        rho = 2
        theta = np.pi/180
        threshold = 50
        minLine = 50
        maxLine = 8
        lines = cv2.HoughLinesP(image_canny, rho, theta, threshold, np.array([]), minLineLength=minLine, maxLineGap=maxLine)
        #lines = cv2.HoughLines(image_canny,1,np.pi/180,200) # for regular Hough Transform



        try:
            if lines[0,0,0] < 150: # turn left slightly
                robot.motors.set_wheel_motors(10, 15)

            elif lines[1,0,0] > 450: # turn right slightly
                robot.motors.set_wheel_motors(15, 10)

            else: # go straight
                robot.motors.set_wheel_motors(10, 10)
        except:
            print("didnt find any")

        # the code below is for testing purposes
        # plt.imshow(image_canny)
        # #plt.imshow(image,cmap="gray")
        # plt.show()
        # cv2.waitKey(3)
        # print(lines)
