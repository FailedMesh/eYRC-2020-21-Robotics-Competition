'''
*****************************************************************************************
*
*                ===============================================
*                   Nirikshak Bot (NB) Theme (eYRC 2020-21)
*                ===============================================
*
*  This script is to implement Task 1B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''

# Team ID:            [ NB_887 ]
# Author List:        [ Tanaya Gupte, Kallol Saha ]
# Filename:            task_1b.py
# Functions:        applyPerspectiveTransform, detectMaze, writeToCsv
#                     [ Comma separated list of functions in this file ]
# Global variables:
#                     [ List of global variables defined in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, csv)               ##
##############################################################
import numpy as np
import cv2
import csv
##############################################################


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################






##############################################################


def applyPerspectiveTransform(input_img):

    """
    Purpose:
    ---
    takes a maze test case image as input and applies a Perspective Transfrom on it to isolate the maze

    Input Arguments:
    ---
    `input_img` :   [ numpy array ]
        maze image in the form of a numpy array

    Returns:
    ---
    `warped_img` :  [ numpy array ]
        resultant warped maze image after applying Perspective Transform

    Example call:
    ---
    warped_img = applyPerspectiveTransform(input_img)
    """

    warped_img = None

    ##############    ADD YOUR CODE HERE    ##############
    
    #Converting image to grayscale
    gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    #Obtaining height and width of the image
    height, width = input_img.shape[:2]
    if (height, width)== (512,512):
       edged = cv2.Canny(gray, 30, 200)
    else:
      edged=cv2.threshold(gray, 245, 255, type=cv2.THRESH_BINARY)
      edged= edged[1]
    cv2.waitKey(0)

    #Finding conours of the image:
    contours = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    #If contours contains more than 1 array, concatenating these into a single array
    if len(contours) is 2:
      s1= len(contours[0])
      s2= len(contours[1])
      C= [[[0,0]] for i in range((s1+s2)) ]
      C= np.array(C)
      C= C.reshape((s1+s2), 2)
      cnt= contours[0]
      C= np.concatenate((contours[0], contours[1]))
    elif len(contours) is 3:
      s1= len(contours[0])
      s2= len(contours[1])
      s3= len(contours[2])
      C= [[[0,0]] for i in range((s1+s2+s3)) ]
      C= np.array(C)
      C= C.reshape((s1+s2+s3), 2)
      cnt= contours[0]
      C= np.concatenate((contours[0], contours[1], contours[2]))
    else:
      C= contours[0]


    epsilon = 0.05*cv2.arcLength(C,True)
    #Applying approxPolyDP() function to get desired contours
    approx = cv2.approxPolyDP(C,epsilon,True)
    a00=0
    a01=0
    a10=0
    a11=0
    a20=0
    a21=0
    a30=0
    a31=0

    #For givan maze images:
    if (height, width)== (512,512):
    #Obtaining the 4 points to be used for perspective transform
      for i in range(len(approx)):
      #Eliminating points out of range
       if any(approx[i][0]>505):
           continue
      #Obtaining the lefmost top corner point
       if approx[i][0][0]<100:
          if approx[i][0][1]<100:
               a00= approx[i][0][0]
               a01= approx[i][0][1]
      #Obtaining the rightmost top corner point
       if approx[i][0][0]>400:
          if approx[i][0][1]<100:
            a10= approx[i][0][0]
            a11= approx[i][0][1]
      #Obtaining the rightmost bottom corner point
       if approx[i][0][0]>400:
          if approx[i][0][1]>400:
            a20= approx[i][0][0]
            a21= approx[i][0][1]
      #Obtaining the lefmost bottom corner point
       if approx[i][0][0]<100:
          if approx[i][0][1]>400:
            a30= approx[i][0][0]
            a31= approx[i][0][1]
    #For images obtained from coppelia sim vision sensor:
    else:
        for i in range(len(approx)):
            if approx[i][0][0]<200:
                if approx[i][0][1]<200:
                    a00= approx[i][0][0]
                    a01= approx[i][0][1]
            if 800<approx[i][0][0]<1020:
                if approx[i][0][1]<200:
                    a10= approx[i][0][0]
                    a11= approx[i][0][1]
            if 800<approx[i][0][0]<1020:
                if 800<approx[i][0][1]<1020:
                    a20= approx[i][0][0]
                    a21= approx[i][0][1]
            if approx[i][0][0]<200:
                if 800<approx[i][0][1]<1020:
                    a30= approx[i][0][0]
                    a31= approx[i][0][1]

    pts1 = np.float32([[a00, a01], [a10, a11], [a20, a21], [a30, a31]])
    pts2= np.float32([[0,0], [width,0],[width,height],[0,height]])
    #Applying perpective transform on the extreme points of the original image
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result= cv2.warpPerspective(input_img, matrix, (width, height))
    #Storing result as an array
    result= np.array(result)
    #Resizing vision sensor image to size- 1280x1280
    if (height, width)!= (512,512):
       result= cv2.resize(result,(1280, 1280))
    warped_img= result


    ##################################################

    return warped_img


def detectMaze(warped_img):

    """
    Purpose:
    ---
    takes the warped maze image as input and returns the maze encoded in form of a 2D array

    Input Arguments:
    ---
    `warped_img` :    [ numpy array ]
        resultant warped maze image after applying Perspective Transform

    Returns:
    ---
    `maze_array` :    [ nested list of lists ]
        encoded maze in the form of a 2D array

    Example call:
    ---
    maze_array = detectMaze(warped_img)
    """

    maze_array = []

    ##############    ADD YOUR CODE HERE    ##############
    
    #Converting warped_image to grayscale
    gray1 = cv2.cvtColor(warped_img, cv2.COLOR_BGR2GRAY)

    #Obtaining height and width of image
    width= gray1.shape[0]
    height= gray1.shape[1]

    #Obtaining the height and width of each cell
    X = width//10
    Y = height//10

    #Initiallizing a 10x10 array of zeros
    A= [0 for i in range(100)]
    A= np.array(A)
    A= A.reshape(10, 10)
    x=0
    j=0
    y=0
    i=0

    #Loop to itterate through the height of the image
    while y<= height-Y+1:
        x=0
        j=0
        l1=[]
        l2=[]
        l3=[]
        l4=[]
        #Loop to itterate through the width of the image
        while x<= width-X+1:
           #Checking if the point is on the leftmost edge of the image
           if y==0:
             A[i][j]+= 2**0
           #Checking the midpoint of the left edge with a tolerance of 3 points on either side of the edge
           else:
             l1= [gray1[x+(X//2),y-3]<100,gray1[x+(X//2),y-2]<100,gray1[x+(X//2),y-1]<100,gray1[x+(X//2),y]<100,gray1[x+(X//2),y+1]<100,gray1[x+(X//2),y+2]<100,gray1[x+(X//2),y+3]<100]
             if any(l1):
                 A[i][j]+= 2**0
           #Checking if the point is on the topmost edge of the image
           if x==0:
              A[i][j]+= 2**1
           #Checking the midpoint of the top edge with a tolerance of 3 points on either side of the edge
           else:
              l2= [gray1[x-3,y+(Y//2)]<100,gray1[x-2,y+(Y//2)]<100,gray1[x-1,y+(Y//2)]<100,gray1[x,y+(Y//2)]<100,gray1[x+1,y+(Y//2)]<100,gray1[x+2,y+(Y//2)]<100,gray1[x+3,y+(Y//2)]<100]
              if any(l2):
                 A[i][j]+= 2**1
           #Checking if the point is on the righttmost edge of the image(y+Y*10=510)
           if y+Y== 510:
              A[i][j]+= 2**2
           #Checking the midpoint of the right edge with a tolerance of 3 points on either side of the edge
           else:
              l3= [gray1[x+(X//2),y+Y-3]<100,gray1[x+(X//2),y+Y-2]<100,gray1[x+(X//2),y+Y-1]<100,gray1[x+(X//2),y+Y]<100,gray1[x+(X//2),y+Y+1]<100,gray1[x+(X//2),y+Y+2]<100,gray1[x+(X//2),y+Y+3]<100]
              if any(l3):
                 A[i][j]+= 2**2
           #Checking if the point is on the bottommost edge of the image(x+X*10=510)
           if x+X== 510:
              A[i][j]+= 2**3
           #Checking the midpoint of the bottom edge with a tolerance of 3 points on either side of the edge
           else:
              l4= [gray1[x+X-3,y+(Y//2)]<100,gray1[x+X-2,y+(Y//2)]<100,gray1[x+X-1,y+(Y//2)]<100,gray1[x+X,y+(Y//2)]<100,gray1[x+X+1,y+(Y//2)]<100,gray1[x+X+2,y+(Y//2)]<100,gray1[x+X+3,y+(Y//2)]<100]
              if any(l4):
                 A[i][j]+= 2**3
           j+=1
           x+=X
        y+=Y
        i+=1
    #Obtaining the matrix in desired form
    A=np.transpose(A)
    #Converting array to a list
    maze_array= A.tolist()

    ##################################################

    return maze_array


# NOTE:    YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
def writeToCsv(csv_file_path, maze_array):

    """
    Purpose:
    ---
    takes the encoded maze array and csv file name as input and writes the encoded maze array to the csv file

    Input Arguments:
    ---
    `csv_file_path` :    [ str ]
        file path with name for csv file to write

    `maze_array` :        [ nested list of lists ]
        encoded maze in the form of a 2D array

    Example call:
    ---
    warped_img = writeToCsv('test_cases/maze00.csv', maze_array)
    """

    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(maze_array)


# NOTE:    YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
#
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    This part of the code is only for testing your solution. The function first takes 'maze00.jpg'
#                     as input, applies Perspective Transform by calling applyPerspectiveTransform function,
#                     encodes the maze input in form of 2D array by calling detectMaze function and writes this data to csv file
#                     by calling writeToCsv function, it then asks the user whether to repeat the same on all maze images
#                     present in 'test_cases' folder or not. Write your solution ONLY in the space provided in the above
#                     applyPerspectiveTransform and detectMaze functions.

if __name__ == "__main__":

    # path directory of images in 'test_cases' folder
    img_dir_path = 'test_cases/'

    # path to 'maze00.jpg' image file
    file_num = 0
    img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

    print('\n============================================')
    print('\nFor maze0' + str(file_num) + '.jpg')

    # path for 'maze00.csv' output file
    csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'

    # read the 'maze00.jpg' image file
    input_img = cv2.imread(img_file_path)

    # get the resultant warped maze image after applying Perspective Transform
    warped_img = applyPerspectiveTransform(input_img)

    if type(warped_img) is np.ndarray:

        # get the encoded maze in the form of a 2D array
        maze_array = detectMaze(warped_img)

        if (type(maze_array) is list) and (len(maze_array) == 10):

            print('\nEncoded Maze Array = %s' % (maze_array))
            print('\n============================================')

            # writes the encoded maze array to the csv file
            writeToCsv(csv_file_path, maze_array)

            cv2.imshow('warped_img_0' + str(file_num), warped_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        else:

            print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
            exit()

    else:

        print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
        exit()

    choice = input('\nDo you want to run your script on all maze images ? => "y" or "n": ')

    if choice == 'y':

        for file_num in range(1, 10):

            # path to image file
            img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

            print('\n============================================')
            print('\nFor maze0' + str(file_num) + '.jpg')

            # path for csv output file
            csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'

            # read the image file
            input_img = cv2.imread(img_file_path)

            # get the resultant warped maze image after applying Perspective Transform
            warped_img = applyPerspectiveTransform(input_img)

            if type(warped_img) is np.ndarray:

                # get the encoded maze in the form of a 2D array
                maze_array = detectMaze(warped_img)

                if (type(maze_array) is list) and (len(maze_array) == 10):

                    print('\nEncoded Maze Array = %s' % (maze_array))
                    print('\n============================================')

                    # writes the encoded maze array to the csv file
                    writeToCsv(csv_file_path, maze_array)

                    cv2.imshow('warped_img_0' + str(file_num), warped_img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()

                else:

                    print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
                    exit()

            else:

                print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
                exit()

    else:

        print('')
