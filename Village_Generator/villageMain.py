# Assignment 1 main file 
# Feel free to add additional modules/files as you see fit.

# DON'T SET UP NEW X Y Z COOORD IN OTHER MODULES, REFERENCE COORDS ONLY FROM HERE!!!!!!! testing webhooks
from secrets import choice
from mcpi.minecraft import Minecraft
from mcpi import block
from Houses import House
from Terraforming import Terraform
import time
import random
import time
import math
import blocks
from Path import housePath
 

mc = Minecraft.create()

#Get beginning position
x, y, z = mc.player.getPos()
x, y, z = round(x), round(y), round(z)
mc.postToChat(f'x: {x}, y: {y}, z: {z}')    

# place path function
def placePath(path_list):
    for path in path_list:
        path.clearPath()

    for path in path_list:
        path.placeOutline()

    for path in path_list:
        path.placeBlocksInPath(block.STONE_BRICK.id)

#dictionary of the paths last direction best on which section the house is in
path_end_directions = {
    "north_east": ["North","East"],
    "north_west": ["North","West"],
    "south_east": ["South","East"],
    "south_west": ["South","West"]
}

# adjustable front house locations
house_front = {
    "North": [0,6],
    "East": [-6,0],
    "South": [0,-6],
    "West": [6,0]
}

#stores the different types of tree blocks (moved here cos oml could not ready the code with this big hunk of junk in the way swtg)
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


#randomise amount of houses being built
num_houses = random.randint(5,6)

#house placement, max_dist, farther x or z coordinate, min gap = at least that far from another house, max_build_height = cannot build higher or lower than that point
max_dist = 50
min_gap = 18
max_build_height = 7

#empty lists for coordinates of houses, a list of the houses, and the end to end of each house respectively
house_locations = []
house_list = []
house_areas = []
house_objects = []
path_list = []

#creating area to exclude of building houses so theyre not directly inline with the player
exclude = []
for i in range(21):
    exclude.append(i-10)

#loop for building each house
for i in range(num_houses):

    # #randomise location
    housex = random.choice(list(set([x for x in range(-max_dist, max_dist)]) - set(exclude)))
    housez = random.choice(list(set([x for x in range(-max_dist, max_dist)]) - set(exclude)))
    #testing branch and avoiding
    # housex = (i+1)*20
    # housez = (i+1)*20
    print(housex,housez)
    housey = mc.getHeight(x + housex, z + housez)

    #first houses location doesnt have to avoid any other houses
    build = False
    if house_locations == []:
        build = True

    while not build:
        # print(x, housex, z, housez)
        housey = mc.getHeight(x + housex, z + housez)
        # print("yay")
        for x_val, z_val in house_locations:
            if ((housex > x_val + min_gap) or (housex < x_val - min_gap)):
                build = True
            elif ((housez > z_val + min_gap) or (housez < z_val - min_gap)):
                build = True
            else:
                build = False
                housex = random.choice(list(set([x for x in range(-max_dist, max_dist)]) - set(exclude)))
                housez = random.choice(list(set([x for x in range(-max_dist, max_dist)]) - set(exclude)))
                break
    
    #ensures the house is not built too high or too low
    if (housey > y + max_build_height):
        housey = y + max_build_height
    elif housey < y - max_build_height:
        housey = y-max_build_height

    #adds the coordinates of the house a list
    house_displacement = (housex, housez)
    house_locations.append(house_displacement)

    #assigns the dimensions of the house
    story = random.randint(1, 2)
    xlength = random.randrange(9, 14, 2)
    zlength = random.randrange(9, 12, 2)
    height = random.randrange(3, 5)

    house_path = housePath(x + housex, housey + 1, z + housez, x, y, z)
    house_path.setRandomDirection(path_end_directions)
    #adds the path to a list so it can iterate through once terraforming has been complete
    path_list.append(house_path)  

    land = Terraform(x + housex, housey, z + housez, xlength + 6, zlength + 6, house_path.direction)

    if mc.getBlockWithData(x + housex, housey, z + housez) in treeBlocks:
        # logging funtion removes the tree and returns the highest y value, for x and z, with the tree removed.
        mc.postToChat('logging...')
        housey = land.logging()
        land.y = housey

    mc.postToChat('terraforming...')
    land.carve()
    land.hill()
    time.sleep(1)

    #creates house class with parameters of the house
    house = House(story, xlength, zlength, height, x + housex, housey + 1, z + housez, house_path.direction, house_path)
    house_list.append(house)
    house.section = house_path.section
    house_area = list(house.get_dimensions())
    house_areas.append(house_area) 
    house_objects.append(house) 
    
time.sleep(1)
mc.postToChat('pathing...')
for paths in path_list:
    section_houses = paths.objectsInSection(house_objects)
    section_paths = paths.existingPathsInSection(section_houses)
    paths.initializePath(house_front, house_areas, house_objects, section_houses, section_paths)
placePath(path_list)


    
time.sleep(1)
#calls the function to actually build the house
for house in house_list:
    mc.postToChat('building...')
    house.build_house()

mc.postToChat('village built!')
print(house_locations)
print(house_areas)