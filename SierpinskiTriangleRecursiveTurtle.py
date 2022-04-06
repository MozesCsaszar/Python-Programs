"""
A program to draw a Fractal Sierpinski Triangle.
"""

import turtle


def drawTriang(points,t,col):
    t.fillcolor(col)
    t.begin_fill()
    t.goto(points[1][0],points[1][1])
    t.goto(points[2][0],points[2][1])
    t.goto(points[0][0],points[0][1])
    t.end_fill()

def doStuff(points,n,t,colors):
    if n >= 1:
        t.up()
        t.goto(points[0][0],points[0][1])
        t.down()
        drawTriang(points,t,colors[9-n])
        doStuff([points[0],[(points[0][0]+points[1][0])//2,(points[0][1]+points[1][1])//2],[(points[0][0]+points[2][0])//2,(points[0][1]+points[2][1])//2]],n-1,t,colors)
        doStuff([ [(points[0][0]+points[2][0])//2,(points[0][1]+points[2][1])//2],[(points[1][0]+points[2][0])//2,(points[1][1]+points[2][1])//2],points[2] ],n-1,t,colors)
        doStuff([ [(points[0][0]+points[1][0])//2,(points[0][1]+points[1][1])//2] , points[1], [(points[1][0]+points[2][0])//2,(points[1][1]+points[2][1])//2] ],n-1,t,colors)

t = turtle.Turtle()
t.speed(7)
colors = ['blue','red','green','white','yellow','pink','Dark Violet','orange','black']

win = turtle.Screen()
win.setworldcoordinates(-600, -600, 600, 600)
win.tracer(1000,0)
points = [[-540,-468],[540,-468],[0,468]]
doStuff(points,7,t,colors)
win.exitonclick()
