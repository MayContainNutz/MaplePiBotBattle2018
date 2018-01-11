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
        continue

#processes the map into an int field
myMap = pathFinding.pathPlanetMap(myMap)
#enemyx,enemyy is the starting locations of(at least one) of the enemies bots
#I am making the assumption that they stay near there
start = time.time()
myMap = pathFinding.pathMap(myMap, enemyx, enemyy)
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
    return

def workerLogic():
    #TODO: find and gather resources
    #TODO: be picky about building placement
    #if there is something I can build nearby, do so, or if i can garrison, do that
    if unit.location.is_on_map() and unit.location.is_on_planet(bc.Planet.Earth):
        nearby = gc.sense_nearby_units(unit.location.map_location(), 2)
        for other in nearby:
            if gc.can_build(unit.id, other.id):
                gc.build(unit.id, other.id)
                continue
            if gc.can_load(other.id, unit.id):
                gc.load(other.id, unit.id)
    
    #TODO: worker pathing, current random wander
    d = random.choice(directions)
    if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
        gc.move_robot(unit.id, d)
    
    #TODO: under 10 workers, replicate, otherwise build atleast 1 rocket and upto 5 factories
    if numWorkers < 10:
        if gc.can_replicate(unit.id, d):
            gc.replicate(unit.id, d)
    else:
        if numRockets < 1 and rocketCount < 1:
            if gc.karbonite() > bc.UnitType.Rocket.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Rocket, d) and gc.research_info().get_level(bc.UnitType.Rocket) > 0:
                #numRockets+=1#because we just built one, saves us making many at a time#makes numRockets local, breaks functionality
                print("built rocket")
                gc.blueprint(unit.id, bc.UnitType.Rocket, d)
        if gc.karbonite() > bc.UnitType.Factory.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, d) and numFactories < 5:
            print("built factory")
            gc.blueprint(unit.id, bc.UnitType.Factory, d)
    
    return

def rocketLogic():
    if unit.location.is_on_planet(bc.Planet.Mars):
        d = random.choice(directions)
        if gc.can_unload(unit.id, d):
            gc.unload(unit.id, d)
    myx = unit.location.map_location().x
    myy = unit.location.map_location().y
    destination = bc.MapLocation(bc.Planet.Mars, myx, myy)
    #TODO:wait until has someone in before launch
    garrison = unit.structure_garrison()
    garrisoned = 0
    for thing in garrison:
        garrisoned+=1
    if garrisoned == unit.structure_max_capacity():
        print("we takin off boys")
        #TODO:make sure destination is a valid landing zone, currently keeps x,y from earth
        if gc.can_launch_rocket(unit.id, destination):
            gc.launch_rocket(unit.id, destination)
    return

def knightLogic():
    #TODO: movement and attack logic
    return

def rangerLogic():
    #TODO: movement and attack logic
    return

def mageLogic():
    #TODO: movement and attack logic
    return

def healerLogic():
    #TODO: movement and heal logic
    return


#turn loop
while True:
    try:
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


