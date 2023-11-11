import msilib
from sys import path_importer_cache
from xmlrpc.client import boolean
from mcpi.minecraft import Minecraft
from mcpi import block
from time import sleep
from Houses import House
import random 
import math

class housePath:
    def __init__(self, xhouse, yhouse, zhouse, xstart, ystart, zstart):
        self.path = []
        self.xloc = xhouse
        self.yloc = yhouse
        self.zloc = zhouse
        self.xstart = xstart
        self.ystart = ystart
        self.zstart = zstart
        self.xfront = 0
        self.zfront = 0
        self.section = ""
        self.direction = ""

    def addCurrentPathLocation(self, cur_path):
        self.path.append(cur_path)

    # finds and sets the section the path goes towards
    def setPathSection(self):
        if self.xstart < self.xloc and self.zstart >= self.zloc:
            self.section = "north_east"
        if self.xstart >= self.xloc and self.zstart > self.zloc:
            self.section = "north_west"
        if self.xstart < self.xloc and self.zstart <= self.zloc:
            self.section = "south_east"
        if self.xstart >= self.xloc and self.zstart < self.zloc:
            self.section = "south_west"       
    
    # gives a random last direction that the path would enter the house by using a dictionary
    def setRandomDirection(self, path_end_directions):
        self.setPathSection()
        direction = path_end_directions[self.section][random.randint(0,1)]
        self.direction = direction 

    def smoother(self):
        mc = Minecraft.create()
        for curr_path in range(len(self.path)-12):
            if self.path[curr_path][1] == self.path[curr_path + 12][1]:
                y = self.path[curr_path][1]
                for i in range(12):
                    mc.setBlock(self.path[curr_path][0], self.path[curr_path][1], self.path[curr_path][2], block.AIR.id)
                    self.path[curr_path + i][1] = y
                    mc.setBlock(self.path[curr_path][0], self.path[curr_path][1], self.path[curr_path][2], block.STONE_BRICK.id)
                    
            
            

    def fixEndHeight(self):
        self.path[len(self.path)-1][1] = self.yloc - 1
        for i in range(len(self.path) - 1, 0, -1):
            cur_y = self.path[i][1]
            prev_y = self.path[i - 1][1]
            # print(i, cur_y, prev_y)
            if prev_y >= cur_y - 1 and prev_y <= cur_y + 1:
                # print(prev_y, cur_y, len(self.path) - 1, i)
                break
            else: 
                if prev_y < cur_y - 1:
                    self.path[i-1][1] = cur_y - 1
                if prev_y > cur_y + 1:
                    self.path[i-1][1] = cur_y + 1

    #return the house dimenstions that the path touches
    def checkDimensions(self, avoid_list, x, z):
        for cube in avoid_list:
            if x >= cube[0] and x <= cube[2] and z >= cube[1] and z <= cube[3]:
                return cube
        return False

    def getShortestHousePosition(self, cube, x, z): 
        count = 0
        for i in cube:
            cube[count] = round(i)
            count += 1
        initial_side = ""
        
        # when the path toches a wall the side recorded
        if x == cube[0] and z > cube[1] and z < cube[3]:
            initial_side = "left"
            print(x, "left")
        if x == cube[2] and z > cube[1] and z < cube[3]:
            initial_side = "right"
            print(x, "right")

        if z == cube[1] and x > cube[0] and x < cube[2]:
            initial_side = "down"
            print(z, "down")
        if z == cube[3] and x > cube[0] and x < cube[2]:
            initial_side = "up"
            print(z, "up")


        shortest = math.dist([cube[0], cube[1]], [self.xloc, self.zloc])
        shortest_pos = [cube[0], cube[1]]

        # checks the shortest value at the bottom wall
        for x in range(cube[0], cube[2]+1):
            dist = math.dist([x, cube[1]], [self.xloc, self.zloc])
            if shortest > dist:
                shortest = dist
                shortest_pos = [x, cube[1]]

        # checks top wall
        for x in range(cube[0], cube[2]+1):
            dist = math.dist([x, cube[3]], [self.xloc, self.zloc])
            if shortest > dist:
                shortest = dist
                shortest_pos = [x, cube[3]]

        # checks left wall
        for z in range(cube[1], cube[3]+1):
            dist = math.dist([cube[0], z], [self.xloc, self.zloc])
            if shortest > dist:
                shortest = dist
                shortest_pos = [cube[0], z]

        # checks right wall
        for z in range(cube[1], cube[3]+1):
            dist = math.dist([cube[2], z], [self.xloc, self.zloc])
            if shortest > dist:
                shortest = dist
                shortest_pos = [cube[2], z]

        return initial_side, shortest_pos


    def pathingAroundHouse(self, side, dimensions, end_pos, x, y, z):
        if side == "left" or side == "right":
            path_top = [[x, y, z]]
            path_bottom = [[x, y, z]]
            print("left, right")
            # creates two paths; top and bottom 
            # top path
            for z in range(z, dimensions[3]+1):
                path_top.append([x,y,z])
            self.whileLoop(path_top, end_pos, x, y, z)

            # bottom path
            for z in reversed(range(dimensions[1], z+1)):
                path_bottom.append([x,y,z])
            self.whileLoop(path_bottom, end_pos, x, y, z)
            
            # compare path lengths
            if len(path_top) > len(path_bottom):
                for cur_path in path_bottom:
                    self.addCurrentPathLocation(cur_path)
            else:
                for cur_path in path_top:
                    self.addCurrentPathLocation(cur_path)
        

        if side == "up" or side == "down":
            path_right = [[x, y, z]]
            path_left = [[x, y, z]]
            print("up, down")
            # creates two paths; left and right path
            # left path
            for x in range(x, dimensions[2]+1):
                    path_right.append([x,y,z])
            self.whileLoop(path_right, end_pos, x, y, z)

            # right path
            for x in reversed(range(dimensions[0], x+1)):
                    path_left.append([x,y,z])
            self.whileLoop(path_left, end_pos, x, y, z)

            # compare path lengths
            if len(path_right) > len(path_left):
                for cur_path in path_left:
                    self.addCurrentPathLocation(cur_path)
            else:
                for cur_path in path_right:
                    self.addCurrentPathLocation(cur_path)
        return end_pos[0], end_pos[1]
            

    def whileLoop(self, path, end_pos, x, y, z):
        while True:
            double_up = [x, y, z]
            if random.randint(0, 1) == 0: # randomizes between the x and z directions
                x = self.pathingDirection(x, end_pos[0])
            else: # checks if zpath is on the zfront plane
                z = self.pathingDirection(z, end_pos[1])

            # prevents two of the same coordinates from being placed in the path list 
            if double_up != [x, y, z]:
                path.append([x, y, z]) 
            
            # breaks loop when the path reaches the end
            if end_pos[0] == x and end_pos[1] ==  z: 
                break
        return path


    def pathingDirection(self, value, end_value):
            if value != end_value: # checks if xpath is the same as xhouse 
                if value > end_value:
                    value -= 1
                elif value < end_value:
                    value += 1
            return value
        

    def returnList(self):
        return self.path

    def objectsInSection(self, house_objects):
        section_houses = []
        for house in house_objects:
            if house.section == self.section:
                section_houses.append(house)
        return section_houses    

    # returns boolean is there is and existig path in a section
    def findExistingPathInSection(self, section_paths):
        # print(f'this the one{section_paths[0].path.returnList()}')
        # print(f'this the one')
        if section_paths[0].path.returnList() == []:
            # print("false")
            return None
        return True
        
    # return the existing paths in a section
    def existingPathsInSection(self, section_houses):
        existing_paths = []
        
        for house in section_houses:
            # print(list(house.path.path))
            # print("if house.path.path != []:")
            if house.path.path != []:
                # print("YES")
                existing_paths.append(list(house.path.path))
        
        return existing_paths
        
    # choses wether a new path should be made or a branch
    def initializePath(self, house_front, avoid_list, house_objects, section_houses, paths):
        # determins if there's an existing path in a section
        if self.findExistingPathInSection(section_houses):
            shortest = math.dist([paths[0][0][0], paths[0][0][2]], [self.xloc, self.zloc])
            shortest_path = paths[0][0]
            for path in paths:
                for cur_path in path:
                    dist = math.dist([cur_path[0], cur_path[2]], [self.xloc, self.zloc])
                    if dist < shortest:
                        shortest = dist
                        shortest_path = cur_path
            x = shortest_path[0]
            y = shortest_path[1]
            z = shortest_path[2]
            self.createBlueprint(house_front, avoid_list, x, y, z)
        else:
            self.createBlueprint(house_front, avoid_list, self.xstart, self.ystart, self.zstart)


    def createBlueprint(self, house_front, avoid_list, xpath, ypath, zpath):
        mc = Minecraft.create()
        gold_block = block.GOLD_BLOCK.id 
        
        #adjusts the end location to the front of the house
        self.xfront = self.xloc + house_front[self.direction][0]
        self.zfront = self.zloc + house_front[self.direction][1]
        xfront = self.xfront
        zfront = self.zfront

        ypath = mc.getHeight(xpath, zpath)

        self.path = [[xpath, ypath, zpath]]

        cur_pos = 0
        while True:
            double_up = [xpath, ypath, zpath]

            # randomizes paths direction towards house by 1 block
            if random.randint(0, 1) == 0: # randomizes between the x and z directions
                xpath = self.pathingDirection(xpath, xfront)
            else: # checks if zpath is on the zfront plane
                zpath = self.pathingDirection(zpath, zfront)

            ypath = mc.getHeight(xpath, zpath)

            #checks if path is in a house area
            dimensions = self.checkDimensions(avoid_list, xpath, zpath)
            if dimensions:
                wall, shortest_pos = self.getShortestHousePosition(dimensions, xpath, zpath)
                xpath, zpath = self.pathingAroundHouse(wall, dimensions, shortest_pos, xpath, ypath, zpath)

            # prevents two of the same coordinates from being placed in the path list 
            if double_up != [xpath, ypath, zpath]:
                cur_pos += 1
                self.addCurrentPathLocation([xpath, ypath, zpath])
            
            mc.setBlock(xpath, ypath, zpath, block.STONE_BRICK.id)

            # breaks loop when the path reaches the end
            if xfront == xpath and zfront ==  zpath: 
                break
        
        prev_path_height = self.path[0][1]

        #adjusts path so that the next path isn't more than a blocks above or below
        count = 0
        for cur_path in range(len(self.path)):
            cur_height = self.path[cur_path][1]
            mc.setBlock(self.path[count][0], self.path[count][1], self.path[count][2], block.AIR.id)

            if prev_path_height + 1 < cur_height: 
                self.path[cur_path][1] = prev_path_height + 1
            if prev_path_height - 1 > cur_height:
                self.path[cur_path][1] = prev_path_height - 1
            if cur_path != 0:
                prev_path_height = self.path[cur_path][1]
            mc.setBlock(self.path[count][0], self.path[count][1], self.path[count][2], block.STONE_BRICK.id)

        

        self.fixEndHeight()
        self.smoother()

    def clearPath(self):
        mc = Minecraft.create()
        # clears out area 3x3 area above the path
        for cur_path in self.path:
            mc.setBlocks(cur_path[0]+1, cur_path[1]+1, cur_path[2]+1,cur_path[0]-1, cur_path[1]+4, cur_path[2]-1, block.AIR.id)
    
    def placeOutline(self):
        mc = Minecraft.create()
        # creates stone brick outline
        for cur_path in self.path:
            mc.setBlocks(cur_path[0]+1, cur_path[1], cur_path[2]+1,cur_path[0]-1, cur_path[1], cur_path[2]-1, block.STONE_BRICK.id)    
    
    def placeBlocksInPath(self, blockId):
        mc = Minecraft.create()
        # places a block in the path for possible customisation
        for cur_path in self.path:
            mc.setBlock(cur_path[0], cur_path[1], cur_path[2], block.STONE_BRICK.id)

        # places gold block at the end point
        mc.setBlocks(self.xloc, self.yloc - 1, self.zloc, self.xfront, self.yloc - 1, self.zfront, blockId)
        mc.setBlock(self.xloc, self.yloc, self.zloc, block.GOLD_BLOCK.id)
        

