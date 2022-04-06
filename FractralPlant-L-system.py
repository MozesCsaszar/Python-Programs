"""
Fractal tree generation with L-system (based on 7th article model on wikipedia
L-system article: https://en.wikipedia.org/wiki/L-system).
"""


import turtle

def symbolMeaning(symbol):
    if symbol == 'X':
        return 'F+[[X]-X]-F[-FX]+X'
    elif symbol == 'F':
        return 'FF'
    elif symbol == '[':
        return '['
    elif symbol =='+':
        return '+'
    elif symbol == '-':
        return '-'
    elif symbol == ']':
        return ']'

def symbolDrawing(symbol,tur,pos,ang):
    if symbol == 'F':
        tur.forward(20)
    elif symbol == '[':
        pos.append(tur.position())
        ang.append(tur.heading())
    elif symbol =='+':
        tur.left(25)
    elif symbol == '-':
        tur.right(25)
    elif symbol == ']':
        tur.up()
        tur.setposition(pos.pop())
        tur.down()
        tur.setheading(ang.pop())
    

def phraseMeaning(phrase,tur):
    newPhrase = ''
    for i in range(len(phrase)):
        ret = symbolMeaning(phrase[i])
        newPhrase += ret
    return newPhrase

#repeat phase meaning, then draw the system
def doRepeatedly(phrase,tur,num):
    ang = []
    pos = []
    while num > 0:
        newPhrase = phraseMeaning(phrase,tur)
        num-=1
        phrase = newPhrase
    for i in phrase:
        symbolDrawing(i,tur,pos,ang)

def theGrowingPlant(phrase,tur,num):
    ang = []
    pos = []
    while num > 0:
        newPhrase = phraseMeaning(phrase,tur)
        num-=1
        phrase = newPhrase
    for i in newPhrase:
        symbolDrawing(i,tur,pos,ang)

while True:
    try:
        MAX_NUMBER_OF_BRANCHES = int(input("Max number of branches (2 < nr < 9): "))
        if MAX_NUMBER_OF_BRANCHES < 2:
            raise Exception()
        break
    except:
        print("Please give an integer number!")

#calculate the sides of the fram we want to display the tree into
sides = 50
mul = 5/3
for i in range(MAX_NUMBER_OF_BRANCHES - 1):
    
    if i < 6:
        mul += 1/(i*2 + 4)
    else:
        mul = 1
    sides = int(sides * mul)
win = turtle.Screen()
win.setworldcoordinates(-sides,-sides,sides,sides)
win.tracer(10000)
t = turtle.Turtle()
t.left(60)
t.up()
t.goto(-sides,-sides)
t.down()
doRepeatedly('X',t,MAX_NUMBER_OF_BRANCHES)
win.exitonclick()
