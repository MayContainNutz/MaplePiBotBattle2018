import sys
import traceback
import battlecode as bc

#magic numbers
unmapped = 60000
impassable = 65000

def pathPlanetMap(currentMap):
    mapHeight = currentMap.height
    mapWidth = currentMap.width

    #game map grows up and right, array grows down and right
    #so all my maps are upsidedown
    map = [[unmapped]*mapHeight for i in range(mapWidth)]
    
    mL = bc.MapLocation(currentMap.planet,1,1)
    for i in range(0,mapHeight):
        for j in range(0,mapWidth):

            if currentMap.is_passable_terrain_at(bc.MapLocation(currentMap.planet,i,j)):
                map[j][i] = unmapped
            else:
                map[j][i] = impassable
    return map    
            
def pathMap(map, x, y):
    #rearrange the co-ords given to match our internal structure
    sizeOf = len(map)-1
    x,y = sizeOf-y,sizeOf-x
    #define our target destination
    map[x][y] = 0
    #make a list of locations we have rated, to be the source of further ratings
    openlocs = []
    openlocs.append([x,y])
    #so we know not to go off the edges
    edge = len(map)
    #at each location we have rated, we inspect all around it,
    #any that are empty are 1 step further than us
    for loc in openlocs:
        i,j = loc
        #orthagonal
        #x-1,y
        if i-1 >=0:
            if map[i-1][j] == unmapped and map[i-1][j] != impassable:
                map[i-1][j] = map[i][j] +1
                openlocs.append([i-1,j])
        #x,y+1
        if j+1 < edge:
            if map[i][j+1] == unmapped and map[i][j+1] != impassable:
                map[i][j+1] = map[i][j] +1
                openlocs.append([i,j+1])
        #x+1,y
        if i+1 < edge:
            if map[i+1][j] == unmapped and map[i+1][j] != impassable:
                map[i+1][j] = map[i][j] +1
                openlocs.append([i+1,j])
        #x,y-1
        if j-1 >= 0:
            if map[i][j-1] == unmapped and map[i][j-1] != impassable:
                map[i][j-1] = map[i][j] +1
                openlocs.append([i,j-1])
        #diagonal
        #x-1,y+1
        if i-1 >=0 and j+1 < edge:
            if map[i-1][j+1] == unmapped and map[i-1][j+1] != impassable:
                map[i-1][j+1] = map[i][j] +1
                openlocs.append([i-1,j+1])
        #x+1,y+1
        if i+1 < edge and j+1 < edge:
            if map[i+1][j+1] == unmapped and map[i+1][j+1] != impassable:
                map[i+1][j+1] = map[i][j] +1
                openlocs.append([i+1,j+1])     
        #x+1,y-1
        if i+1 < edge and j-1 >=0:
            if map[i+1][j-1] == unmapped and map[i+1][j-1] != impassable:
                map[i+1][j-1] = map[i][j] +1
                openlocs.append([i+1,j-1])
        #x,y-1
        if j-1 >= 0:
            if map[i][j-1] == unmapped and map[i][j-1] != impassable:
                map[i][j-1] = map[i][j] +1
                openlocs.append([i,j-1])
        #x-1,y-1
        if j-1 >= 0 and i-1 >= 0:
            if map[i-1][j-1] == unmapped and map[i-1][j-1] != impassable:
                map[i-1][j-1] = map[i][j] +1
                openlocs.append([i-1,j-1])
    #print(map)
    return map

#given a map(witch should have pathfinding stuffs, and my current location which direction do i move
#return list of directions, starting with best
def whereShouldIGo(map,x,y):
    sizeOf = len(map)-1
    x,y = sizeOf-y,sizeOf-x
    #print(x)
    #print(y)
    #print(sizeOf-x)
    #print(sizeOf-y)
    nearbyLocations = []
    edge = len(map)
    for i in range(-1,2):
        for j in range(-1,2):
            if x+i>=0 and y+j>=0 and x+i<edge and y+j<edge and map[x+i][y+j]<65000:
                nearbyLocations.append([i,j,map[x+i][y+j]])
    for i in range(1,len(nearbyLocations)):
        for j in range(1,len(nearbyLocations)):
            if nearbyLocations[j][2] < nearbyLocations[j-1][2]:
                nearbyLocations[j], nearbyLocations[j-1] = nearbyLocations[j-1], nearbyLocations[j]
    #since map is inverted, +i is south, -i is north
    #+y is east, -y is west?
    sortedLocations = []
    for location in nearbyLocations:
        if location[0] == 1:#south?
            if location[1] == 0:
                sortedLocations.append(bc.Direction.South)
            if location[1] == 1:
                sortedLocations.append(bc.Direction.Southwest)
            if location[1] == -1:
                sortedLocations.append(bc.Direction.Southeast)
        if location[0] == 0:
            if location[1] == 1:
                sortedLocations.append(bc.Direction.West)
            if location[1] == -1:
                sortedLocations.append(bc.Direction.East)
        if location[0] == -1:
            if location[1] == 0:
                sortedLocations.append(bc.Direction.North)
            if location[1] == 1:
                sortedLocations.append(bc.Direction.Northwest)
            if location[1] == -1:
                sortedLocations.append(bc.Direction.Northeast)
    #print(nearbyLocations[0])
    #print(sortedLocations)
    return sortedLocations
