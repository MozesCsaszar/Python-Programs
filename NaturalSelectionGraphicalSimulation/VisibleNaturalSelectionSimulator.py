"""
Simulate a natural ecosystem with carnivore, herbivore and omnivore animals.
Each animal has variable capabilities. The 
"""


import turtle
import random

class Env():
    def __init__(self,size):
        self.env = []
        self.size = size
        for i in range(size):
            self.env.append([])
            for j in range(size):
                self.env[i].append([])
        self.win = turtle.Screen()
        self.win.setworldcoordinates(-0.5,-0.5,size-0.5,size-0.5)
        #the things (sorted)list holds the animals on the screen(alive)
        self.things = []
        self.growingRate = 1

    def setGrowingRate(self,num):
        self.growingRate = num

    def animalChooseAction(self):
        for anim in self.things:
            anim.env.removeFromTile(anim)
            anim.chooseAction()

    def moveAnimals(self):
        # moves the animal to the target (needs to be found first)
        num_animals = len(self.things)
        #k represents the number of integers in the length of the things list
        self.win.tracer(num_animals)
        if num_animals < 40:
            k = 20
        if num_animals < 80:
            k = 45
        elif num_animals < 100:
            k = 70
        elif num_animals < 400:
            k = 280
        elif num_animals < 1000:
            k = 700
        elif num_animals < 3000:
            k = 2400
        elif num_animals < 6000:
            k = 5000
        #z is the number of frames (3000 by default); used to change the pace of the game
        if num_animals < 10:
            k = 20 - num_animals
        else:
            k = 1000 - num_animals
        z = 1000
        for i in range(int(z/k)):
            for animal in self.things:
                animal.turtle.goto(1/z*k*(animal.toGo[0]-animal.loc[0])*(i+1)+animal.loc[0],1/z*k*(animal.toGo[1]-animal.loc[1])*(i+1)+animal.loc[1])
        for animal in self.things:
            self.addToTile(animal)
            animal.loc = animal.turtle.position()
            animal.loc = tuple(animal.loc)

    def animalsDoActions(self):
        # do the action chosen by the animal
        #rework it!!!
        for animal in self.things:
            if type(animal.target) != tuple and type(animal.target) != turtle.Vec2D:
                if animal.toDo == 'Hunt':
                    animal.attack(animal.target)
                elif animal.toDo == 'Eat':
                    animal.eat(animal.target)
                elif animal.toDo == 'Mate':
                    if animal.urge_to_mate > 49 and animal.target.urge_to_mate > 49:
                        animal.mate(animal.target)
                animal.target.targeted = False

    def animalCheck(self):
        #check if the animal dies or not, updates modifiers (hunger,urge_to_mate)
        for animal in self.things:
            animal.tick()
        for animal in self.things:
            animal.target = None
            animal.goTo = None
            animal.toDo = None
                

    def getTile(self,where):
        return self.env[int(where[0])][int(where[1])]

    def addToTile(self,toAdd):
        self.env[int(toAdd.turtle.position()[0])][int(toAdd.turtle.position()[1])].append(toAdd)

    def removeFromTile(self,toRemove):
        self.env[int(toRemove.turtle.position()[0])][int(toRemove.turtle.position()[1])].remove(toRemove)

    def addToThings(self,toAdd):
        #creates an ordered list, so it can use binary insertion
        #searches for the speed value of the toAdd animal, when finds it, inserts the animal there
        needs_placing = True
        start,end = 0,len(self.things)
        if self.things == []:
            self.things.append(toAdd)
        else:
            while needs_placing:
                center = (start + end)//2
                if center == start:
                    needs_placing = False
                    if self.things[start] > toAdd:
                        self.things.insert(start+1,toAdd)
                    else:
                        self.things.insert(start,toAdd)
                elif toAdd == self.things[center]:
                    needs_palcing = False
                    self.things.insert(center,toAdd)
                elif toAdd > self.things[center]:
                    end = center
                else:
                    start = center
        
    def removeFromThings(self,toRemove):
        #removes the toRemove animal from the things list(can be updated to binary search)
        self.things.remove(toRemove)

    def globalTick(self,ticks):
        #global tick will have four (or more) phases:
        #   search target (needs a system to mark the target for mating, because it may run away)
        #   move to target
        #   do the selected action
        #   check status(if dead or not)
        #   create food
        for i in range(ticks):
            self.animalChooseAction()
            self.moveAnimals()
            self.animalsDoActions()
            self.animalCheck()
            self.win.tracer(self.size)
            for j in range(int(self.size**0.5)*self.growingRate):
                f = Plant(self)
    

class Animal():

    @classmethod
    def createDna(cls):
        dna = {}
        for i in ['speed','preg_time','num_of_child','preg_extra_food','hiding_power']:
            dna[i] = random.randrange(cls.dna[i][0],cls.dna[i][1]+1)
            if random.randint(0,7) == 0:
                dna[i] += random.randint(-1,1)
                if dna[i] < 1:
                    dna[i] = 1
        if random.randrange(0,2):
            dna['male'] = True
        else:
            dna['male'] = False
        return dna
    
    def __init__(self,env,dna,loc = None):
        #initialization of the turtle
        if dna == {} or len(dna) < 5:
            dna = type(self).createDna()
        self.dna = dna
        self.turtle = turtle.Turtle()
        self.turtle.penup()
        self.turtle.shape('turtle')
        self.turtle.speed(0)
        if loc == None:
            self.turtle.goto(random.randrange(0,env.size),random.randrange(0,env.size))
        else:
            self.turtle.goto(loc)
        self.turtle.speed(1)
        #initialization of the traits + environment
        self.env = env
        self.env.addToTile(self)
        self.env.addToThings(self)
        self.hunger = 0
        self.loc = self.turtle.position()
        self.urge_to_mate = 0
        if not self.dna['male']:
            self.children_dna = []
            self.time_left_till_birth = -1
            self.is_pregnant = False
        #initialization for additional stats (which help at other methods)
        self.toGo = None
        self.toDo = None
        self.target = None
        self.targeted = False

    def move(self,dest):
        self.env.removeFromTile(self)
        self.turtle.goto(dest)
        self.env.addToTile(self)

    def mate(self,other):
        #pregnancy methdod, start pergnancy method, give birth method, mated method not to mate if pregnant
        #needs a get valid mate function
        ('mated',self.hunger,self.urge_to_mate,other.hunger,other.urge_to_mate)
        self.urge_to_mate -= 50
        other.urge_to_mate -= 50
        if not self.dna['male']:
            self.getPregnant()
        else:
            other.getPregnant()
        

    def wantsToMate(self):
        if not self.dna['male']:
            if self.is_pregnant:
                return False
        if self.urge_to_mate > 49 and self.hunger < 50:
            return True
        return False

    def getPregnant(self,dna = {}):
        self.is_pregnant = True
        self.time_left_till_birth = self.dna['preg_time']
        self.children_dna = dna

    def giveBirth(self):
        for i in range(self.dna['num_of_child']):
            child = type(self)(self.env,self.children_dna,self.loc)
            child.hunger = 80-(self.dna['preg_extra_food']*self.dna['preg_time'])/(self.dna['num_of_child']//3+1)

    def doNothing(self,ize = None):
        if ize==None:
            return None
        else:
            return False
        
    def getTarget(self,to_search_func):
        x =  int(self.turtle.position()[0])
        y = int(self.turtle.position()[1])
        lastLoc = []
        for i in range(3):
            for j in range(3):
                try:
                    tile = self.env.getTile((x+i,y+j))
                    lastLoc.append((x+i,y+j))
                    for k in tile:
                        if to_search_func(k):
                            return k
                except:
                    self.doNothing
                try:
                    if y-j <= -1:
                        raise Error('NegativeNumber')
                    tile = self.env.getTile((x+i,y-j))
                    lastLoc.append((x+i,y-j))
                    for k in tile:
                        if to_search_func(k):
                            return k
                except:
                    self.doNothing
                try:
                    if x-i <= -1:
                        raise Error('NegativeNumber')
                    tile = self.env.getTile((x-i,y+j))
                    lastLoc.append((x-i,y+j))
                    for k in tile:
                        if to_search_func(k):                           
                            return k
                except:
                    self.doNothing
                try:
                    if y-j <= -1 or x-i <= -1:
                        raise Error('NegativeNumber')
                    tile = self.env.getTile((x-i,y-j))
                    lastLoc.append((x-i,y-j))
                    for k in tile:
                        if to_search_func(k):                            
                            return k
                except:
                    self.doNothing
        return lastLoc[random.randrange(len(lastLoc))]
                
    def eat(self,toEat):
        if self.hunger >= toEat.nutrition:
            self.hunger -= toEat.nutrition
            toEat.remove()
        else:
            toEat.nutrition -= self.hunger
            self.hunger = 0

    def validFood(self,other):
        if type(other) == self.dna['eats'] and not other.targeted:
            return True
        return False

    def validMate(self,other):
        if type(other) == type(self) and other.wantsToMate() and other.dna['male'] != self.dna['male'] and not other.targeted and not other.target:
            return True

    #chooses the action
    def chooseAction(self):
        #wants to mate
        if self.wantsToMate():
            self.target = self.getTarget(self.validMate)
            self.toDo = 'Mate'
        elif self.hunger > 10:
            self.target = self.getTarget(self.validFood)
            self.toDo = 'Eat'
        else:
            self.target = self.getTarget(self.doNothing)
        self.setDestination()
    
    #sets the location where to go
    def setDestination(self):
        if self.targeted:
            self.toGo = self.loc
        elif type(self.target) == tuple or type(self.target) == turtle.Vec2D:
            self.toGo = self.target
        else:
            self.target.targeted = True
            self.toGo = self.target.turtle.position()
            
    #at the end of the turn of an animal, check status and update it
    def tick(self):
        self.hunger += 3 + self.dna['speed']/5
        if self.urge_to_mate <= 50:
            self.urge_to_mate += 2
        else:
            self.urge_to_mate += random.randint(0,1)
        if not self.dna['male'] and self.is_pregnant:
            if self.time_left_till_birth == 0:
                self.giveBirth()
                self.time_till_birth = -1
                self.is_pregnant = False
            elif self.time_left_till_birth > 0:
                self.hunger += self.dna['preg_extra_food']
                self.time_left_till_birth -= 1
        if self.hunger > 100:
            self.die()

    def remove(self):
        self.env.removeFromThings(self)
        self.env.removeFromTile(self)
        self.turtle.reset()
        self.turtle.hideturtle()

    def die(self):
        if self.hunger < 100:
            meat = Meat(self.env,self.loc)
            meat.nutrition = (100 - self.hunger)/5*(11-self.dna['speed'])
        self.remove()

    def __lt__(self,other):
        if self.dna['speed'] < other.dna['speed']:
            return True
        else:
            return False

    def __le__(self,other):
        if self.dna['speed'] <= other.dna['speed']:
            return True
        else:
            return False

    def __gt__(self,other):
        if self.dna['speed'] > other.dna['speed']:
            return True
        else:
            return False

    def __ge__(self,other):
        if self.dna['speed'] >= other.dna['speed']:
            return True
        else:
            return False

    def __repr__(self):
        return str(self.dna['speed'])
        

class Herbivore(Animal):
    def __init__(self,env,dna,loc = None):
        super().__init__(env,dna,loc)
        self.dna['eats']=Plant
        #self.dna['hide_power'] = 0

    def returnType(self):
        return Herbivore

class Rabbit(Herbivore):

    dna = {'speed':(3,9),'preg_time':(7,15),'preg_extra_food':(1,3),'num_of_child':(3,8),'hiding_power':(25,40)}
    
    def __init__(self,env,dna,loc = None):
        super().__init__(env,dna, loc)
        env.win.addshape('rabbit.gif')
        self.turtle.shape('rabbit.gif')


class Sheep(Herbivore):

    dna = {'speed':(1,5),'preg_time':(10,20),'preg_extra_food':(1,3),'num_of_child':(3,10),'hiding_power':(10,25)}
    
    def __init__(self,env,dna,loc = None):
        super().__init__(env,dna,loc)
        

class Carnivore(Animal):
    def __init__(self,env,dna,loc = None):
        super().__init__(env,dna,loc)
        self.dna['eats'] = Meat
        self.dna['hunts'] = [Herbivore, Omnivore]
        #the agression of an animal will be composed of agression_over_time + hunger
        self.agression_over_time = 0

    def returnType(self):
        return Carnivore

    def validPrey(self,other):
        if self.agression_over_time + self.hunger > 70:
            #final one
            if super(type(other),other).returnType() == Carnivore and not other.targeted and not type(other) == type(self):
                return True
        if super(type(other),other).returnType() in self.dna['hunts'] and not other.targeted:
            return True
        return False

    def canCatch(self,other):
        pass
    
    def attack(self,other):
        self.agression_over_time = 0
        other.die()
        
    #chooses the action
    def chooseAction(self):
        #wants to mate
        if self.wantsToMate():
            self.target = self.getTarget(self.validMate)
            self.toDo = 'Mate'
        elif self.hunger > 25:
            self.target = self.getTarget(self.validFood)
            if type(self.target) == tuple:
                self.toDo = 'Hunt'
                self.target = self.getTarget(self.validPrey)
            else:
                self.toDo = 'Eat'
        else:
            self.target = self.getTarget(self.doNothing)
        self.setDestination()

    def tick(self):
        super().tick()
        if self.hunger > 30:
            self.agression_over_time += random.randint(1,2)
        else:
            self.agression_over_time += random.randint(0,1)


class Fox(Carnivore):
    dna = {'speed':(7,9),'preg_time':(10,20),'preg_extra_food':(1,3),'num_of_child':(1,3),'hiding_power':(20,30)}
    def __init__(self,env,dna,loc = None):
        super().__init__(env,dna,loc)
        env.win.addshape('fox.gif')
        self.turtle.shape('fox.gif')
        


class Omnivore(Animal):
    def __init__(self,env,dna,loc):
        super().__init__(env,dna,loc)
        self.dna['eats'] = [Plant,Meat]
    
    def validFood(self,other): 
        if type(other) in self.dna['eats'] and not other.targeted:
            return True
        return False

    def returnType(self):
        return Omnivore

class Pig(Omnivore):
    dna = {'speed':(1,5),'preg_time':(15,27),'preg_extra_food':(1,3),'num_of_child':(3,5),'hiding_power':(7,15)}
    def __init__(self,env,dna,loc = None):
        super().__init__(env,dna,loc)
        env.win.addshape('pig.gif')
        self.turtle.shape('pig.gif')


class Food():
    def __init__(self,env,place):
        self.turtle = turtle.Turtle()
        self.turtle.color('green')
        self.turtle.penup()
        self.turtle.speed(0)
        self.turtle.goto(place)
        self.env = env
        self.env.addToTile(self)
        self.nutrition = 0
        self.targeted = False

    def remove(self):
        self.env.removeFromTile(self)
        self.turtle.reset()
        self.turtle.hideturtle()


class Plant(Food):
    def __init__(self,env):
        super().__init__(env,(random.randrange(env.size),random.randrange(env.size)))
        env.win.addshape('plant.gif')
        self.turtle.shape('plant.gif')
        self.nutrition = random.randrange(7,16)
        

class Meat(Food):
    def __init__(self,env,place = None):
        if place == None:
            place = (random.randrange(0,env.size),random.randrange(0,env.size))
        super().__init__(env,place)
        env.win.addshape('meat.gif')
        self.turtle.shape('meat.gif')
        

env = Env(10)
env.win.tracer(32)
env.setGrowingRate(3)
for i in range(2):
    o = Pig(env,{})
for i in range(5):
    o = Rabbit(env,{})
for i in range(2):
    o = Fox(env,{})
env.win.tracer(10)
#for i in range(100):
 #   f = Plant(env)
    
env.globalTick(750)
