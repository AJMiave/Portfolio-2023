from mcpi.minecraft import Minecraft
import time
import random
from mcpi import block
from decor import Decor

mc = Minecraft.create()

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


#Dictionary for what style the house will be
style = {
    1: {"floor" : 7, "wall" : stonebrick, "pillar" : log.withData(1), "roof" : wood_slab},
    2: {"floor" : 9, "wall" : planks, "pillar" : log, "roof" : brick}
}

class House():

    def __init__(self, story, xlength, zlength, height, x, y, z, direction):
        
        self.style_type = random.randint(1,2)

        self.direction = direction

        self.xlength = xlength
        self.zlength = zlength
        self.height = height
        self.story = story
        self.y = y
        
        #Changed values for place where house will be build as we want the front door to be at the end of the path. This allows houses to have correct rotation and orientation
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

        if self.direction == "East":
            step = self.y
            stepx = self.x

            #building stairs up until the second floor is built
            while step <= (self.y + self.height):

                #placement of steps
                mc.setBlock(stepx + 3, step, self.z + self.zlength - 1, stonebrick_stair, 0)
                #clearing blocks above steps so players can walk their, incase walls are built over the stairs
                mc.setBlocks(stepx + 3, step + 1, self.z + self.zlength - 1, stepx + 3, self.y + self.height + 2, self.z + self.zlength - 1, air)
                time.sleep(.2)

                #adding support for the steps because even though gravity exists we need our designs to be realistic 8^)
                if step != self.y:
                    mc.setBlocks(stepx + 3, self.y, self.z + self.zlength - 1, stepx + 3, step - 1, self.z + self.zlength - 1, stonebrick)
                    time.sleep(.2)

                #increase the self.z and self.y value by one for each loop
                step = step + 1
                stepx = stepx + 1

        else:
            #assigning variables so previous coordinates arent effected
            step = self.y
            stepz = self.z

            #building stairs up until the second floor is built
            while step <= (self.y + self.height):

                #placement of steps
                mc.setBlock(self.x + 2, step, stepz + 3, stonebrick_stair, 2)
                #clearing blocks above steps so players can walk their, incase walls are built over the stairs
                mc.setBlocks(self.x + 2, step + 1, stepz + 3, self.x + 2, self.y + self.height + 2, stepz + 3,air)
                time.sleep(.2)

                #adding support for the steps because even though gravity exists we need our designs to be realistic 8^)
                if step != self.y:
                    mc.setBlocks(self.x + 2, self.y, stepz + 3, self.x + 2, step - 1, stepz + 3, stonebrick)
                    time.sleep(.2)

                #increase the self.z and self.y value by one for each loop
                step = step + 1
                stepz = stepz + 1

    #function for splitting a floor into rooms
    def build_room(self, xcoord, zcoord, ycoord, length, width):

        #Setting minimum size for when new room can be made
        if width * length < 30:
            return

        else:

            #Determines that if length is greater than width, wall will be built along the self.z axis
            if length > width:

                #assigns a variable with a random location of where the wall will go
                o = random.randrange(2, (length - 2))

                #builds the wall and creates hole for pathway
                mc.setBlocks(xcoord + o, ycoord, zcoord, xcoord + o, ycoord + self.height - 1, zcoord + width - 1, style[self.style_type]["wall"])
                mc.setBlocks(xcoord + o, ycoord, zcoord, xcoord + o, ycoord + 1, zcoord, air)
                time.sleep(.2)
                
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
                time.sleep(.2)

                #calls self again with the 2 split rooms as new parameters
                self.build_room(xcoord, zcoord, ycoord, length, o)
                self.build_room(xcoord, zcoord + o + 1, ycoord, length, width - o - 1)

                return

    def build_story(self, level_height, level):

        #Wall Placement
        mc.setBlocks(self.x + 1, level_height, self.z + 1 , self.x + self.xlength, level_height + self.height, self.z + self.zlength, style[self.style_type]["wall"])
        mc.setBlocks(self.x + 2, level_height, self.z + 2 , self.x + self.xlength - 1, level_height + self.height -1, self.z + self.zlength - 1, air)
        time.sleep(.2)

        #creating border of logs around the base of the house
        mc.setBlocks(self.x + 1, level_height - 1, self.z + 1 , self.x + self.xlength, level_height - 1, self.z + 1, style[self.style_type]["pillar"])
        mc.setBlocks(self.x + self.xlength, level_height - 1, self.z + 1, self.x + self.xlength, level_height - 1, self.z + self.zlength, style[self.style_type]["pillar"])
        mc.setBlocks(self.x + 1, level_height - 1, self.z + 1, self.x + 1, level_height - 1, self.z + self.zlength, style[self.style_type]["pillar"])
        mc.setBlocks(self.x + 1, level_height - 1, self.z + self.zlength, self.x + self.xlength, level_height - 1, self.z + self.zlength, style[self.style_type]["pillar"])
        time.sleep(.2)

        #Window Placement
        mc.setBlocks(self.x + 3 , level_height + 1 , self.z + 1, self.x + self.xlength -2, level_height + (self.height - 2), self.z + 1, glass)
        mc.setBlocks(self.x + self.xlength, level_height + 1 , self.z + 3, self.x + self.xlength, level_height + (self.height - 2), self.z + self.zlength -2, glass)
        mc.setBlocks(self.x + 1, level_height + 1 , self.z + 3, self.x + 1, level_height + (self.height - 2), self.z + self.zlength -2, glass)
        mc.setBlocks(self.x + 3, level_height + 1, self.z + self.zlength, self.x + self.xlength -2, level_height + (self.height - 2), self.z + self.zlength, glass)
        time.sleep(.2)

        #Door Placement
        if level == 0:

            if self.direction == "South":
                mc.setBlock(self.x + 1 + (self.xlength // 2), level_height + 1, self.z + 1, door, 10)
                mc.setBlock(self.x + 1 + (self.xlength // 2), level_height, self.z + 1, door, 1)
                time.sleep(.2)
                mc.setBlocks(self.x + (self.xlength // 2), level_height + 1, self.z + 1, self.x + (self.xlength // 2), level_height + (self.height - 2), self.z + 1, style[self.style_type]["wall"])
                mc.setBlocks(self.x + 2 + (self.xlength // 2), level_height + 1, self.z + 1, self.x + 2 + (self.xlength // 2), level_height + (self.height - 2), self.z + 1, style[self.style_type]["wall"])
                if self.height == 4:
                    mc.setBlock(self.x + 1 + (self.xlength // 2), level_height + 2, self.z + 1, style[self.style_type]["wall"])
                time.sleep(.2)
            
            if self.direction == "North":
                mc.setBlock(self.x + 1 + (self.xlength // 2), level_height + 1, self.z + self.zlength, door, 9)
                mc.setBlock(self.x + 1 + (self.xlength // 2), level_height, self.z + self.zlength, door, 0)
                time.sleep(.2)
                mc.setBlocks(self.x + (self.xlength // 2), level_height + 1, self.z + self.zlength, self.x + (self.xlength // 2), level_height + (self.height - 2), self.z + self.zlength, style[self.style_type]["wall"])
                mc.setBlocks(self.x + 2 + (self.xlength // 2), level_height + 1, self.z + self.zlength, self.x + 2 + (self.xlength // 2), level_height + (self.height - 2), self.z + self.zlength, style[self.style_type]["wall"])
                
                if self.height == 4:
                    mc.setBlock(self.x + 1 + (self.xlength // 2), level_height + 2, self.z + self.zlength, style[self.style_type]["wall"])
                time.sleep(.2)

            if self.direction == "West":
                mc.setBlock(self.x + (self.xlength), level_height + 1, self.z + (self.zlength // 2) + 1, door, 12)
                mc.setBlock(self.x + (self.xlength), level_height, self.z + (self.zlength // 2) + 1, door, 3)
                time.sleep(.2)
                mc.setBlocks(self.x + (self.xlength), level_height + 1, self.z + (self.zlength // 2) + 2, self.x + (self.xlength), level_height + (self.height - 2), self.z + (self.zlength // 2) + 2, style[self.style_type]["wall"])
                mc.setBlocks(self.x + (self.xlength), level_height + 1, self.z + (self.zlength // 2), self.x + (self.xlength), level_height + (self.height - 2), self.z + (self.zlength // 2), style[self.style_type]["wall"])
                if self.height == 4:
                    mc.setBlock(self.x + self.xlength, level_height + 2, self.z + (self.zlength // 2) + 1, style[self.style_type]["wall"])
                time.sleep(.2)

            if self.direction == "East":
                mc.setBlock(self.x + 1, level_height + 1, self.z + (self.zlength // 2) + 1, door, 14)
                mc.setBlock(self.x + 1, level_height, self.z + (self.zlength // 2) + 1, door, 5)
                time.sleep(.2)
                mc.setBlocks(self.x + 1, level_height + 1, self.z + (self.zlength // 2) + 2, self.x + 1, level_height + (self.height - 2), self.z + (self.zlength // 2) + 2, style[self.style_type]["wall"])
                mc.setBlocks(self.x + 1, level_height + 1, self.z + (self.zlength // 2), self.x + 1, level_height + (self.height - 2), self.z + (self.zlength // 2), style[self.style_type]["wall"])
                if self.height == 4:
                    mc.setBlock(self.x + 1, level_height + 2, self.z + (self.zlength // 2) + 1, style[self.style_type]["wall"])
                time.sleep(.2)
            

        # Roof Placement
        if level + 1 >= self.story:
            mc.setBlocks(self.x + 1, level_height + self.height, self.z + 1, self.x + self.xlength,
                         level_height + self.height, self.z + self.zlength, style[self.style_type]["pillar"])
            time.sleep(.2)
            mc.setBlocks(self.x, level_height + self.height + 1, self.z, self.x + self.xlength + 1,
                         level_height + self.height + 1, self.z + self.zlength + 1, style[self.style_type]["roof"])
            time.sleep(.2)

            for i in range(3):
                # side 1
                mc.setBlocks(self.x-1+i, level_height+self.height+1+i, self.z-1+i, self.x+self.xlength+2-i,
                             level_height + self.height+1+i, self.z - 1+i, block.STAIRS_SANDSTONE.withData(2))

                # side 2
                mc.setBlocks(self.x+self.xlength+2-i, level_height+self.height+1+i, self.z-1+i, self.x+self.xlength+2-i,
                             level_height + self.height+1+i, self.z+self.zlength+2-i, block.STAIRS_SANDSTONE.withData(1))

                # side 3
                mc.setBlocks(self.x+self.xlength+1-i,
                             level_height + self.height+1+i, self.z+self.zlength+2-i, self.x-1+i,
                             level_height + self.height+1+i, self.z+self.zlength+2-i, block.STAIRS_SANDSTONE.withData(3))

                # side 4
                mc.setBlocks(self.x-1+i,
                             level_height + self.height+1+i, self.z+self.zlength+2-i, self.x-1+i,
                             level_height + self.height+1+i, self.z-1+i, block.STAIRS_SANDSTONE.withData(0))
                time.sleep(.2)

            # fill in the roof
            mc.setBlocks(self.x+2, level_height+self.height+3, self.z+2, self.x+self.xlength-1,
                         level_height+self.height+3, self.z+self.zlength-1, block.GLOWSTONE_BLOCK)
            time.sleep(.2)

            # chimney
            mc.setBlocks(self.x+3, level_height+self.height+4, self.z+3,
                         self.x+5, level_height+self.height+5, self.z+5, style[self.style_type]["wall"])
            time.sleep(.2)

            mc.setBlocks(self.x+4, level_height +
                         self.height+4, self.z+4, self.x+4, level_height +
                         self.height+5, self.z+4, block.TORCH)
            time.sleep(.2)

        #Floor Placement
        mc.setBlocks(self.x + 2, level_height - 1, self.z + 2, self.x + self.xlength - 1, level_height - 1, self.z + self.zlength - 1, terracotta, style[self.style_type]["floor"])
        time.sleep(.2)

        #pillar placement
        mc.setBlocks(self.x + 1, level_height - 1, self.z + 1, self.x + 1, level_height + self.height, self.z + 1, style[self.style_type]["pillar"])
        mc.setBlocks(self.x + self.xlength, level_height - 1, self.z + self.zlength, self.x + self.xlength, level_height + self.height, self.z + self.zlength, style[self.style_type]["pillar"])
        mc.setBlocks(self.x + 1, level_height - 1, self.z + self.zlength, self.x + 1, level_height + self.height, self.z + self.zlength, style[self.style_type]["pillar"])
        mc.setBlocks(self.x + self.xlength, level_height - 1, self.z + 1, self.x + self.xlength, level_height + self.height, self.z + 1, style[self.style_type]["pillar"])
        time.sleep(.2)

    def build_house(self):
        #created variable for self.y value of each self.story
        h = self.y

        #created this loop for if I wanted to add more stories
        for i in range(self.story): 
            self.build_story(h + (i * self.height), i)    
            self.build_room(self.x + 2, self.z + 2, h + (i * self.height), self.xlength - 2, self.zlength - 2)
            time.sleep(.2)
            h += 1

        #These statements are used to make sure no walls are blocking the entry to the house. South is not needed as the walls which would block it have there gap there already
        if self.direction == "East":
            mc.setBlocks(self.x + 2, self.y , self.z + (self.zlength // 2) + 1, self.x + 2, self.y + 1, self.z + (self.zlength // 2) + 1, air)
            time.sleep(.2)

        elif self.direction == "West":
            mc.setBlocks(self.x + (self.xlength) - 1, self.y ,self.z + (self.zlength // 2) + 1, self.x + (self.xlength) - 1, self.y + 1, self.z + (self.zlength // 2) + 1, air)
            time.sleep(.2)

        elif self.direction == "North":
            mc.setBlocks(self.x + 1 + (self.xlength // 2), self.y , self.z + self.zlength - 1, self.x + 1 + (self.xlength // 2), self.y + 1, self.z + self.zlength - 1, air)
            time.sleep(.2)

        #checks if there is a second self.story and builds stairs if there is
        if self.story == 2:
            self.build_stairs()

        self.build_deck()

    # TODO: add some furniture, paintings
    def build_deck(self):
        torch = block.TORCH
        # fence 3 blocks around house perimeter
        # front fence
        # left side
        mc.setBlocks(self.x + self.xlength+3, self.y, self.z-2, self.x -
                     2, self.y, self.z-2, block.FENCE)
        mc.setBlocks(self.x+self.xlength+3, self.y, self.z-2, self.x+self.xlength +
                     3, self.y, self.z+self.zlength+3, block.FENCE)
        mc.setBlocks(self.x+self.xlength+3, self.y, self.z+self.zlength+3, self.x -
                     2, self.y, self.z+self.zlength+3, block.FENCE)
        mc.setBlocks(self.x-2, self.y, self.z+self.zlength+3, self.x-2, self.y, self.z-2, block.FENCE)
        time.sleep(.2)

        # wood pillars for every corner
        mc.setBlock(self.x-2, self.y, self.z-2, log)
        mc.setBlock(self.x+self.xlength+3, self.y, self.z-2, log)
        mc.setBlock(self.x-2, self.y, self.z+self.zlength+3, log)
        mc.setBlock(self.x+self.xlength+3, self.y, self.z+self.zlength+3, log)
        time.sleep(.2)

        # supposed to be lanterns but torches for now
        mc.setBlock(self.x-2, self.y+1, self.z-2, torch.withData(5))
        mc.setBlock(self.x+self.xlength+3, self.y+1, self.z-2, torch.withData(5))
        mc.setBlock(self.x-2, self.y+1, self.z+self.zlength+3, torch.withData(5))
        mc.setBlock(self.x+self.xlength+3, self.y+1, self.z+self.zlength+3, torch.withData(5))
        time.sleep(.2)

        if self.direction == "South":
            mc.setBlock(self.x + 1 + (self.xlength // 2), self.y, self.z -2, gate, 2)
            time.sleep(.2)
        if self.direction == "North":
            mc.setBlock(self.x + 1 + (self.xlength // 2), self.y, self.z + self.zlength + 3, gate)
            time.sleep(.2)
        if self.direction == "West":
            mc.setBlock(self.x + self.xlength + 3, self.y, self.z + (self.zlength // 2) + 1, gate, 3)
            time.sleep(.2)
        if self.direction == "East":
            mc.setBlock(self.x -2, self.y, self.z + (self.zlength // 2) + 1, gate, 1)
            time.sleep(.2)

        # flowers
        yellow_flower = block.FLOWER_YELLOW
        cyan_flower = block.FLOWER_CYAN
        mc.setBlock(self.x-1, self.y, self.z-1, yellow_flower)

    def get_decorations(self):
        # front door position
        front_door = (self.x + 1 + (self.xlength // 2),
                      self.y, self.z + 1, door, 1)
        decor = Decor(self.x, self.y, self.z, self.xlength,
                      self.zlength, front_door)

    def get_dimensions(self):
        '''returns all dimensions and coords in the order of x,y,z,xlenght,zlength,direction'''
        return self.x,self.y,self.z,self.xlength,self.zlength,self.direction