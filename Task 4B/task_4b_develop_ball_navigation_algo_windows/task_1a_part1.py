'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 1A - Part 1 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
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

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_1a_part1.py
# Functions:		scan_image
# 					[ Comma separated list of functions in this file ]
# Global variables:	shapes
# 					[ List of global variables defined in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, os)                ##
##############################################################
import cv2
import numpy as np
import os
##############################################################


# Global variable for details of shapes found in image and will be put in this dictionary, returned from scan_image function
shapes = {}


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################






##############################################################


def scan_image(warped_image):

    """
    Purpose:
    ---
    this function takes file path of an image as an argument and returns dictionary
    containing details of colored (non-white) shapes in that image

    Input Arguments:
    ---
    `img_file_path` :		[ str ]
        file path of image

    Returns:
    ---
    `shapes` :              [ dictionary ]
        details of colored (non-white) shapes present in image at img_file_path
        { 'Shape' : ['color', Area, cX, cY] }
    
    Example call:
    ---
    shapes = scan_image(img_file_path)
    """

    global shapes

    ##############	ADD YOUR CODE HERE	##############
	
    
     #Convert image to Grayscale:
    warped_image = cv2.cvtColor(warped_image, cv2.COLOR_BGR2GRAY)
    
     #Convert Grayscale Image to Binary:
    bin_img=cv2.threshold(warped_image, 245, 255, type=cv2.THRESH_BINARY)
    bin_img=bin_img[1]
    #display(Image.fromarray(bin_img))
    
    #Detect Contours in the Binary Image, each contour represents perimeter of each shape detected:
    contours=cv2.findContours(bin_img,1,2)
    contours=contours[0]
    
    #Initializing the dictionary shapes:
    shapes={}
    
    if len(contours) is 0:
        return shapes
    
    #Initializing a list to store the values before sorting with respect to area
    unsorted_shapes=[]
    
    #For Loop that iterates through each contour(shape) detected except the last one since the last one is the boundary of the entire image itself    
    for cont in contours[:-1]:
        
        #Finding the coordinates of each vertex of the shape detected and storing it in the array points:
        points=cv2.approxPolyDP(cont, 0.01*cv2.arcLength(cont,True), True)
        #n = No. of vertices
        n=len(points)
        
        #Initializing centroid coordinates as (0,0)
        cX=0
        cY=0
        
        #Iterating through each point detected and adding its X and Y coordinates
        for p in points:
            cY=cY+p[0][1]
            cX=cX+p[0][0]
            
        #Dividing the total sum of X,Y coordinates by the number of points to find the centroid coordinates
        cX=cX//n
        cY=cY//n
        
        #Detecting the colour code at the centroid of the shape, then finding out its colour:
        #b,g,r=warped_image[cY, cX]
        #if g<r and b<r:
        #    colour="red"
        #elif r<g and b<g:
        #    colour="green"
        #elif r<b and g<b:
        #    colour="blue"
        #else:
        colour="black"
            
        #Considering a polygon of n sides, it can be divided into n triangles by connecting each vertex to the centroid
        #Area of the polygon can be calculated by finding the area of each triangle using Heron's Formula and then adding the area of each triangle up.
        
        #Initializing a list sides to contain all the side lengths:
        sides=[]
        #Initializing a list radii to contain the distances from the centroid to each vertex:
        radii=[]
        
        #Filling up sides and radii with distance values:
        for i in range(n-1):
            sides.append((((points[i][0][0]-points[i+1][0][0])**2)+((points[i][0][1]-points[i+1][0][1])**2))**0.5)
            radii.append(((((points[i][0][0]-cX)**2)+(points[i][0][1]-cY)**2)**0.5))
        sides.append((((points[0][0][0]-points[n-1][0][0])**2)+((points[0][0][1]-points[n-1][0][1])**2))**0.5)
        radii.append(((((points[n-1][0][0]-cX)**2)+(points[n-1][0][1]-cY)**2)**0.5))
        
        #Initialize area as zero:
        area=0
        
        #Iterate through each triangle that the polygon has been divided into and accumulating the area of each triangle:
        for i in range(n):
            j=i+1
            if j==n:
                j=0
            #Applying Heron's Formula:
            peri=(sides[i]+radii[i]+radii[j])/2
            area=area+(peri*(peri-sides[i])*(peri-radii[i])*(peri-radii[j]))**0.5
            
        #DETECTING THE SHAPE:
        
        if n==3:
            shape="Triangle"
            #If the shape is already a triangle, we can calculate its area directly from each side length using heron's formula for higher accuracy
            #Note: each side length is multiplied 1.01 because there is a +1% error observed in the coordinates detected by approxPolyDP function
            a=((((points[0][0][0]-points[1][0][0])**2)+((points[0][0][1]-points[1][0][1])**2))**0.5)*1.01
            b=((((points[1][0][0]-points[2][0][0])**2)+((points[1][0][1]-points[2][0][1])**2))**0.5)*1.01
            c=((((points[2][0][0]-points[0][0][0])**2)+((points[2][0][1]-points[0][0][1])**2))**0.5)*1.01
            peri=(a+b+c)/2
            area=(peri*(peri-a)*(peri-b)*(peri-c))**0.5
            
            
        elif n==4:
            #The shape is detected to be a quadrilateral,
            #Calculating length of each side:
            a=(((points[0][0][0]-points[1][0][0])**2)+((points[0][0][1]-points[1][0][1])**2))**0.5
            b=(((points[1][0][0]-points[2][0][0])**2)+((points[1][0][1]-points[2][0][1])**2))**0.5
            c=(((points[2][0][0]-points[3][0][0])**2)+((points[2][0][1]-points[3][0][1])**2))**0.5
            d=(((points[3][0][0]-points[0][0][0])**2)+((points[3][0][1]-points[0][0][1])**2))**0.5
            
            #Calculating the length of diagonals:
            diag1=(((points[0][0][0]-points[2][0][0])**2)+((points[0][0][1]-points[2][0][1])**2))**0.5
            diag2=(((points[1][0][0]-points[3][0][0])**2)+((points[1][0][1]-points[3][0][1])**2))**0.5
            
            #Checking if all angles are 90 degrees using (side1)^2 + (side2)^2 = diagonal^2 i.e. Pythagoras Theorem
            if (abs((a*a+b*b)-(diag1*diag1))**0.5)<20 and (abs((b*b+c*c)-(diag2*diag2))**0.5)<20 and (abs((c*c+d*d)-(diag1*diag1))**0.5)<20:
                #Checking if adjacent sides are equal:
                if abs(a-d)<=2:
                    shape="Square"
                else:
                    shape="Rectangle"
                    
            #Checking all sides are equal:
            elif abs(a-b)<2 and abs(b-c)<2 and abs(c-d)<2:
                shape="Rhombus"
            else: 
                #Checking if opposite sides are equal:
                if abs(a-c)<2 and abs(b-d)<2:
                    shape="Parallelogram"
                else:
                    shape="Quadrilateral"
                    
        #For a circle, we cannot calculate area by dividing into triangles,
        #So, we take the average radius from radii list we made earlier and use it to calculate area
        else:
            shape="Circle"
            radius=sum(radii)/n
            area=3.14*radius*radius
        
        #Rounding the value of area to one decimal
        area=round(area,1)
        
        #Inserting the values obtained into the unsorted list:
        unsorted_shapes.append((shape, colour , cX, cY))
    
    
    #Sorting the list with respect to decreasing area using bubble sort:
    n=len(unsorted_shapes)
    for i in range(n):
        for j in range(n-i-1):
            if unsorted_shapes[j]>unsorted_shapes[j+1]:
                temp=unsorted_shapes[j]
                unsorted_shapes[j]=unsorted_shapes[j+1]
                unsorted_shapes[j+1]=temp
    
    #Finally, inserting the sorted values in the dictionary:
    new_array_created=0
    for i in range(n):
        if unsorted_shapes[i][0] not in shapes:
            shapes[unsorted_shapes[i][0]]=[unsorted_shapes[i][1], unsorted_shapes[i][2], unsorted_shapes[i][3]]
        elif new_array_created==0:
            shapes[unsorted_shapes[i][0]]=[shapes[unsorted_shapes[i][0]]]
            shapes[unsorted_shapes[i][0]].append([unsorted_shapes[i][1], unsorted_shapes[i][2], unsorted_shapes[i][3]])
            new_array_created=1
        else:
            shapes[unsorted_shapes[i][0]].append([unsorted_shapes[i][1], unsorted_shapes[i][2], unsorted_shapes[i][3]])
    
	##################################################
    
    return shapes


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    the function first takes 'Sample1.png' as input and runs scan_image function to find details
#                   of colored (non-white) shapes present in 'Sample1.png', it then asks the user whether
#                   to repeat the same on all images present in 'Samples' folder or not

if __name__ == '__main__':

    curr_dir_path = os.getcwd()
    print('Currently working in '+ curr_dir_path)

    # path directory of images in 'Samples' folder
    img_dir_path = curr_dir_path + '/Samples/'
    
    # path to 'Sample1.png' image file
    file_num = 1
    img_file_path = img_dir_path + 'Sample' + str(file_num) + '.png'

    print('\n============================================')
    print('\nLooking for Sample' + str(file_num) + '.png')

    if os.path.exists('Samples/Sample' + str(file_num) + '.png'):
        print('\nFound Sample' + str(file_num) + '.png')
    
    else:
        print('\n[ERROR] Sample' + str(file_num) + '.png not found. Make sure "Samples" folder has the selected file.')
        exit()
    
    print('\n============================================')

    try:
        print('\nRunning scan_image function with ' + img_file_path + ' as an argument')
        shapes = scan_image(img_file_path)

        if type(shapes) is dict:
            print(shapes)
            print('\nOutput generated. Please verify.')
        
        else:
            print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.\n')
            exit()

    except Exception:
        print('\n[ERROR] scan_image function is throwing an error. Please debug scan_image function')
        exit()

    print('\n============================================')

    choice = input('\nWant to run your script on all the images in Samples folder ? ==>> "y" or "n": ')

    if choice == 'y':

        file_count = 2
        
        for file_num in range(file_count):

            # path to image file
            img_file_path = img_dir_path + 'Sample' + str(file_num + 1) + '.png'

            print('\n============================================')
            print('\nLooking for Sample' + str(file_num + 1) + '.png')

            if os.path.exists('Samples/Sample' + str(file_num + 1) + '.png'):
                print('\nFound Sample' + str(file_num + 1) + '.png')
            
            else:
                print('\n[ERROR] Sample' + str(file_num + 1) + '.png not found. Make sure "Samples" folder has the selected file.')
                exit()
            
            print('\n============================================')

            try:
                print('\nRunning scan_image function with ' + img_file_path + ' as an argument')
                shapes = scan_image(img_file_path)

                if type(shapes) is dict:
                    print(shapes)
                    print('\nOutput generated. Please verify.')
                
                else:
                    print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.\n')
                    exit()

            except Exception:
                print('\n[ERROR] scan_image function is throwing an error. Please debug scan_image function')
                exit()

            print('\n============================================')

    else:
        print('')
