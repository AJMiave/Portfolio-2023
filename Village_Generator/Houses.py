from importlib.resources import path
from mcpi.minecraft import Minecraft
from time import sleep
import random
from mcpi import block
import decor
from decor import backyard
from decor import roof


mc = Minecraft.create()
decor_list = [116, 47, "table"]
#assigning block id's to variables
glass = block.GLASS
door = block.DOOR_WOOD.id
air = block.AIR
log = block.WOOD
stonebrick = block.STONE_BRICK
planks = block.WOOD_PLANKS
wood_slab = block.WOODEN_SLAB
terracotta = 159
brick = 44
stonebrick_stair = block.STAIRS_STONE_BRICK.id
brick_stair = block.STAIRS_BRICK.id
yellow_flower = block.FLOWER_YELLOW
cyan_flower = block.FLOWER_CYAN
torch = block.TORCH
gate = block.FENCE_GATE.id
glowstone = block.GLOWSTONE_BLOCK


#Dictionary for what style the house will be
style = {
    1: {"floor": 7, "wall": stonebrick, "pillar": log.withData(1), "roof": wood_slab, 'roof_tile': block.STAIRS_NETHER_BRICK},
    2: {"floor": 9, "wall": planks.withData(1), "pillar": log.withData(1), "roof": brick, 'roof_tile': block.STAIRS_WOOD},
    3: {"floor": 7, "wall": block.SANDSTONE, "pillar": log.withData(1), "roof": wood_slab, 'roof_tile': block.STAIRS_WOOD},
    4: {"floor": 7, "wall": block.SANDSTONE, "pillar": block.NETHER_BRICK, "roof": wood_slab, 'roof_tile': block.STAIRS_SANDSTONE},
    5: {"floor": 9, "wall": block.MOSS_STONE, "pillar": block.NETHER_BRICK, "roof": block.STONE_SLAB, 'roof_tile': block.STAIRS_NETHER_BRICK},
    6: {"floor": 9, "wall": block.SANDSTONE, "pillar": block.MOSS_STONE, "roof": block.STONE_SLAB, 'roof_tile': block.STAIRS_WOOD},
    7: {"floor": 9, "wall": block.MOSS_STONE, "pillar": log.withData(1), "roof": wood_slab, 'roof_tile': block.STAIRS_SANDSTONE},
    8: {"floor": 7, "wall": block.COBBLESTONE, "pillar": block.MOSS_STONE, "roof": block.STONE_SLAB, 'roof_tile': block.STAIRS_WOOD},
    9: {"floor": 9, "wall": block.SANDSTONE, "pillar": block.MOSS_STONE, "roof": block.STONE_SLAB, 'roof_tile': block.Block(203)}, #purple stairs roof
    10: {"floor": 7, "wall": stonebrick, "pillar": log.withData(1), "roof": wood_slab, 'roof_tile': block.Block(203)},
}

class House():
    #initialisation of a house
    def __init__(self, story, xlength, zlength, height, x, y, z, direction, house_path):
        
        self.style_type = random.randint(1,10)

        self.section = ""
        self.direction = direction
        self.path = house_path

        self.xlength = xlength
        self.zlength = zlength
        self.height = height
        self.story = story
        self.y = y
        self.xDoor = x
        self.zDoor = z
        
        #Changed values for place where house will be built as we want the front door to be at the end of the path. This allows houses to have correct rotation and orientation
        if self.direction == "South":
            self.z = z - 1
            self.x = x - (self.xlength//2) - 1

        if self.direction == "North":
            self.z = z - self.zlength
            self.x = x - (self.xlength//2) - 1

        if self.direction == "West":
            self.z = z - (self.zlength//2) - 1
            self.x = x - self.xlength

        if self.direction == "East":
            self.z = z - (self.zlength//2) - 1
            self.x = x - 1
    

    #Function for building stiars
    def build_stairs(self):
        
        #assigning variables so previous coordinates arent effected
        step = self.y
        stepz = self.z
        stepx = self.x

        #have to make an except for east as otherwise the door would spawn blocked by the stairs
        if self.direction == "East":

            #building stairs up until the second floor is built
            while step <= (self.y + self.height):

                #placement of steps
                mc.setBlock(stepx + 3, step, self.z + self.zlength - 1, stonebrick_stair, 0)
                #clearing blocks above steps so players can walk their, incase walls are built over the stairs
                mc.setBlocks(stepx + 3, step + 1, self.z + self.zlength - 1, stepx + 3, self.y + self.height + 2, self.z + self.zlength - 1, air)

                #adding support for the steps because even though gravity exists we need our designs to be realistic 8^)
                if step != self.y:
                    mc.setBlocks(stepx + 3, self.y, self.z + self.zlength - 1, stepx + 3, step - 1, self.z + self.zlength - 1, stonebrick)

                #increase the self.z and self.y value by one for each loop
                step = step + 1
                stepx = stepx + 1

        else:

            #building stairs up until the second floor is built
            while step <= (self.y + self.height):

                #placement of steps
                mc.setBlock(self.x + 2, step, stepz + 3, stonebrick_stair, 2)
                #clearing blocks above steps so players can walk their, incase walls are built over the stairs
                mc.setBlocks(self.x + 2, step + 1, stepz + 3, self.x + 2, self.y + self.height + 2, stepz + 3,air)

                #adding support for the steps because even though gravity exists we need our designs to be realistic 8^)
                if step != self.y:
                    mc.setBlocks(self.x + 2, self.y, stepz + 3, self.x + 2, step - 1, stepz + 3, stonebrick)

                #increase the self.z and self.y value by one for each loop
                step = step + 1
                stepz = stepz + 1

    #function for splitting a floor into rooms
    def build_room(self, xcoord, zcoord, ycoord, length, width):
        
        #Setting minimum size for when new room can be made
        if width * length < 30:
            mc.setBlock(xcoord + (length /2), ycoord + self.height, zcoord + (width /2), glowstone)
            return

        else:

            #Determines that if length is greater than width, wall will be built along the self.z axis
            if length > width:

                #assigns a variable with a random location of where the wall will go
                o = random.randrange(2, (length - 2))

                #builds the wall and creates hole for pathway
                mc.setBlocks(xcoord + o, ycoord, zcoord, xcoord + o, ycoord + self.height - 1, zcoord + width - 1, style[self.style_type]["wall"])
                mc.setBlocks(xcoord + o, ycoord, zcoord, xcoord + o, ycoord + 1, zcoord, air)

                #place random room decoration
                sleep(.5)
                decor.Room(xcoord + o, ycoord, zcoord, length-o, width)
                
                #calls self again with the 2 split rooms as new parameters
                self.build_room(xcoord, zcoord, ycoord, o, width)
                self.build_room(xcoord + o + 1, zcoord, ycoord, length - o - 1, width)

                return

            #Determines that if width is greater than or equal to length, wall will be built along the self.x axis
            else:

                #assigns a variable with a random location of where the wall will go
                o = random.randrange(2, (width - 2))

                #builds the wall and creates hole for pathway
                mc.setBlocks(xcoord, ycoord, zcoord + o, xcoord + length -1, ycoord + self.height - 1, zcoord + o, style[self.style_type]["wall"])
                mc.setBlocks(xcoord + 1, ycoord, zcoord + o, xcoord + 1, ycoord + 1, zcoord + o, air)

                sleep(.5)
                decor.Room(xcoord + o, ycoord, zcoord, length-o, width)

                #calls self again with the 2 split rooms as new parameters
                self.build_room(xcoord, zcoord, ycoord, length, o)
                self.build_room(xcoord, zcoord + o + 1, ycoord, length, width - o - 1)

                return

    def build_story(self, level_height, level):

        #Wall Placement
        mc.setBlocks(self.x + 1, level_height, self.z + 1 , self.x + self.xlength, level_height + self.height, self.z + self.zlength, style[self.style_type]["wall"])
        mc.setBlocks(self.x + 2, level_height, self.z + 2 , self.x + self.xlength - 1, level_height + self.height -1, self.z + self.zlength - 1, air)

        #creating border of logs around the base of the house
        mc.setBlocks(self.x + 1, level_height - 1, self.z + 1 , self.x + self.xlength, level_height - 1, self.z + 1, style[self.style_type]["pillar"])
        mc.setBlocks(self.x + self.xlength, level_height - 1, self.z + 1, self.x + self.xlength, level_height - 1, self.z + self.zlength, style[self.style_type]["pillar"])
        mc.setBlocks(self.x + 1, level_height - 1, self.z + 1, self.x + 1, level_height - 1, self.z + self.zlength, style[self.style_type]["pillar"])
        mc.setBlocks(self.x + 1, level_height - 1, self.z + self.zlength, self.x + self.xlength, level_height - 1, self.z + self.zlength, style[self.style_type]["pillar"])

        #Window Placement
        mc.setBlocks(self.x + 3 , level_height + 1 , self.z + 1, self.x + self.xlength -2, level_height + (self.height - 2), self.z + 1, glass)
        mc.setBlocks(self.x + self.xlength, level_height + 1 , self.z + 3, self.x + self.xlength, level_height + (self.height - 2), self.z + self.zlength -2, glass)
        mc.setBlocks(self.x + 1, level_height + 1 , self.z + 3, self.x + 1, level_height + (self.height - 2), self.z + self.zlength -2, glass)
        mc.setBlocks(self.x + 3, level_height + 1, self.z + self.zlength, self.x + self.xlength -2, level_height + (self.height - 2), self.z + self.zlength, glass)

        #Door Placement
        if level == 0:
            
            #Manually making if statement for door placement of each direction :(
            if self.direction == "South":
                mc.setBlock(self.x + 1 + (self.xlength // 2), level_height + 1, self.z + 1, door, 10)
                mc.setBlock(self.x + 1 + (self.xlength // 2), level_height, self.z + 1, door, 1)
                mc.setBlocks(self.x + (self.xlength // 2), level_height + 1, self.z + 1, self.x + (self.xlength // 2), level_height + (self.height - 2), self.z + 1, style[self.style_type]["wall"])
                mc.setBlocks(self.x + 2 + (self.xlength // 2), level_height + 1, self.z + 1, self.x + 2 + (self.xlength // 2), level_height + (self.height - 2), self.z + 1, style[self.style_type]["wall"])
                if self.height == 4:
                    mc.setBlock(self.x + 1 + (self.xlength // 2), level_height + 2, self.z + 1, style[self.style_type]["wall"])
            
            if self.direction == "North":
                mc.setBlock(self.x + 1 + (self.xlength // 2), level_height + 1, self.z + self.zlength, door, 9)
                mc.setBlock(self.x + 1 + (self.xlength // 2), level_height, self.z + self.zlength, door, 0)
                mc.setBlocks(self.x + (self.xlength // 2), level_height + 1, self.z + self.zlength, self.x + (self.xlength // 2), level_height + (self.height - 2), self.z + self.zlength, style[self.style_type]["wall"])
                mc.setBlocks(self.x + 2 + (self.xlength // 2), level_height + 1, self.z + self.zlength, self.x + 2 + (self.xlength // 2), level_height + (self.height - 2), self.z + self.zlength, style[self.style_type]["wall"])
                
                if self.height == 4:
                    mc.setBlock(self.x + 1 + (self.xlength // 2), level_height + 2, self.z + self.zlength, style[self.style_type]["wall"])

            if self.direction == "West":
                mc.setBlock(self.x + (self.xlength), level_height + 1, self.z + (self.zlength // 2) + 1, door, 12)
                mc.setBlock(self.x + (self.xlength), level_height, self.z + (self.zlength // 2) + 1, door, 3)
                mc.setBlocks(self.x + (self.xlength), level_height + 1, self.z + (self.zlength // 2) + 2, self.x + (self.xlength), level_height + (self.height - 2), self.z + (self.zlength // 2) + 2, style[self.style_type]["wall"])
                mc.setBlocks(self.x + (self.xlength), level_height + 1, self.z + (self.zlength // 2), self.x + (self.xlength), level_height + (self.height - 2), self.z + (self.zlength // 2), style[self.style_type]["wall"])
                if self.height == 4:
                    mc.setBlock(self.x + self.xlength, level_height + 2, self.z + (self.zlength // 2) + 1, style[self.style_type]["wall"])

            if self.direction == "East":
                mc.setBlock(self.x + 1, level_height + 1, self.z + (self.zlength // 2) + 1, door, 14)
                mc.setBlock(self.x + 1, level_height, self.z + (self.zlength // 2) + 1, door, 5)
                mc.setBlocks(self.x + 1, level_height + 1, self.z + (self.zlength // 2) + 2, self.x + 1, level_height + (self.height - 2), self.z + (self.zlength // 2) + 2, style[self.style_type]["wall"])
                mc.setBlocks(self.x + 1, level_height + 1, self.z + (self.zlength // 2), self.x + 1, level_height + (self.height - 2), self.z + (self.zlength // 2), style[self.style_type]["wall"])
                if self.height == 4:
                    mc.setBlock(self.x + 1, level_height + 2, self.z + (self.zlength // 2) + 1, style[self.style_type]["wall"])
            

        # Roof Placement
        if level + 1 >= self.story:
            roof(self.x, level_height+self.height, self.z,
                 self.xlength, self.zlength, style[self.style_type]["roof_tile"], style[self.style_type]["pillar"], style[self.style_type]["wall"], self.direction)
           
        #Floor Placement
        mc.setBlocks(self.x + 2, level_height - 1, self.z + 2, self.x + self.xlength - 1, level_height - 1, self.z + self.zlength - 1, terracotta, style[self.style_type]["floor"])

        #pillar placement
        mc.setBlocks(self.x + 1, level_height - 1, self.z + 1, self.x + 1, level_height + self.height, self.z + 1, style[self.style_type]["pillar"])
        mc.setBlocks(self.x + self.xlength, level_height - 1, self.z + self.zlength, self.x + self.xlength, level_height + self.height, self.z + self.zlength, style[self.style_type]["pillar"])
        mc.setBlocks(self.x + 1, level_height - 1, self.z + self.zlength, self.x + 1, level_height + self.height, self.z + self.zlength, style[self.style_type]["pillar"])
        mc.setBlocks(self.x + self.xlength, level_height - 1, self.z + 1, self.x + self.xlength, level_height + self.height, self.z + 1, style[self.style_type]["pillar"])
    
    def build_house(self):
        #created variable for self.y value of each self.story
        h = self.y

        #created this loop for if I wanted to add more stories
        for i in range(self.story): 
            self.build_story(h + (i * self.height), i)    
            h += 1

        h = self.y
        for i in range(self.story):    
            self.build_room(self.x + 2, self.z + 2, h + (i * self.height), self.xlength - 2, self.zlength - 2)
            h += 1

        #These statements are used to make sure no walls are blocking the entry to the house
        if self.direction == "East":
            mc.setBlocks(self.x + 2, self.y , self.z + (self.zlength // 2) + 1, self.x + 2, self.y + 1, self.z + (self.zlength // 2) + 1, air)

        elif self.direction == "West":
            mc.setBlocks(self.x + (self.xlength) - 1, self.y ,self.z + (self.zlength // 2) + 1, self.x + (self.xlength) - 1, self.y + 1, self.z + (self.zlength // 2) + 1, air)

        elif self.direction == "North":
            mc.setBlocks(self.x + 1 + (self.xlength // 2), self.y , self.z + self.zlength - 1, self.x + 1 + (self.xlength // 2), self.y + 1, self.z + self.zlength - 1, air)

        elif self.direction == "South":
            mc.setBlocks(self.x + 1 + (self.xlength // 2), self.y , self.z + 2, self.x + 1 + (self.xlength // 2), self.y + 1, self.z + 2, air)

        #checks if there is a second self.story and builds stairs if there is
        if self.story == 2:
            self.build_stairs()

        self.build_deck()

    def build_deck(self):
        backyard(self.x, self.y, self.z, self.xlength,
                self.zlength, self.direction)

    def get_dimensions(self):
        '''returns all dimensions and coords in the order of x,y,z,xlenght,zlength,direction'''
        #house_coords = round(self.x -2), round(self.z -2) , round(self.x + self.xlength + 3), round(self.z + self.zlength + 3)
        house_coords = (self.x -4), (self.z -4) , (self.x + self.xlength + 5), (self.z + self.zlength + 5)
        return list(house_coords)

