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
    ["Mercury", None, "#824a42", 50, 0.6, 2.75, []],
    ["Venus", None, "red", 85, 1.4, 1.25, []],
    ["Earth", None, "green", 145, 1.75, 0.75, [[None, 30, 0.6, 3]]],
    ["Mars", None, "orange", 200, 1.2, 0.5, [[None, 25, 0.5, 4], [None, 40, 0.4, 2]]],
    ["Jupiter", None, "#c7a06d", 270, 2.75, 0.25, [[None, 35, 0.2, 0.7], [None, 45, 0.3, -1], [None, 55, 0.4, 1.25]]],
    ["Neptune", None, "blue", 325, 0.8, 0.1, []]
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

def custom_speed():
    global simulation_speed
    custom = trtl.textinput("Custom Speed", "Enter an integer:")
    while type(custom) is not int:
        try:
            custom = int(custom)
            simulation_speed = custom
            write_status()
        except:
            custom = trtl.textinput("Custom Speed", "Not a valid integer, try again:")
            if custom is None:
                break
    screen.listen()
screen.onkey(custom_speed, "Return")

ctrl = False
def ctrl_down():
    global ctrl
    ctrl = True
def ctrl_up():
    global ctrl
    ctrl = False
screen.onkeypress(ctrl_down, "Control_L")
screen.onkeyrelease(ctrl_up, "Control_L")

def write_speed(w=False):
    writer.penup()
    writer.color("gold")
    writer.goto(-500, 0)
    writer.pendown()
    if not w:
        writer.clear()
    writer.write(f"Speed: {simulation_speed}x", align="left", font=("Arial", 12, "normal"))
    if not w:
        write_status(True)
def speedup():
    global simulation_speed, writing_status
    if writing_status:
        return
    writing_status = True
    simulation_speed += 1 * (10 if ctrl else 1)
    write_speed()
def slowdown():
    global simulation_speed, writing_status
    if writing_status:
        return
    writing_status = True
    simulation_speed -= 1 * (10 if ctrl else 1)
    write_speed()
screen.onkey(speedup, "Up")
screen.onkey(slowdown, "Down")

writing_status = False
def write_status(w=False):
    global writing_status

    writer.penup()
    if not w:
        writer.clear()
    for i in range(len(planets)):
        planet = planets[i]

        writer.penup()
        writer.goto(-500, 150 - (i * 20), )
        writer.pendown()
        font = ("Arial", 12, "normal")
        if planet[7]:
            writer.color("green")
            writer.write(f"{planet[0]} [{str(i + 1)}]: On", align="left", font=font)
        else:
            writer.color("red")
            writer.write(f"{planet[0]} [{str(i + 1)}]: Off", align="left", font=font)
    if not w:
        write_speed(True)
    writing_status = False

def add_listener(n):
    def toggle():
        global writing_status
        if writing_status:
            return
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
        
        writing_status = True
        write_status()

    screen.onkey(toggle, str(n + 1))

# allow user to enable/disable planets
for n in range(len(planets)):
    add_listener(n)

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
        write_status()

# start screen updates
screen.mainloop()