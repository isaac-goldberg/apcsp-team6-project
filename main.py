import turtle as trtl
from math import sin, cos, radians

SUN_RADIUS = 50
MAX_ORBITS = 100

simulation_speed = input("Enter the speed (integer) to run the simulation at: ")
while type(simulation_speed) is not int:
    try:
        simulation_speed = int(simulation_speed)
    except:
        simulation_speed = input("Invalid input, must be an integer. Try again: ")

wn = trtl.Screen()
wn.bgcolor("black")

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

# planet name, turtle object, color, distance from sun, size, speed, moons list
# for each moon: turtle object, distance from planet, size, speed
planets = [
    ["mercury", None, "#824a42", 80, 0.6, 3.5, []],
    ["venus", None, "red", 120, 1.4, 1.5, []],
    ["earth", None, "green", 175, 2, 1, [[None, 40, 0.75, 3]]],
    ["mars", None, "orange", 275, 1.2, 0.5, [[None, 30, 0.8, 4], [None, 50, 0.6, 2]]]
]

for planet in planets:
    p = trtl.Turtle(shape="circle")
    p.hideturtle()
    p.speed(0)
    p.penup()
    p.shapesize(planet[4])
    p.color(planet[2])
    planet[1] = p

    for moon in planet[6]:
        m = trtl.Turtle(shape="circle")
        m.hideturtle()
        m.speed(0)
        m.penup()
        m.shapesize(moon[2])
        m.color("gray")
        moon[0] = m

for i in range(360 * MAX_ORBITS):
    angle = i * simulation_speed
    for planet in planets:
        x = planet[3] * sin(radians(angle * planet[5]))
        y = planet[3] * cos(radians(angle * planet[5]))
        planet[1].goto(x, y)

        for moon in planet[6]:
            mx = moon[1] * sin(radians(angle * moon[3])) + planet[1].xcor()
            my = moon[1] * cos(radians(angle * moon[3])) + planet[1].ycor()
            moon[0].goto(mx, my)

            if angle == 0:
                moon[0].showturtle()
        if angle == 0:
            planet[1].showturtle()

wn.mainloop()