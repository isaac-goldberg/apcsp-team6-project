import turtle as trtl
from math import sin, cos, radians

# constants
SUN_RADIUS = 50
MAX_ORBITS = 100

# prompt the user for an animation speed,
# and keep asking them until they give a valid integer input
simulation_speed = input("Enter the speed (integer) to run the simulation at: ")
while type(simulation_speed) is not int:
    try:
        simulation_speed = int(simulation_speed)
    except:
        simulation_speed = input("Invalid input, must be an integer. Try again: ")

# the screen that will be drawn on - initialize it here so that we can
# give the entire screen a black background before rendering anything else
screen = trtl.Screen()
screen.bgcolor("black")

# turtle that will write the loading screen text
writer = trtl.Turtle()
writer.speed(0)
writer.hideturtle()
writer.penup()
writer.goto(0, -300)
writer.color("white")
writer.pendown()
writer.write("Loading...", align="center", font=("Arial", 24, "normal"))

# initialize sun turtle,
# and draw the sun so that its center is in the exact center of the screen
sun = trtl.Turtle()
sun.hideturtle()
sun.speed(0)
sun.color("yellow")
sun.penup()
sun.goto(0, -SUN_RADIUS)
sun.pendown()
sun.begin_fill() # this will fill in the circle, instead of just being an outline
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

# initialize the turtle objects for each planet
for planet in planets:
    p = trtl.Turtle(shape="circle")
    p.hideturtle()
    p.speed(0)
    p.penup()
    p.shapesize(planet[4])
    p.color(planet[2])
    planet[1] = p

    # initialize the turtle objects for each moon
    for moon in planet[6]:
        m = trtl.Turtle(shape="circle")
        m.hideturtle()
        m.speed(0)
        m.penup()
        m.shapesize(moon[2])
        m.color("gray")
        moon[0] = m

# main loop that will go until we have orbited MAX_ORBITS times
for i in range(360 * MAX_ORBITS):
    angle = i * simulation_speed # changes the speed of the objects

    # for each planet, move to position calculated from current angle, with the sun as the center
    # using trig functions (FYI, python math only accepts radians, not degrees)
    for planet in planets:
        x = planet[3] * sin(radians(angle * planet[5]))
        y = planet[3] * cos(radians(angle * planet[5]))
        planet[1].goto(x, y)

        # for each moon of the planet (if any),
        # move to position calculated from angle, with the planet as the center
        for moon in planet[6]:
            mx = moon[1] * sin(radians(angle * moon[3])) + planet[1].xcor()
            my = moon[1] * cos(radians(angle * moon[3])) + planet[1].ycor()
            moon[0].goto(mx, my)

            # if this is the first iteration, reveal all the planets and moons
            if i == 0:
                moon[0].showturtle()
        if i == 0:
            planet[1].showturtle()
    # also delete the loading text if this is the first iteration
    if i == 0:
        writer.clear()

# start screen updates
screen.mainloop()