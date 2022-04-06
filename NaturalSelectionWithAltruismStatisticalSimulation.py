"""
Simulate fluctuations in populations of creatures with changable altruism chances
(which decides if the creature will want to share or fight for food) and other
settings.
"""


from random import random
import numpy as np
import matplotlib.pyplot as plt

mutations_enabled = True
monitor_population_enabled = True

class Creature:
    mutation_coefficient = 10

    def __init__(self,share_percent = 1, reproduction_delay = 1, nr_offspring = 1, offspring_cost = 1,max_age = 12, peace_percent = 1):
        self.share_percent = share_percent
        self.peace_percent = peace_percent
        self.food_count = 0
        self.reproduction_delay = reproduction_delay
        self.days_until_reproduction = reproduction_delay
        self.nr_offspring = nr_offspring
        self.offspring_cost = offspring_cost
        self.age = 0
        self.max_age = max_age
        self.health = 100

    @classmethod
    def get_mutation_value(this, val):
        val += (random()-0.5)/this.mutation_coefficient
        if val > 1:
            val = 1
        elif val < 0:
            val = 0
        return val

    @classmethod
    def check_percent(this,val):
        if random() >= val:
            return True
        return False

    def reproduce(self):
        share_percent = self.share_percent
        peace_percent = self.peace_percent
        if mutations_enabled:
            share_percent = Creature.get_mutation_value(share_percent)
            peace_percent = Creature.get_mutation_value(peace_percent)
        return Creature(share_percent,self.reproduction_delay,self.nr_offspring,self.offspring_cost,self.max_age, peace_percent)

    def __repr__(self):
        return str(self.food_count)



day_count = 100
loop_count = 1

food_count = 10
food_per_loc = 3
#prepare food_loc
food_loc = []
for _ in range(food_count):
    food_loc.append([])

av_feeding_grounds = []
nr_max_creature_loc = 200

creatures = []

monitor_creatures = []

#start creatures for my current ecosystem
#start_creatures = ( (75,"Pacifist dove","blue",1,4,2,1, 36),(60,"Agressive dove","red",0.8,6,1,2, 30),
#                   (30,"Falcon","green",0.4,6,3,5, 48),(5,"Bear","brown",0,12,2,20, 240) )

#decrementing valued creatures
start_creatures = ( (30, "Crea 1","blue",1,5,2,1, 36),(30, "Crea 0.8","green",0.8,5,2,1, 36),
                    (30, "Crea 0.6","red",0.6,5,2,1, 36),(30, "Crea 0.4","brown",0.4,5,2,1, 36),
                    (30, "Crea 0.2","pink",0.2,5,2,1, 36),(30, "Crea 0","yellow",0,5,2,1, 36)  )

#used to monitor the stats of the creatures as a whole
#for each start creature group, put one monitor component in
for s_c in start_creatures:
    monitor_creatures.append({"share_percent":s_c[2]})
        
#used to monitor the creature number of each population
y = []
for i in range(len(start_creatures)):
    y.append([start_creatures[i][0]])

for i in range(len(y)):
    for _ in range(day_count-1):
        y[i].append(0)

#populate creatures list with creatures created from start_creatures
def instantiate_creatures(creatures):
    for i in range(len(start_creatures)):
        creatures.append([])
        for _ in range(start_creatures[i][0]):
            creatures[i].append(Creature(start_creatures[i][3],start_creatures[i][4],start_creatures[i][5],start_creatures[i][6],start_creatures[i][7]))

#place creatures to their respective feeding grounds
def assign_creatures_to_feeding_grounds(food_loc,creatures):
    #reset food_loc
    for i in range(food_count):
        food_loc[i]=[]
    #get the feeding grounds
    av_feeding_grounds = []
    for i in range(food_count):
        av_feeding_grounds.append(i)
    #assign creatures to food
    for i in range(len(creatures)):
        for j in range(len(creatures[i])):
            loc = int(random()*len(av_feeding_grounds))
            food_loc[loc].append((i,j))
            #if feeding_ground is full, delete it
            if len(food_loc[loc]) == nr_max_creature_loc:
                del av_feeding_grounds[loc]

#get a location object and distribute the food there 
def distribute_food(l,creatures):
    agressive = []
    pacifist= []
    av_food = food_per_loc
    for i in range(len(l)):
        if Creature.check_percent(creatures[l[i][0]][l[i][1]].share_percent):
            agressive.append(l[i])
        else:
            pacifist.append(l[i])
    if len(agressive) > 1:
        for l in agressive:
            creatures[l[0]][l[1]].food_count += av_food/(4*len(l))
        av_food -= len(agressive)*av_food/(4*len(l))
        for l in pacifist:
            creatures[l[0]][l[1]].food_count += av_food/len(pacifist)
    elif len(agressive) == 1:
        creatures[agressive[0][0]][agressive[0][1]].food_count += av_food*3/5
        av_food *= 2/5
        for l in pacifist:
            creatures[l[0]][l[1]].food_count += av_food/len(pacifist)
    else:
        for l in pacifist:
            creatures[l[0]][l[1]].food_count += av_food/len(pacifist)

def resolve_food_consequences(creatures):
    n_creatures = []
    for i in range(len(creatures)):
        n_creatures.append([])
        for c in creatures[i]:
            #increment the age of the creature
            c.age += 1
            if c.age > c.max_age:
                continue
            
            #if you have less than 1 food, check if it is enought to survive
            if c.food_count <= 1:
                number = random()
                if number < c.food_count:
                    n_creatures[i].append(c)
            #if it has one or more food, it survives automatically
            if c.food_count > 1:
                n_creatures[i].append(c)
                number = (random()+c.nr_offspring-1)*c.offspring_cost
                #if it has enought food to reproduce, then reproduce
                if number < c.food_count and c.days_until_reproduction == 0:
                    for _ in range(c.nr_offspring):
                        n_creatures[i].append(c.reproduce())
                    c.food_count -= c.offspring_cost*c.nr_offspring
                    c.days_until_reproduction = c.reproduction_delay
            #decrement days_until_reproduction
            if c.days_until_reproduction > 0: 
                c.days_until_reproduction -= 1
            #decrement food
            c.food_count -= 1
    return n_creatures


#the main loop of the simulation
for _ in range(loop_count):
    #create and set creatures for the next round
    creatures = []

    #create creatures 
    instantiate_creatures(creatures)
    
    for d in range(day_count-1):
        #assign creatures to feeding grounds
        assign_creatures_to_feeding_grounds(food_loc,creatures)

        #distribute food
        for l in food_loc:
            distribute_food(l,creatures)

        #resolve deaths and reproduction
        creatures = resolve_food_consequences(creatures)

        #monitor creature population numbers
        for i in range(len(creatures)):
            y[i][d+1] += len(creatures[i])
    #decrease food_count after every loop
            
#monitor population stats
if monitor_population_enabled:
    for i in range(len(creatures)):
        monitor_creatures[i]["share_percent"] = 0
        for c in creatures[i]:
            monitor_creatures[i]["share_percent"] += c.share_percent
        if len(creatures[i]):
            monitor_creatures[i]["share_percent"] /= len(creatures[i])
            #PLACEHOLDER for function which will output the result in a nice and meaningful way
            print("{} \n    Share chance: {}".format(start_creatures[i][1],monitor_creatures[i]["share_percent"]))
        else:
            print("{} has gone extinct.".format(start_creatures[i][1]))
            
#normalize runs by dividing the sum by the loop count
for i in range(len(y)):
    for j in range(1,len(y[i])):
        y[i][j] = y[i][j] / loop_count

#put the results into a diagram
for i in range(len(y)):
    x = x = np.linspace(1,day_count,day_count)
    plt.plot(x,y[i],label = start_creatures[i][1], color = start_creatures[i][2])
    
#put a legend on the diagram and display it

plt.legend()
plt.show()
    
