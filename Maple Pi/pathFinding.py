import sys
import traceback
import battlecode as bc

#magic numbers
unmapped = 60000
impassable = 65000

def pathPlanetMap(currentMap):
    mapHeight = currentMap.height
    mapWidth = currentMap.width
    
    map = [[unmapped]*mapHeight for i in range(mapWidth)]
    
    mL = bc.MapLocation(currentMap.planet,1,1)
    for i in range(0,mapHeight):
        for j in range(0,mapWidth):

            if currentMap.is_passable_terrain_at(bc.MapLocation(currentMap.planet,i,j)):
                map[i][j] = unmapped+1
            else:
                map[i][j] = impassable+1
    return map    
            
def pathMap(map, x, y):
    #TODO: test diagonal pathing
    #openlocs = [[1]*5 for i in range(5)]

    openlocs = []
    map[x][y] = 0
    openlocs.append([x,y])

    edge = len(map)
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
    print(map)
    return map

#given a map(witch should have pathfinding stuffs, and my current location which direction do i move
def whereShouldIGo(map,x,y):
    return x,y
