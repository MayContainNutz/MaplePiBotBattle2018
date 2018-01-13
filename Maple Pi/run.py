import battlecode as bc
import sys
import traceback
import time

import pathFinding
#TODO: remove random and use intelligent pathing
import random

#build my environment
gc = bc.GameController()
directions = list(bc.Direction)

#get the starting map
myMap = gc.starting_map(gc.planet())

#get my team name
my_team = gc.team()

#get the details of the orbit
orbit = gc.orbit_pattern()

#TOTO:research, currently only gets the first level of rockets
gc.queue_research(bc.UnitType.Rocket)

#count my starting units, and find out where the enemy spawned
enemyx = 0
enemyy = 0
friendlyx = 0
friendlyy = 0
myStartingUnits = 0
#TODO:account for starting off world
for unit in myMap.initial_units:
    if unit.team != my_team:
        enemyLocation = unit.location
        enemyx = enemyLocation.map_location().x
        enemyy = enemyLocation.map_location().y
        continue
    if unit.team == my_team:
        myStartingUnits += 1
        friendlyx = unit.location.map_location().x
        friendlyy = unit.location.map_location().y
        continue

#processes the map into an int field
myMap = pathFinding.pathPlanetMap(myMap)
#enemyx,enemyy is the starting locations of(at least one) of the enemies bots
#I am making the assumption that they stay near there
start = time.time()
#TODO:map testing
myMap = pathFinding.pathMap(myMap, enemyx, enemyy)
#reverseMap = pathFinding.pathMap(myMap, friendlyx, friendlyy)
end = time.time()
print("did the map thing in:")
print(end-start)

#print(myMap.initial_units)
#unit counters init
numFactories = 0
numRockets = 0
numWorkers = 0
numKnights = 0
numRangers = 0
numMages = 0
numHealers = 0
factoryCount = 0
rocketCount = 0
workerCount = myStartingUnits
knightCount = 0
rangerCount = 0
mageCount = 0
healerCount = 0

#logic for each unit type
def factoryLogic():
    #TODO: build order/rations ect
    if gc.can_produce_robot(unit.id, bc.UnitType.Ranger) and numRangers < 5:
        gc.produce_robot(unit.id, bc.UnitType.Ranger)
    if len(unit.structure_garrison()) > 0:
        myDirections = pathFinding.whereShouldIGo(myMap, unit.location.map_location().x, unit.location.map_location().y)
        for d in myDirections:
            if gc.can_unload(unit.id, d):
                gc.unload(unit.id, d)
    return

def workerLogic():
    #If i am on a map
    if unit.location.is_on_map():
        #get valid directions around me
        myDirections = pathFinding.whereShouldIGo(myMap, unit.location.map_location().x, unit.location.map_location().y)
        #find out what else is near me
        nearby = gc.sense_nearby_units(unit.location.map_location(), 50)
        nearbyWorkers = 0
        for other in nearby:
            if gc.can_build(unit.id, other.id):#if its something I can build, then I should
                gc.build(unit.id, other.id)
                continue
            if other.unit_type == unit.unit_type and other.team == unit.team:#note, this unit shows up here, so +1
                nearbyWorkers +=1#we cound the number of other workers we can see
        if nearbyWorkers < 3:#if there arent enough, we build more workers
            for d in reversed(myDirections):#we want to buid the worker as far from the enemy as possible without moving
                if gc.can_replicate(unit.id, d):
                    gc.replicate(unit.id, d)
        if numFactories < 3:#if their arent many factories reporting in
                if gc.karbonite() > bc.UnitType.Factory.blueprint_cost():#can we afford it
                    for d in myDirections:#furthest from the enemy again
                        if gc.can_blueprint(unit.id, bc.UnitType.Factory, d):#if the direction is valid for building
                            print("built factory")
                            gc.blueprint(unit.id, bc.UnitType.Factory, d)
        #next we want to harvest all the kryponite, we also want to track if we have harvested any
        haveHarvested = 0
        for direction in myDirections:
            if gc.can_harvest(unit.id, direction):
                haveHarvested = 1
                #print("found dirt")
                gc.harvest(unit.id, direction)
        #TODO:spread out to make sure we harvest all kryptonite on the map
        if haveHarvested == 0:
            #print("no dirt")
            for d in reversed(myDirections):
                if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                    #print(d)
                    gc.move_robot(unit.id, d)
        
        #basicly do a fill, if i cant see another worker, make one, gather any kryponite i can see, then move slowly out from my corner
    """
    #TODO: be picky about building placement

    if unit.location.is_on_map(): # and unit.location.is_on_planet(bc.Planet.Earth):
        nearby = gc.sense_nearby_units(unit.location.map_location(), 2)
        for other in nearby:
            if gc.can_build(unit.id, other.id):
                gc.build(unit.id, other.id)
                continue
            if gc.can_load(other.id, unit.id):
                gc.load(other.id, unit.id)
    else:
        if numRockets < 1:
            if gc.karbonite() > bc.UnitType.Rocket.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Rocket, d) and gc.research_info().get_level(bc.UnitType.Rocket) > 0:
                #numRockets+=1#because we just built one, saves us making many at a time#makes numRockets local, breaks functionality
                print("built rocket")
                gc.blueprint(unit.id, bc.UnitType.Rocket, d)
        if numFactories < 5:
            if gc.karbonite() > bc.UnitType.Factory.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
                print("built factory")
                gc.blueprint(unit.id, bc.UnitType.Factory, d)
    """
    return

def rocketLogic():
    if unit.location.is_on_planet(bc.Planet.Mars):
        d = random.choice(directions)
        if gc.can_unload(unit.id, d):
            gc.unload(unit.id, d)
    elif unit.location.is_on_planet(bc.Planet.Earth):
        myx = unit.location.map_location().x
        myy = unit.location.map_location().y
        destination = bc.MapLocation(bc.Planet.Mars, myx, myy)
        #TODO:wait until has someone in before launch
        garrison = unit.structure_garrison()
        garrisoned = 0
        for thing in garrison:
            garrisoned+=1
        if garrisoned > 0:
            #print("we takin off boys")
            #TODO:make sure destination is a valid landing zone, currently keeps x,y from earth
            if gc.can_launch_rocket(unit.id, destination):
                gc.launch_rocket(unit.id, destination)
    return

def knightLogic():
    #TODO: movement and attack logic
    if unit.location.is_on_map():
        nearby = gc.sense_nearby_units(unit.location.map_location(), unit.vision_range)
        myDirections = pathFinding.whereShouldIGo(myMap, unit.location.map_location().x, unit.location.map_location().y)
        knightsNearby = 0
        for other in nearby:
            if other.unit_type == unit.unit_type and other.team == unit.team:
                knightsNearby+=1
            if other.team != unit.team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id):
                gc.attack(unit.id, other.id)
            if other.team != unit.team:
                me = unit.location.map_location()
                them = other.location.map_location()
                directionToThem = me.direction_to(them)
                if gc.is_move_ready(unit.id) and gc.can_move(unit.id, directionToThem):
                    gc.move_robot(unit.id, directionToThem)
        #print(myDirections)
        for d in myDirections:
            if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                #print(d)
                gc.move_robot(unit.id, d)
    return

def rangerLogic():
    #TODO: movement and attack logic
    #print("i'm alive")
    #TODO: dont move into my minimum range
    if unit.location.is_on_map():
        nearby = gc.sense_nearby_units(unit.location.map_location(), unit.vision_range)
        myDirections = pathFinding.whereShouldIGo(myMap, unit.location.map_location().x, unit.location.map_location().y)
        rangersNearby = 0
        for other in nearby:
            if other.unit_type == unit.unit_type and other.team == unit.team:
                rangersNearby+=1
            if other.team != unit.team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id):
                gc.attack(unit.id, other.id)
            if other.team != unit.team:
                distanceTo = unit.location.map_location().distance_squared_to(other.location.map_location())
                myRange = unit.attack_range()
                if distanceTo < myRange:
                    #move away
                    for d in reversed(myDirections):
                        if gc.is_move_ready(unit.id) and gc.can_move(unit.id,d):
                            gc.move_robot(unit.id,d)
                else:
                    me = unit.location.map_location()
                    them = other.location.map_location()
                    directionToThem = me.direction_to(them)
                    if gc.is_move_ready(unit.id) and gc.can_move(unit.id, directionToThem):
                        gc.move_robot(unit.id, directionToThem)
                #outside range, inside view range, move closer
        #print(myDirections)
        for d in myDirections:
            if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                #print(d)
                gc.move_robot(unit.id, d)
    #TODO: wait for friends
    #TODO: once i dont have enemies, full map search
    #if there are 3? other rangers nearme, then move toward target
    return

def mageLogic():
    #TODO: movement and attack logic
    if unit.location.is_on_map():
        nearby = gc.sense_nearby_units(unit.location.map_location(), unit.vision_range)
        myDirections = pathFinding.whereShouldIGo(myMap, unit.location.map_location().x, unit.location.map_location().y)
        magesNearby = 0
        for other in nearby:
            if other.unit_type == unit.unit_type and other.team == unit.team:
                magesNearby+=1
            if other.team != unit.team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id):
                gc.attack(unit.id, other.id)
            if other.team != unit.team:
                distanceTo = unit.location.map_location().distance_squared_to(other.location.map_location())
                myRange = unit.attack_range()
                if distanceTo < myRange:
                    #move away
                    for d in reversed(myDirections):
                        if gc.is_move_ready(unit.id) and gc.can_move(unit.id,d):
                            gc.move_robot(unit.id,d)
                else:
                    me = unit.location.map_location()
                    them = other.location.map_location()
                    directionToThem = me.direction_to(them)
                    if gc.is_move_ready(unit.id) and gc.can_move(unit.id, directionToThem):
                        gc.move_robot(unit.id, directionToThem)
                #outside range, inside view range, move closer
        #print(myDirections)
        for d in myDirections:
            if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                #print(d)
                gc.move_robot(unit.id, d)
    return

def healerLogic():
    #TODO: movement and heal logic
    return


#turn loop
while True:
    try:
        #print(gc.karbonite())#proves karbonite is shared accross planets
        #unit counters
        numFactories = factoryCount
        numWorkers = workerCount
        numRockets = rocketCount
        numKnights = knightCount
        numRangers = rangerCount
        numMages = mageCount
        numHealers = healerCount
        factoryCount = 0
        rocketCount = 0
        workerCount = 0
        knightCount = 0
        rangerCount = 0
        mageCount = 0
        healerCount = 0
        
        #turn logic goes here,
        #we seperate into a function for each unit type,
        #and count the number of each unit we have
        #so we can have build ratios and limits
        for unit in gc.my_units():
            if unit.unit_type == bc.UnitType.Factory:
                factoryCount+=1
                factoryLogic()
                continue
            if unit.unit_type == bc.UnitType.Rocket:
                rocketCount+=1
                rocketLogic()
                continue
            if unit.unit_type == bc.UnitType.Worker:
                if unit.location.is_on_map():
                    workerCount+=1
                workerLogic()
                continue
            if unit.unit_type == bc.UnitType.Knight:
                knightCount+=1
                knightLogic()
                continue
            if unit.unit_type == bc.UnitType.Ranger:
                rangerCount+=1
                rangerLogic()
                continue
            if unit.unit_type == bc.UnitType.Mage:
                mageCount+=1
                mageLogic()
                continue
            if unit.unit_type == bc.UnitType.Healer:
                healerCount+=1
                healerLogic()
                continue
    except Exception as e:
        print('Error:', e)
        # use this to show where the error was
        traceback.print_exc()

    # send the actions we've performed, and wait for our next turn.
    gc.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()


