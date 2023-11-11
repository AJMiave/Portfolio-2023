from ast import And
from random import randint
from mcpi.minecraft import Minecraft
import time
from statistics import mode
from mcpi import block
import blocks
from Houses import House

mc = Minecraft.create()



class Terraform:

    def __init__(self,x,y,z,length, width,direction):
        ### DOOR COORDS
        self.doorX = x
        self.doorY = y 
        self.doorZ = z

        ### gets half the length and width of the house (as the x,y,z is the middle edge of the plot)
        self.halfLength = int(length / 2) + 1
        self.halfWidth = int(width / 2) + 1

        
        ### sets the x y z coords in the middle based on the direction of the house 
        if direction == 'North':
            self.z = z - self.halfWidth + 4
            self.x = x
            self.y = y 
        elif direction == 'South':
            self.z = z + self.halfWidth - 4
            self.x = x
            self.y = y 
        elif direction == 'West':
            self.z = z
            self.x = x - self.halfLength + 4
            self.y = y  
        elif direction == 'East':
            self.z = z
            self.x = x + self.halfLength - 4
            self.y = y 

        ### lists to store heights and blocks of the plot
        self.heights = []
        self.blocks = []

        ### iterates through every x and z in the plot
        ### gets the height and block data of each block in the area and appending to the lists
        ### has a stride of 2 to reduce runtime
        for i in range(int(self.x)-self.halfLength, int(self.x)+(self.halfLength),2):
            for j in range(int(self.z)-self.halfWidth, int(self.z)+(self.halfWidth),2):
                self.heights.append(mc.getHeight(i,j))
                self.blocks.append(mc.getBlockWithData(i,mc.getHeight(i,j),j))

    def blockChoice(self):
        ### function to choose the block to build with based on the most frequent block in the plot, given that theyre valid
        
        ### list of valid blocks to build with
        validBlocks = [
            blocks.GRASS, 
            blocks.SAND, 
            blocks.RED_SAND, 
            blocks.STAINED_TERRACOTTA.withData(0),
            blocks.STAINED_TERRACOTTA.withData(1),
            blocks.STAINED_TERRACOTTA.withData(8),
            blocks.STAINED_TERRACOTTA.withData(12),
            blocks.TERRACOTTA.withData(0)
            ]
        
        ### returns the most common block if valid
        freqblock = mode(self.blocks)
        if freqblock in validBlocks:
            return freqblock

        ### else searches for a valid block in the area
        for block in self.blocks:
            if block in validBlocks:
                return block

        ### else, worst case, returns grass
        return blocks.GRASS

    def logging(self):
        ### function to remove a tree or mushroom are the coords the house door is placed on
        
        ### list of all tree blocks and their types
        treeBlocks = [
            blocks.WOOD.withData(0), 
            blocks.WOOD.withData(1), 
            blocks.WOOD.withData(2), 
            blocks.WOOD.withData(3), 
            blocks.WOOD.withData(4), 
            blocks.WOOD.withData(5), 
            blocks.WOOD.withData(6), 
            blocks.WOOD.withData(7), 
            blocks.WOOD.withData(8), 
            blocks.WOOD.withData(9), 
            blocks.WOOD.withData(10), 
            blocks.WOOD.withData(11), 
            blocks.WOOD2.withData(0), 
            blocks.WOOD2.withData(1), 
            blocks.WOOD2.withData(4), 
            blocks.WOOD2.withData(5), 
            blocks.WOOD2.withData(8), 
            blocks.WOOD2.withData(9), 
            blocks.LEAVES.withData(0), 
            blocks.LEAVES.withData(1), 
            blocks.LEAVES.withData(2), 
            blocks.LEAVES.withData(3), 
            blocks.LEAVES2.withData(0),
            blocks.LEAVES2.withData(1),
            blocks.MUSHROOM_BLOCK_BROWN.withData(0),
            blocks.MUSHROOM_BLOCK_BROWN.withData(1),
            blocks.MUSHROOM_BLOCK_BROWN.withData(2),
            blocks.MUSHROOM_BLOCK_BROWN.withData(3),
            blocks.MUSHROOM_BLOCK_BROWN.withData(4),
            blocks.MUSHROOM_BLOCK_BROWN.withData(5),
            blocks.MUSHROOM_BLOCK_BROWN.withData(6),
            blocks.MUSHROOM_BLOCK_BROWN.withData(7),
            blocks.MUSHROOM_BLOCK_BROWN.withData(8),
            blocks.MUSHROOM_BLOCK_BROWN.withData(9),
            blocks.MUSHROOM_BLOCK_BROWN.withData(10),
            blocks.MUSHROOM_BLOCK_BROWN.withData(14),
            blocks.MUSHROOM_BLOCK_BROWN.withData(15),
            blocks.MUSHROOM_BLOCK_RED.withData(0),
            blocks.MUSHROOM_BLOCK_RED.withData(1),
            blocks.MUSHROOM_BLOCK_RED.withData(2),
            blocks.MUSHROOM_BLOCK_RED.withData(3),
            blocks.MUSHROOM_BLOCK_RED.withData(4),
            blocks.MUSHROOM_BLOCK_RED.withData(5),
            blocks.MUSHROOM_BLOCK_RED.withData(6),
            blocks.MUSHROOM_BLOCK_RED.withData(7),
            blocks.MUSHROOM_BLOCK_RED.withData(8),
            blocks.MUSHROOM_BLOCK_RED.withData(9)
            
            ]

        ### calculates the lowest y block to loop to
        lowest = int(self.y - min(self.heights))
        
        ### iterates through a 3x3 area from the lowest block to 2 blocks about the coords
        ### if the block is a tree block it sets it as air
        for h in range(int(self.y) - lowest, int(self.y + 2)):
            for i in range(int(self.doorX) - 3, int(self.doorX) + 3):
                for j in range(int(self.doorZ) - 3, int(self.doorZ) + 3):
                    if mc.getBlockWithData(i,h,j) in treeBlocks:
                        mc.setBlock(i,h,j, blocks.AIR)
                        
        ### reassigns the y coords to the new highest block with the tree removed
        self.doorY = mc.getHeight(self.doorX, self.doorZ)
        self.y = mc.getHeight(self.doorX, self.doorZ)
        ### returns new y level for village main
        return mc.getHeight(self.doorX, self.doorZ)

    def hillSteepness(self, blockDiff):
        ### function for calculating how steep the terraforming will be (i.e. if the plot is greater than 5 blocks above the lowest y level it builds 2 down)
        ### 1: builds 2 block, 2: builds 3 blocks, 3: builds 3 blocks
        if blockDiff > 12:
            return 3
        elif blockDiff > 8:
            return 2
        elif blockDiff > 5:
            return 1
        else:
            return 0
     
    def flattenPlot(self,block):
        ###function to flatten the land for the house to build on
         
        ### deck -> if the plot is a deck or land, count -> to count the number of water blocks
        deck = False
        count = 0
        
        ### list of all water blocks
        waterBlocks = [blocks.WATER, blocks.WATER_FLOWING, blocks.WATER_STATIONARY, blocks.AIR]
        
        ### if there is water blocks in the area and theyre greater than 3 blocks down, sets deck to true
        for blockTemp in self.blocks:
            if (blockTemp in waterBlocks) and 3 > (int(self.y - min(self.heights))):
                count +=1
                deck = True
        
        ### if there is less than 10 water block in the plot then  sets deck to false
        if count < 10:
            deck = False
                
        ### builds a plane 
        ### if deck true then builds the plot with wood planks
        if deck:
            mc.setBlocks(self.x-self.halfLength, self.y, self.z-self.halfWidth, self.x+self.halfLength, self.y, self.z+self.halfWidth, blocks.WOOD_PLANKS)
        else:
            mc.setBlocks(self.x-self.halfLength, self.y-1, self.z-self.halfWidth, self.x+self.halfLength, self.y-1, self.z+self.halfWidth, blocks.BARRIER)
            mc.setBlocks(self.x-self.halfLength, self.y, self.z-self.halfWidth, self.x+self.halfLength, self.y, self.z+self.halfWidth, block)

        ### checks each corner of the plot for wood planks, if so builds with logs all the way down to the lowest non water block
        deckY = self.y
        if mc.getBlockWithData(self.x+self.halfLength, deckY, self.z+self.halfWidth) == blocks.WOOD_PLANKS:
            mc.setBlock(self.x+self.halfLength, deckY, self.z+self.halfWidth, blocks.WOOD)
            deckY -= 1
            while mc.getBlockWithData(self.x+self.halfLength, deckY, self.z+self.halfWidth) in waterBlocks:
                mc.setBlock(self.x+self.halfLength, deckY, self.z+self.halfWidth, blocks.WOOD)
                deckY -= 1
        deckY = self.y
        
        if mc.getBlockWithData(self.x+self.halfLength, deckY, self.z-self.halfWidth) == blocks.WOOD_PLANKS:
            mc.setBlock(self.x+self.halfLength, deckY, self.z-self.halfWidth, blocks.WOOD)
            deckY -= 1
            while mc.getBlockWithData(self.x+self.halfLength, deckY, self.z-self.halfWidth) in waterBlocks:
                mc.setBlock(self.x+self.halfLength, deckY, self.z-self.halfWidth, blocks.WOOD)
                deckY -= 1
        deckY = self.y
        
        if mc.getBlockWithData(self.x-self.halfLength, deckY, self.z-self.halfWidth) == blocks.WOOD_PLANKS:
            mc.setBlock(self.x-self.halfLength, deckY, self.z-self.halfWidth, blocks.WOOD)
            deckY -= 1
            while mc.getBlockWithData(self.x-self.halfLength, deckY, self.z-self.halfWidth) in waterBlocks:
                mc.setBlock(self.x-self.halfLength, deckY, self.z-self.halfWidth, blocks.WOOD)
                deckY -= 1
        deckY = self.y
        
        if mc.getBlockWithData(self.x-self.halfLength, deckY, self.z+self.halfWidth) == blocks.WOOD_PLANKS:
            mc.setBlock(self.x-self.halfLength, deckY, self.z+self.halfWidth, blocks.WOOD)
            deckY -= 1
            while mc.getBlockWithData(self.x-self.halfLength, deckY, self.z+self.halfWidth) in waterBlocks:
                mc.setBlock(self.x-self.halfLength, deckY, self.z+self.halfWidth, blocks.WOOD)
                deckY -= 1
            
        ### clears all the blocks above the plot
        mc.setBlocks(self.x-self.halfLength, self.y+1, self.z-self.halfWidth, self.x+self.halfLength, self.y+100, self.z+self.halfWidth,blocks.AIR)

        ### returns if the plot is a deck
        return deck
   
    # def blockReplace(self, block, loops, height):
    #     bounds = loops 
    #     blocksToReplace = [
    #         blocks.STONE.withData(0),
    #         blocks.STONE.withData(1),
    #         blocks.STONE.withData(3),
    #         blocks.STONE.withData(5),
    #         blocks.DIRT,
    #         blocks.GRAVEL,
    #         blocks.SANDSTONE,
    #         blocks.COAL_ORE,
    #         blocks.IRON_ORE,
    #     ]
        
    #     for i in range(int(self.x)-self.halfLength - bounds - 1, int(self.x)+(self.halfLength) + bounds):
    #         for j in range(int(self.z)-self.halfWidth - bounds - 1, int(self.z)+(self.halfWidth) + bounds):
    #             if (i not in range(int(self.x)-self.halfLength - 1, int(self.x)+(self.halfLength))) or (j not in range(int(self.z)-self.halfWidth - 1, int(self.z)+(self.halfWidth))):
    #                 if mc.getBlockWithData(i, mc.getHeight(i,j), j) in blocksToReplace:
    #                     mc.setBlock(i, mc.getHeight(i,j), j, block)
    
    
    def declineLoops(self):
        ### function to calculate how far down to build to
        ### gets the lowest block in the plot
        lowest = int(self.y - min(self.heights))

        ### iterates through the plot plus the lowest(var) number
        ### appends the height of each plock to heights list
        for i in range(int(self.x)-self.halfLength - lowest - 1, int(self.x)+(self.halfLength) + lowest):
            for j in range(int(self.z)-self.halfWidth - lowest - 1, int(self.z)+(self.halfWidth) + lowest):
                if (i not in range(int(self.x)-self.halfLength - 1, int(self.x)+(self.halfLength))) or (j not in range(int(self.z)-self.halfWidth - 1, int(self.z)+(self.halfWidth))):
                    self.heights.append(mc.getHeight(i,j))
        
        ### returns new lowest height
        return int(self.y - min(self.heights))
        
        
    def hill(self):
        ### function for building a hill downwards to blend in with the environment
        
        ### assigns building block with the block choice funtion
        block = self.blockChoice()
        
        #calculates how far to build down based off the difference between the self.y height and the lowest block in the plot area using decline loops funtion
        lowest = self.declineLoops()

        ### calculates how steep to build with the hillsteepness function
        buildLength = self.hillSteepness(lowest)
        
        ### sets if the plot is a deck or not
        deck =self.flattenPlot(block)
        
        ### if not deck then build hill downwards
        ### each block has a barrier block placed beneath to prevent sand falling
        if deck == False:
            ### sets temporary variables to increment
            tempLength = self.halfLength
            tempWidth = self.halfWidth + 1
            tempy = self.y -1
            
            ### builds the z axis decline
            for i in range(lowest):
                mc.setBlocks(self.x-tempLength, tempy - 1, self.z+tempWidth,self.x+tempLength, tempy - buildLength - 1, self.z+tempWidth, blocks.BARRIER)
                mc.setBlocks(self.x-tempLength, tempy, self.z+tempWidth,self.x+tempLength, tempy - buildLength, self.z+tempWidth,block)
                mc.setBlocks(self.x-tempLength, tempy - 1, self.z-tempWidth,self.x+tempLength, tempy - buildLength - 1, self.z-tempWidth, blocks.BARRIER)
                mc.setBlocks(self.x-tempLength, tempy, self.z-tempWidth,self.x+tempLength, tempy - buildLength, self.z-tempWidth,block)
                #time.sleep(.1)
                tempWidth +=1
                tempy-= (1 + buildLength)

            ### sets temporary variables to increment
            tempLength += 1
            tempWidth = self.halfWidth
            tempy = self.y -1
            ### builds the x axis decline
            for i in range(lowest):
                mc.setBlocks(self.x-tempLength, tempy - 1 , self.z-tempWidth,self.x-tempLength, tempy - buildLength - 1, self.z+tempWidth,blocks.BARRIER)
                mc.setBlocks(self.x-tempLength, tempy, self.z-tempWidth,self.x-tempLength, tempy - buildLength, self.z+tempWidth,block)
                mc.setBlocks(self.x+tempLength, tempy - 1 , self.z-tempWidth,self.x+tempLength, tempy - buildLength - 1, self.z+tempWidth,blocks.BARRIER)
                mc.setBlocks(self.x+tempLength, tempy, self.z-tempWidth,self.x+tempLength, tempy - buildLength, self.z+tempWidth,block)
                #time.sleep(.1)
                tempLength +=1
                tempy-= (1 + buildLength)


            ### sets temporary variables to increment in loops
            tempH = 2
            tempIncrease = 1
            ### builds the corner declines by placing a block one more down and out
            for j in range(lowest):
                tempy = self.y - tempH
                tempLength = self.halfLength + tempIncrease
                tempWidth = self.halfWidth + 1
                for i in range(lowest):
                    mc.setBlocks(self.x-tempLength, tempy-1, self.z+tempWidth, self.x-tempLength, tempy - buildLength-1, self.z+tempWidth,blocks.BARRIER)
                    mc.setBlocks(self.x-tempLength, tempy, self.z+tempWidth, self.x-tempLength, tempy - buildLength, self.z+tempWidth,block)
                    mc.setBlocks(self.x+tempLength, tempy-1, self.z+tempWidth, self.x+tempLength, tempy - buildLength-1, self.z+tempWidth,blocks.BARRIER)
                    mc.setBlocks(self.x+tempLength, tempy, self.z+tempWidth, self.x+tempLength, tempy - buildLength, self.z+tempWidth,block)

                    mc.setBlocks(self.x-tempLength, tempy-1, self.z-tempWidth, self.x-tempLength, tempy - buildLength - 1, self.z-tempWidth,blocks.BARRIER)
                    mc.setBlocks(self.x-tempLength, tempy, self.z-tempWidth, self.x-tempLength, tempy - buildLength, self.z-tempWidth,block)
                    mc.setBlocks(self.x+tempLength, tempy-1, self.z-tempWidth, self.x+tempLength, tempy - buildLength - 1, self.z-tempWidth,blocks.BARRIER)
                    mc.setBlocks(self.x+tempLength, tempy, self.z-tempWidth, self.x+tempLength, tempy - buildLength, self.z-tempWidth,block)
                    #time.sleep(.1)
                    tempWidth +=1
                    tempy-= (1 + buildLength)
                tempH += (1 + buildLength)
                tempIncrease +=1

    def carve(self):
        ### function to carve out the plot area to blend in with the terrain
        
        ### set air block to build with
        air = blocks.AIR

        ### clears the blocks above the plot
        mc.setBlocks(self.x-self.halfLength, self.y+1, self.z-self.halfWidth, self.x+self.halfLength, self.y+100, self.z+self.halfWidth,air)

        #calculates how far to build down based off the difference between the highest block in the plot area and the y level
        highest = int(max(self.heights) - self.y)

        ### calculates how steep to carve up
        buildLength = self.hillSteepness(highest)

        ### sets temporary variables to increment
        tempLength = self.halfLength
        tempWidth = self.halfWidth + 1
        tempy = self.y + 1
        ### carves the z axis incline
        for i in range(highest):
            mc.setBlocks(self.x-tempLength, tempy, self.z+tempWidth,self.x+tempLength, 100, self.z+tempWidth,air)
            mc.setBlocks(self.x-tempLength, tempy, self.z-tempWidth,self.x+tempLength, 100, self.z-tempWidth,air)
            #time.sleep(.1)
            tempWidth +=1
            tempy+= (1 + buildLength)

        ### sets temporary variables to increment
        tempLength += 1
        tempWidth = self.halfWidth
        tempy = self.y + 1
        ### carves the x axis incline
        for i in range(highest):
            mc.setBlocks(self.x-tempLength, tempy, self.z-tempWidth,self.x-tempLength, 100, self.z+tempWidth,air)
            mc.setBlocks(self.x+tempLength, tempy, self.z-tempWidth,self.x+tempLength, 100, self.z+tempWidth,air)
            #time.sleep(.1)
            tempLength +=1
            tempy+= (1 + buildLength)


        ### sets temporary variables to increment in loops
        tempH = 2
        tempIncrease = 1
        ### carves corner inclnie
        for j in range(highest):
            tempy = self.y + tempH
            tempLength = self.halfLength + tempIncrease
            tempWidth = self.halfWidth + 1
            for i in range(highest):
                mc.setBlocks(self.x-tempLength, tempy, self.z+tempWidth,self.x+tempLength, 100, self.z+tempWidth,air)
                mc.setBlocks(self.x-tempLength, tempy, self.z-tempWidth ,self.x+tempLength, 100 , self.z-tempWidth,air)
                #time.sleep(.1)
                tempWidth +=1
                tempy+= (1 + buildLength)
            tempH += (1 + buildLength)
            tempIncrease +=1


### testing terraforming
# x,y,z = mc.player.getPos()
# direction = 'North'
# house = House(1, 11, 9, 4, x, y , z, direction)
# area = Terraform(x,y-1,z,0+6,0+6, direction)


# area.carve()
# area.hill()
# mc.postToChat('done')
# mc.postToChat(mc.getBlockWithData(x,y-1,z))
# print(mc.getBlockWithData(x,y-1,z))
# area.logging()
# # time.sleep(1)
# house.build_house()
