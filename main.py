import turtle as trtl
from math import sin, cos, radians

# constants
SUN_RADIUS = 30
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

# planet name, turtle object, color, distance from sun, size, speed, moons list, enabled
# for each moon: turtle object, distance from planet, size, speed
planets = [
    ["mercury", None, "#824a42", 50, 0.6, 2.75, []],
    ["venus", None, "red", 85, 1.4, 1.25, []],
    ["earth", None, "green", 145, 1.75, 0.75, [[None, 40, 0.6, 3]]],
    ["mars", None, "orange", 200, 1.2, 0.5, [[None, 30, 0.6, 4], [None, 50, 0.4, 2]]],
    ["jupiter", None, "#c7a06d", 260, 2.75, 0.25, [[None, 35, 0.2, 0.7], [None, 45, 0.3, -1], [None, 55, 0.4, 1.25]]],
    ["neptune", None, "blue", 325, 0.8, 0.1, []]
]

# initialize the turtle objects for each planet
for planet in planets:
    p = trtl.Turtle(shape="circle")
    p.hideturtle()
    p.speed(-100)
    p.penup()
    p.shapesize(planet[4])
    p.color(planet[2])
    planet[1] = p
    planet.append(True)

    # initialize the turtle objects for each moon
    for moon in planet[6]:
        m = trtl.Turtle(shape="circle")
        m.hideturtle()
        m.speed(0)
        m.penup()
        m.shapesize(moon[2])
        m.color("gray")
        moon[0] = m


# allow user to change simulation speed using arrow keys
screen.listen()
def writespeed():
    writer.clear()
    writer.write(f"Speed: {simulation_speed}", align="center", font=("Arial", 18, "normal"))
def speedup():
    global simulation_speed
    simulation_speed += 1
    writespeed()
def slowdown():
    global simulation_speed
    simulation_speed -= 1
    writespeed()
screen.onkey(speedup, "Up")
screen.onkey(slowdown, "Down")

def toggle_planet(n):
    print("got here", n)
    if planets[n][7]:
        planets[n][7] = False
        planets[n][1].hideturtle()
        for moon in planets[n][6]:
            moon[0].hideturtle()
    else:
        planets[n][7] = True
        planets[n][1].showturtle()
        for moon in planets[n][6]:
            moon[0].showturtle()

# allow user to enable/disable planets
for n in range(len(planets)):
    screen.onkey(lambda: toggle_planet(n), str(n + 1))

# main loop that will go until we have orbited MAX_ORBITS times
for i in range(360 * MAX_ORBITS):
    angle = (i % 360) * simulation_speed # changes the speed of the objects

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
        writespeed()

# start screen updates
screen.mainloop()