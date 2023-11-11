from tkinter import LEFT
from mcpi.minecraft import Minecraft
from time import sleep
import random
from mcpi import block
import math

roof = {
    block.STAIRS_NETHER_BRICK: block.NETHER_BRICK,
    block.STAIRS_WOOD: block.WOOD_PLANKS,
    block.STAIRS_SANDSTONE: block.SANDSTONE,
    block.Block(203): block.Block(201),
    block.Block(180): block.Block(179)

}

mc = Minecraft.create()

cyan_flower = block.FLOWER_CYAN
yellow_flower = block.FLOWER_YELLOW
brown_mushroom = block.MUSHROOM_BROWN
red_mushroom = block.MUSHROOM_RED
grass = block.GRASS
closed_trapdoor = block.TRAPDOOR.withData(4)
left_trapdoor = block.TRAPDOOR.withData(7)
right_trapdoor = block.TRAPDOOR.withData(6)
log = block.WOOD
torch = block.TORCH
gate = block.FENCE_GATE


'''Each class has at least 2 randomised aspects'''
class Room():
    def __init__(self, x, y, z, length, width):
        self.x = math.floor(x)
        self.x1 = math.floor(x+length-1)
        self.y = math.floor(y)
        self.z = math.floor(z+2)
        self.z1 = math.floor(z+width)
        self.length = length
        self.width = width
        self.xdoor = 0
        self.zdoor = 0
        self.room(self, self.x, self.y, self.length, self.width)

    def doorpos(self, x, z):
        self.xdoor = x
        self.zdoor = z

    def room(self, x, y, z, length, width):
        # dont build anything if the room is small
        if (length*width) < 10:
            return

        else:
            # randomly choosing room type
            rooms = [self.enchanting_room, self.cactus, self.bookshelf, self.brewing_stand]
            random.choice(rooms)()

            return

    def enchanting_room(self):
        # 2 blocks of enchanting table side by side
        mc.setBlock(self.x+1, self.y, self.z-1, block.Block(116))
        

    def brewing_stand(self):
        # a single brewing stand on top of obsidian
        mc.setBlock(self.x+1, self.y, self.z-1, block.Block(49))
        mc.setBlock(self.x+1, self.y+1, self.z-1, block.Block(117))
        # mc.setBlock(self.x+1, self.y+2, self.z-1, block.Block(50))

    def cactus(self):
        # cactus on top of bookshelf
        mc.setBlock(self.x+1, self.y, self.z-1, block.Block(47))
        mc.setBlock(self.x+1, self.y+1, self.z-1, block.Block(140))
        mc.setBlock(self.x+1, self.y+2, self.z-1, block.Block(50))

    def bookshelf(self):
        # 2 stack bookshelf
        mc.setBlock(self.x+1, self.y, self.z-1, block.Block(47))
        mc.setBlock(self.x+1, self.y+1, self.z-1, block.Block(47))
        mc.setBlock(self.x+1, self.y+2, self.z-1, block.Block(50))

    def plant(self):
        mc.setBlock(self.x+1, self.y, self.z-1, block.Block(47))
        mc.setBlock(self.x+1, self.y+1, self.z-1, block.Block(47))
        mc.setBlock(self.x+1, self.y+2, self.z-1, block.Block(50))


class villageDecor():
    # village decoration items
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def farm(self, x, y, z):
        # wood perimeter
        mc.setBlocks(x-1, y, z-1, x+5, y-1, z+5, block.WOOD)

        # farm with wheat seads planted
        mc.setBlocks(x, y, z, x+4, y, z+1, block.Block(60))
        mc.setBlocks(x, y+1, z, x+4, y+1, z+1, block.Block(59))
        mc.setBlocks(x, y, z+3, x+4, y, z+4, block.Block(60))
        mc.setBlocks(x, y+1, z+3, x+4, y+1, z+4, block.Block(59))

        mc.setBlocks(x, y, z+2, x+4, y, z+2, block.WATER)

    def well(self, x, y, z):
        mc.setBlocks(x, y, z, x+5, y, z+5, block.MOSS_STONE)
        mc.setBlocks(x+1, y+1, z+1,  x+4, y+1, z+4, block.MOSS_STONE)
        mc.setBlocks(x+1, y+5, z+1,  x+4, y+5, z+4, block.MOSS_STONE)

        mc.setBlocks(x+2, y+1, z+2, x+3, y+1, z+3, block.WATER)

        # fence
        mc.setBlocks(x+1, y+2, z+1, x+1, y+4, z+1, block.FENCE)
        mc.setBlocks(x+4, y+2, z+1, x+4, y+4, z+1, block.FENCE)
        mc.setBlocks(x+4, y+2, z+4, x+4, y+4, z+4, block.FENCE)
        mc.setBlocks(x+1, y+2, z+4, x+1, y+4, z+4, block.FENCE)

    def mushroom(self):
        pass

class backyard():
    def __init__(self, x, y, z, xlength, zlength, direction):
        # To change backyards
        self.x = x
        self.y = y
        self.z = z
        self.xlength = xlength
        self.zlength = zlength
        self.direction = direction
        backyard = [self.lightfence, self.fence, self.lanterns]
        random.choice(backyard)()
        # self.fence()
        # self.flowerbed()

    def lightfence(self):
        # fence 3 blocks around house perimeter
        # front fence
        # # left side
        mc.setBlocks(self.x + self.xlength+3, self.y, self.z-2, self.x -
                     2, self.y, self.z-2, block.FENCE)
        mc.setBlocks(self.x+self.xlength+3, self.y, self.z-2, self.x+self.xlength +
                     3, self.y, self.z+self.zlength+3, block.FENCE)
        mc.setBlocks(self.x+self.xlength+3, self.y, self.z+self.zlength+3, self.x -
                     2, self.y, self.z+self.zlength+3, block.FENCE)
        mc.setBlocks(self.x-2, self.y, self.z+self.zlength+3,
                     self.x-2, self.y, self.z-2, block.FENCE)

        '''lanterns every corner'''
        # corner 1
        mc.setBlocks(self.x-2, self.y+1, self.z-2, self.x -
                     2, self.y+4, self.z-2, block.FENCE)
        mc.setBlock(self.x - 1, self.y+4, self.z-2, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x - 3, self.y+4, self.z-2, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x - 2, self.y+4, self.z-1, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x - 2, self.y+4, self.z-3, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x - 2, self.y+5, self.z-2, block.GLOWSTONE_BLOCK)

        # corner 2
        mc.setBlocks(self.x+self.xlength+3, self.y+1, self.z-2,
                     self.x+self.xlength+3, self.y+4, self.z-2, block.FENCE)
        mc.setBlock(self.x+self.xlength+2, self.y+4,
                    self.z-2, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x+self.xlength+4, self.y+4,
                    self.z-2, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x+self.xlength+3, self.y+4,
                    self.z-1, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x+self.xlength+3, self.y+4,
                    self.z-3, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x+self.xlength+3, self.y+5,
                    self.z-2, block.GLOWSTONE_BLOCK)

        # corner 3
        mc.setBlocks(self.x-2, self.y+1, self.z+self.zlength+3,
                     self.x-2, self.y+4, self.z+self.zlength+3, block.FENCE)
        mc.setBlock(self.x-1, self.y+4, self.z +
                    self.zlength+3, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x-3, self.y+4, self.z +
                    self.zlength+3, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x-2, self.y+4, self.z +
                    self.zlength+2, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x-2, self.y+4, self.z +
                    self.zlength+4, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x-2, self.y+5, self.z +
                    self.zlength+3, block.GLOWSTONE_BLOCK)

        # corner 4
        mc.setBlocks(self.x+self.xlength+3, self.y+1, self.z+self.zlength+3,
                     self.x+self.xlength+3, self.y+4, self.z+self.zlength+3, block.FENCE)
        mc.setBlock(self.x+self.xlength+2, self.y+4, self.z +
                    self.zlength+3, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x+self.xlength+4, self.y+4, self.z +
                    self.zlength+3, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x+self.xlength+3, self.y+4, self.z +
                    self.zlength+2, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x+self.xlength+3, self.y+4, self.z +
                    self.zlength+4, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x+self.xlength+3, self.y+5, self.z +
                    self.zlength+3, block.GLOWSTONE_BLOCK)
                    
        # gates for the different door directions
        if self.direction == "South":
            mc.setBlock(self.x + 1 + (self.xlength // 2),
                        self.y, self.z - 2, gate.withData(2))
        if self.direction == "North":
            mc.setBlock(self.x + 1 + (self.xlength // 2),
                        self.y, self.z + self.zlength + 3, gate.withData(2))
        if self.direction == "West":
            mc.setBlock(self.x + self.xlength + 3, self.y,
                        self.z + (self.zlength // 2) + 1, gate.withData(3))
        if self.direction == "East":
            mc.setBlock(self.x - 2, self.y, self.z +
                        (self.zlength // 2) + 1, gate.withData(3))

    # def flowerbed(self):
    #     mc.setBlocks(x, y, z+3, x+1, y, z+3, block.DIRT)

    def fence(self):
        mc.setBlocks(self.x + self.xlength+3, self.y, self.z-2, self.x -
                     2, self.y, self.z-2, block.FENCE)
        mc.setBlocks(self.x+self.xlength+3, self.y, self.z-2, self.x+self.xlength +
                     3, self.y, self.z+self.zlength+3, block.FENCE)
        mc.setBlocks(self.x+self.xlength+3, self.y, self.z+self.zlength+3, self.x -
                     2, self.y, self.z+self.zlength+3, block.FENCE)
        mc.setBlocks(self.x-2, self.y, self.z+self.zlength+3,
                     self.x-2, self.y, self.z-2, block.FENCE)

        # gates for the different door directions
        if self.direction == "South":
            mc.setBlock(self.x + 1 + (self.xlength // 2),
                        self.y, self.z - 2, gate.withData(2))
        if self.direction == "North":
            mc.setBlock(self.x + 1 + (self.xlength // 2),
                        self.y, self.z + self.zlength + 3, gate.withData(2))
        if self.direction == "West":
            mc.setBlock(self.x + self.xlength + 3, self.y,
                        self.z + (self.zlength // 2) + 1, gate.withData(3))
        if self.direction == "East":
            mc.setBlock(self.x - 2, self.y, self.z +
                        (self.zlength // 2) + 1, gate.withData(3))

    def lanterns(self):
        # corner 1
        mc.setBlocks(self.x-2, self.y, self.z-2, self.x -
                     2, self.y+4, self.z-2, block.FENCE)
        mc.setBlock(self.x - 1, self.y+4, self.z-2, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x - 3, self.y+4, self.z-2, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x - 2, self.y+4, self.z-1, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x - 2, self.y+4, self.z-3, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x - 2, self.y+5, self.z-2, block.GLOWSTONE_BLOCK)

        # corner 2
        mc.setBlocks(self.x+self.xlength+3, self.y, self.z-2,
                     self.x+self.xlength+3, self.y+4, self.z-2, block.FENCE)
        mc.setBlock(self.x+self.xlength+2, self.y+4,
                    self.z-2, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x+self.xlength+4, self.y+4,
                    self.z-2, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x+self.xlength+3, self.y+4,
                    self.z-1, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x+self.xlength+3, self.y+4,
                    self.z-3, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x+self.xlength+3, self.y+5,
                    self.z-2, block.GLOWSTONE_BLOCK)

        # corner 3
        mc.setBlocks(self.x-2, self.y, self.z+self.zlength+3,
                     self.x-2, self.y+4, self.z+self.zlength+3, block.FENCE)
        mc.setBlock(self.x-1, self.y+4, self.z +
                    self.zlength+3, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x-3, self.y+4, self.z +
                    self.zlength+3, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x-2, self.y+4, self.z +
                    self.zlength+2, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x-2, self.y+4, self.z +
                    self.zlength+4, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x-2, self.y+5, self.z +
                    self.zlength+3, block.GLOWSTONE_BLOCK)

        # corner 4
        mc.setBlocks(self.x+self.xlength+3, self.y, self.z+self.zlength+3,
                     self.x+self.xlength+3, self.y+4, self.z+self.zlength+3, block.FENCE)
        mc.setBlock(self.x+self.xlength+2, self.y+4, self.z +
                    self.zlength+3, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x+self.xlength+4, self.y+4, self.z +
                    self.zlength+3, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x+self.xlength+3, self.y+4, self.z +
                    self.zlength+2, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x+self.xlength+3, self.y+4, self.z +
                    self.zlength+4, block.GLOWSTONE_BLOCK)
        mc.setBlock(self.x+self.xlength+3, self.y+5, self.z +
                    self.zlength+3, block.GLOWSTONE_BLOCK)
class roof():
    def __init__(self, x, y, z, length, width, material, pillar, wall, direction):
        self.x = x
        self.y = y
        self.z = z
        self.length = length
        self.width = width
        self.material = material
        self.wall = wall
        self.pillar = pillar
        self.direction = direction
        #A list of the different roof builds
        roofs = [self.build, self.build2]
        random.choice(roofs)()
        # self.build2()

    def get_dimensions(self, x, y, z, length, width, material):
        '''A way to get the dimensions since the random roof build does not take parameters'''
        return x, y, z, length, width, material

    def build(self):
        x, y, z, length, width, material = self.get_dimensions(
            self.x, self.y, self.z, self.length, self.width, self.material)
        mc.setBlocks(x + 1, y, z + 1, x + length, y, z +
                     width, self.pillar)
        mc.setBlocks(self.x, y + 1, z, x + length + 1,
                     y + 1, z + width + 1, block.WOODEN_SLAB)
        print('build')
        for i in range(3):
            # side 1
            mc.setBlocks(x-1+i, y+1+i, z-1+i, x + length-i+2,
                         y+1+i, z+i-1, material.withData(2))

            # # side 2
            mc.setBlocks(x+length+2-i, y+1+i, z-1+i, x+length+2-i,
                         y+1+i, z+width+2-i, material.withData(1))

            # side 3
            mc.setBlocks(x+length+1-i,
                         y+1+i, z+width+2-i, x-1+i,
                         y+1+i, z+width+2-i, material.withData(3))

            # side 4
            mc.setBlocks(x-1+i,
                         y+1+i, z+width+2-i, x-1+i,
                         y+1+i, z-1+i, material.withData(0))
        # fill in the roof
        # mc.setBlocks(x+2, y+3, z+2, x+length-1,
        #              y+3, z+length-3, block.GLOWSTONE_BLOCK)
        mc.setBlocks(x+2,y+3,z+2,x+length-1,y+3,z+width-1,block.GLOWSTONE_BLOCK)

        # chimney
        # mc.setBlocks(x+3, y+4, z+3,
        #              x+5, y+5, self.z+5, self.wall)

        # mc.setBlocks(x+4, y+4, z+4, x+4, y+5, z+4, block.TORCH)

    def build2(self):
        x, y, z, length, width, material = self.get_dimensions(
            self.x, self.y, self.z, self.length, self.width, self.material)
        if (self.direction == 'East') or (self.direction == 'West'):
            top = (int(length)//2)-1
            for i in range(top):
                # roof side 1
                mc.setBlocks(x, y+1+i, z+i, x + length+1,
                             y+1+i, z+i, material.withData(2))
                # roof side 2
                mc.setBlocks(x+length+1,
                             y+1+i, z+width+1-i, x,
                             y+1+i, z+width+1-i, material.withData(3))

                # wall in between the roofs
                mc.setBlocks(x+1, y+1+i, z+i+1,x+length,
                             y+1+i, z+width-i, self.wall)
                mc.setBlock( self.wall)
            # top of the roof
            mc.setBlocks(x+length+1,
                             y+top, z+width+1-top, x, y+top, z+top, block.GLOWSTONE_BLOCK)      
            mc.setBlocks(x+length+1,
                             y+top+1, z+width+1-top, block.TORCH)

            # pillars
            mc.setBlocks(x+1, y+1, z+1, x+length, y+1, z+width, self.pillar)
        else:
            #for north and south
            top = (int(width)//2)-1
            for i in range(top):
                # roof side 1
                mc.setBlocks(x+i, y+1+i, z, x+i, y+1+i, z +
                             width+1, material.withData(0))
                # roof side 2
                mc.setBlocks(x+length+1-i,
                             y+1+i, z, x+length+1-i,
                             y+1+i, z+width+1, material.withData(1))

                # wall in between the roofs
                mc.setBlocks(x+1+i, y+1, z+1, x+length-i, y +
                             1+i, z+width, self.wall)
            # top of the roof
            mc.setBlocks(x+top, y+top, z, x+length+1-top,
                             y+top, z+width+1, block.GLOWSTONE_BLOCK)

            # pillars
            mc.setBlocks(x+1, y+1, z+1, x+length, y+1, z+width, self.pillar)

    def build3(self):
        print('rof 3')
