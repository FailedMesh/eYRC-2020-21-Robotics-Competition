--[[
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This Lua script is to implement Task 4B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
]]--


--[[
# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_4b_lua
# Functions:        [ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]
]]--

--[[
##################### GLOBAL VARIABLES #######################
## You can add global variables in this section according   ##
## to your requirement.                                     ##
## DO NOT TAMPER WITH THE ALREADY DEFINED GLOBAL VARIABLES. ##
##############################################################
]]--

maze_walls_handle = -1
maze_index = 0
maze_array = {}
wall_array = {}
maze_walls_array = {}
base_children_list={} --Do not change or delete this variable
baseHandle = -1       --Do not change or delete this variable

--############################################################

--[[
##################### HELPER FUNCTIONS #######################
## You can add helper functions in this section according   ##
## to your requirement.                                     ##
## DO NOT MODIFY OR CHANGE THE ALREADY DEFINED HELPER       ##
## FUNCTIONS                                                ##
##############################################################
]]--

--[[
**************************************************************
  YOU ARE NOT ALLOWED TO MODIFY THIS FUNCTION
**************************************************************
	Function Name : createWall()
	Purpose:
	---
	Creates a black-colored wall of dimensions 90cm x 10cm x 10cm

	Input Arguments:
	---
	None
	
	Returns:
	---
	wallObjectHandle : number
	
	returns the object handle of the wall created
	
	Example call:
	---
	wallObjectHandle = createWall()
**************************************************************	
]]--
function createWall()
	wallObjectHandle = sim.createPureShape(0, 8, {0.09, 0.01, 0.1}, 0.0001, nil)
	--Refer https://www.coppeliarobotics.com/helpFiles/en/regularApi/simCreatePureShape.htm to understand the parameters passed to this function
	sim.setShapeColor(wallObjectHandle, nil, sim.colorcomponent_ambient_diffuse, {0, 0, 0})
	sim.setObjectInt32Parameter(wallObjectHandle,sim.shapeintparam_respondable_mask,65280)
	--Refer https://www.coppeliarobotics.com/helpFiles/en/apiFunctions.htm#sim.setObjectInt32Parameter to understand the various parameters passed. 	
	--The walls should only be collidable with the ball and not with each other.
	--Hence we are enabling only the local respondable masks of the walls created.
	sim.setObjectSpecialProperty(wallObjectHandle, sim.objectspecialproperty_collidable)
	--Walls may have to be set as renderable........................... 
	--This is required to make the wall as collidable
	return wallObjectHandle
end

--############################################################

--[[
**************************************************************
	Function Name : receiveData()
	Purpose:
	---
	Receives data via Remote API. This function is called by 
	simx.callScriptFunction() in the python code (task_2b.py)

	Input Arguments:
	---
	inInts : Table of Ints
	inFloats : Table of Floats
	inStrings : Table of Strings
	inBuffer : string
	
	Returns:
	---
	inInts : Table of Ints
	inFloats : Table of Floats
	inStrings : Table of Strings
	inBuffer : string
	
	These 4 variables represent the data being passed from remote
	API client(python) to the CoppeliaSim scene
	
	Example call:
	---
	Shall be called from the python script
**************************************************************	
]]--
function receiveData(inInts,inFloats,inStrings,inBuffer)

	--*******************************************************
	--               ADD YOUR CODE HERE
    
    maze_array[maze_index] = inInts
    maze_index = maze_index + 1
    
	--*******************************************************
	return inInts, inFloats, inStrings, inBuffer
end

--[[
**************************************************************
	Function Name : generateHorizontalWalls()
	Purpose:
	---
	Generates all the Horizontal Walls in the scene.

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	generateHorizontalWalls()
**************************************************************	
]]--
function generateHorizontalWalls()

	--*******************************************************
	--               ADD YOUR CODE HERE
    
    for i=-0.45,0.45,0.1 do
        wall_array[math.floor(i*100+0.5)]={}
        for j=-0.5,0.5,0.1 do
            wall = createWall()
            sim.setObjectPosition(wall, -1, {i,j,0.372})
            sim.setObjectOrientation(wall, -1, {0,0,0})
            sim.setObjectParent(wall, baseHandle, 1)
            wall_array[math.floor(i*100+0.5)][math.floor(j*100+0.5)] = wall
        end
    end
    
	--*******************************************************
end

--[[
**************************************************************
	Function Name : generateVerticalWalls()
	Purpose:
	---
	Generates all the Vertical Walls in the scene.

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	generateVerticalWalls()
**************************************************************	
]]--
function generateVerticalWalls()

	--*******************************************************
	--               ADD YOUR CODE HERE
    
    for i=-0.5,0.5,0.1 do
        wall_array[math.floor(i*100+0.5)] = {}
        for j=-0.45,0.45,0.1 do
            wall = createWall()
            sim.setObjectPosition(wall, -1, {i,j,0.372})
            sim.setObjectOrientation(wall, -1, {0,0,1.57})
            sim.setObjectParent(wall, baseHandle, 1)
            wall_array[math.floor(i*100+0.5)][math.floor(j*100+0.5)] = wall
        end
    end
    
	--*******************************************************
end

--[[
**************************************************************
	Function Name : deleteWalls()
	Purpose:
	---
	Deletes all the grouped walls in the given scene

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	deleteWalls()
**************************************************************	
]]--
function deleteWalls()

	--*******************************************************
	--               ADD YOUR CODE HERE
    
    sim.removeObject(maze_walls_handle)
    
    maze_index = 0
    maze_array = {}
    wall_array = {}
    maze_walls_array = {}
    
	--*******************************************************
end


--[[
**************************************************************
  YOU CAN DEFINE YOUR OWN INPUT AND OUTPUT PARAMETERS FOR THIS
						  FUNCTION
**************************************************************
	Function Name : createMaze()
	Purpose:
	---
	Creates the maze in the given scene by deleting specific 
	horizontal and vertical walls

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	createMaze()
**************************************************************	
]]--
function createMaze()
	
	--*******************************************************
	--               ADD YOUR CODE HERE
    
    --print("Entered Create Maze")
    --print(maze_array)
    
    --print(wall_array)
    --print(wall_array[-45][40])
    
    walls_to_remove = {}
    wall_count = 1
    
    for i, row in pairs(maze_array) do
        for j, cell_code in pairs(row) do
            --print(i,j,cell_code)
            
            --Calculating (x,y) centroid of the cell from the cell index
            y = (j/10)-0.55
            x = ((i/10)-0.45)
            --print(x,y, cell_code)
            
            --Converting cell_code to binary and checking which walls are not present around it
            --wall_x : x-coordinate of wall multiplied by 100
            --wall_y : y-coordinate of wall multiplied by 100
            
            --If LEFT wall is not present:
            if (cell_code%2 == 0) then
                wall_y = (y-0.05)*100
                wall_x = x*100
                wall_x = math.floor(wall_x + 0.5)
                wall_y = math.floor(wall_y + 0.5)
                --print(wall_x, wall_y)
                wall_handle = wall_array[wall_x][wall_y]
                walls_to_remove[wall_count] = wall_handle
                wall_count =  wall_count + 1
            end
            cell_code = math.floor(cell_code/2)
            
            --If TOP wall is not present:
            if (cell_code%2 == 0) then
                wall_y = y*100
                wall_x = (x-0.05)*100
                wall_x = math.floor(wall_x + 0.5)
                wall_y = math.floor(wall_y + 0.5)
                --print(wall_x, wall_y)
                wall_handle = wall_array[wall_x][wall_y]
                walls_to_remove[wall_count] = wall_handle
                wall_count =  wall_count + 1
            end
            cell_code = math.floor(cell_code/2)
            
            --If RIGHT wall is not present:
            if (cell_code%2 == 0) then
                wall_y = (y+0.05)*100
                wall_x = x*100
                wall_x = math.floor(wall_x + 0.5)
                wall_y = math.floor(wall_y + 0.5)
                --print(wall_x, wall_y)
                wall_handle = wall_array[wall_x][wall_y]
                walls_to_remove[wall_count] = wall_handle
                wall_count =  wall_count + 1
            end
            cell_code = math.floor(cell_code/2)
            
            --If BOTTOM wall is not present:
            if (cell_code%2 == 0) then
                wall_y = y*100
                wall_x = (x+0.05)*100
                wall_x = math.floor(wall_x + 0.5)
                wall_y = math.floor(wall_y + 0.5)
                --print(wall_x, wall_y)
                wall_handle = wall_array[wall_x][wall_y]
                walls_to_remove[wall_count] = wall_handle
                wall_count =  wall_count + 1
            end
        end
    end
    
    --Removing repeated walls from the walls_to_remove array:
    
    unique_walls_array = {}
    wall_count = 1
    
    for i, wall in pairs(walls_to_remove) do
        --print(i, wall)
        wall_is_unique = 1
        for _, unique_wall in pairs(unique_walls_array) do
            if (wall == unique_wall) then
                wall_is_unique = 0
            end
        end
        if (wall_is_unique == 1) then
            unique_walls_array[wall_count] = wall
            wall_count =  wall_count + 1
        end
    end
    
    --Creating the maze_walls_array:
    i = 1
    maze_walls_array = {}
    for _,row in pairs(wall_array) do
        for _,wall in pairs(row) do
            wall_is_in_maze = 1
            for _,empty_wall in pairs(unique_walls_array) do
                if (wall == empty_wall) then
                    wall_is_in_maze = 0
                end
            end
            if (wall_is_in_maze == 1) then
                maze_walls_array[i] = wall
                i = i + 1
            end
        end
    end
      
    for _,wall in pairs(unique_walls_array) do
        sim.removeObject(wall)
    end
    
	--*******************************************************
end
--[[
	Function Name : groupWalls()
	Purpose:
	---
	Groups the various walls in the scene to one object.
	The name of the new grouped object should be set as 'walls_1'.

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	groupWalls()
**************************************************************	
]]--

function groupWalls()
	--*******************************************************
	--               ADD YOUR CODE HERE

    maze_walls_handle = sim.groupShapes(maze_walls_array)
    sim.setObjectName(maze_walls_handle, "walls_1")

	--*******************************************************
end

--[[
	Function Name : addToCollection()
	Purpose:
	---
	Adds the 'walls_1' grouped object to the collection 'colliding_objects'.  

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	addToCollection()
**************************************************************	
]]--

function addToCollection()
	--*******************************************************
	--               ADD YOUR CODE HERE

    collection_handle = sim.getCollectionHandle("colliding_objects")
    sim.addObjectToCollection(collection_handle, maze_walls_handle, sim.handle_single, 0)

	--*******************************************************
end

--[[
	******************************************************************************
			YOU ARE ALLOWED TO MODIFY THIS FUNCTION DEPENDING ON YOUR PATH. 
	******************************************************************************
	Function Name : drawPath(inInts,path,inStrings,inBuffer)
	Purpose:
	---
	Builds blue coloured lines in the scene according to the
	path generated from the python file. 

	Input Arguments:
	---
	inInts : Table of Ints
	inFloats : Table of Floats (containing the path generated)
	inStrings : Table of Strings
	inBuffer : string
	
	Returns:
	---
	inInts : Table of Ints
	inFloats : Table of Floats
	inStrings : Table of Strings
	inBuffer : string
	
	Example call:
	---
	Shall be called from the python script
**************************************************************	
]]--
function drawPath(inInts,path,inStrings,inBuffer)
	posTable=sim.getObjectPosition(maze_walls_handle,-1)
	print('=========================================')
	print('Path received is as follows: ')
	print(path)
	if not lineContainer then
		_lineContainer=sim.addDrawingObject(sim.drawing_lines,1,0,maze_walls_handle,99999,{0.2,0.2,1})
		sim.addDrawingObjectItem(_lineContainer,nil)
		if path then
			local pc=#path/2
			for i=1,pc-1,1 do
				lineDat={path[(i-1)*2+1],path[(i-1)*2+2],posTable[3]-0.03,path[(i)*2+1],path[(i)*2+2],posTable[3]-0.03}
				sim.addDrawingObjectItem(_lineContainer,lineDat)
			end
		end
	end
	return inInts, path, inStrings, inBuffer
end

--[[
**************************************************************
	Function Name : sysCall_init()
	Purpose:
	---
	Can be used for initialization of parameters
	
	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_init()
	--*******************************************************
	--               ADD YOUR CODE HERE
 
	--*******************************************************
end

--[[
**************************************************************
		YOU ARE NOT ALLOWED TO MODIFY THIS FUNCTION.
		YOU CAN DEFINE YOUR OWN INPUT AND OUTPUT 
		PARAMETERS ONLY FOR CREATEMAZE() FUNCTION
**************************************************************
	Function Name : sysCall_beforeSimulation()
	Purpose:
	---
	This is executed before simulation starts
	
	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_beforeSimulation()
	
	generateHorizontalWalls()
	generateVerticalWalls()
	createMaze()--You can define your own input and output parameters only for this function
	groupWalls()
	addToCollection()
end

--[[
**************************************************************
		YOU ARE NOT ALLOWED TO MODIFY THIS FUNCTION. 
**************************************************************
	Function Name : sysCall_afterSimulation()
	Purpose:
	---
	This is executed after simulation ends
	
	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_afterSimulation()
	-- is executed after a simulation ends
	deleteWalls()
    evaluation_screen_respondable=sim.getObjectHandle('evaluation_screen_respondable@silentError')
    if(evaluation_screen_respondable~=-1) then
        sim.removeModel(evaluation_screen_respondable)
    end
end

function sysCall_cleanup()
	-- do some clean-up here
end

-- See the user manual or the available code snippets for additional callback functions and details