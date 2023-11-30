import turtle as trtl
import math

wn = trtl.Screen()
wn.bgcolor("black")

SUN_RADIUS = 50
EARTH_DISTANCE_FROM_SUN = 200
MOON_DISTANCE_FROM_EARTH = 45
TOTAL_REVOLUTIONS = 2

# initialize sun turtle
sun = trtl.Turtle()
sun.hideturtle()
sun.speed(0)
sun.color("yellow")
sun.penup()
# draw the sun so that the center is exactly in the center of the screen
sun.goto(0, -SUN_RADIUS)
sun.pendown()
sun.begin_fill()
sun.circle(radius=SUN_RADIUS, steps=64)
sun.end_fill()

# initialize earth turtle
earth = trtl.Turtle(shape="circle")
earth.hideturtle()
earth.speed(0)
earth.penup()
earth.shapesize(1.5)
earth.color("green")

# initialize moon turtle
moon = trtl.Turtle(shape="circle")
moon.hideturtle()
moon.speed(0)
moon.penup()
moon.shapesize(0.75)
moon.color("grey")

for i in range(360 * TOTAL_REVOLUTIONS):
    ex = EARTH_DISTANCE_FROM_SUN * math.sin(math.radians(i))
    ey = EARTH_DISTANCE_FROM_SUN * math.cos(math.radians(i))
    earth.goto(ex, ey)

    mx = MOON_DISTANCE_FROM_EARTH * math.sin(math.radians(i * 2.75)) + earth.xcor()
    my = MOON_DISTANCE_FROM_EARTH * math.cos(math.radians(i * 2.75)) + earth.ycor()
    moon.goto(mx, my)

    if i == 0:
        earth.showturtle()
        earth.speed(5)
        moon.showturtle()
        moon.speed(5)

wn.mainloop()