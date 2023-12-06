import turtle as trtl
from math import sin, cos, radians
import os
import time

# constants
SUN_RADIUS = 30
SUPERNOVA_DURATION = 50

# globals
simulation_running = False
supernova_forming = False
time_since_supernova = 0
blackhole_formed = False

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

########################################################
# TURTLE INITIALIZATION
########################################################
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
trtl.register_shape("images/Sun.gif")
sun = trtl.Turtle(shape="images/Sun.gif")
sun.speed(0)
sun.color("yellow")
sun.penup()
sun.shapesize(3)

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
    try:
        s = f"images/{planet[0]}.gif"
        trtl.register_shape(s)
        p.shape(s)
    except:
        pass
    p.hideturtle()
    p.speed(-100)
    p.penup()
    p.shapesize(planet[4])
    p.color(planet[2])
    planet[1] = p
    planet.append(True)

    # initialize the turtle objects for each moon of the planet
    for moon in planet[6]:
        m = trtl.Turtle(shape="circle")
        m.hideturtle()
        m.speed(0)
        m.penup()
        m.shapesize(moon[2])
        m.color("gray")
        moon[0] = m


# create asteroid
asteroid_gravity_radius = 50
asteroid_enabled = False
caught_planets = []

trtl.register_shape("images/Asteroid.gif")
asteroid = trtl.Turtle(shape = "images/Asteroid.gif")
asteroid.hideturtle()
asteroid.speed(0)
asteroid.penup()
asteroid.goto(250,250)
asteroid.setheading(225)

# initialize the black hole turtle
trtl.register_shape("images/Blackhole.gif")
blackhole = trtl.Turtle("images/Blackhole.gif")
blackhole.hideturtle()
blackhole.penup()
blackhole.speed(0)
########################################################



########################################################
# TEXT-WRITING UTILS
########################################################
# write the status of each planet on the screen
writing_status = False
def write_status(w=False):
    global writing_status, blackhole_formed

    writer.penup()
    if not w:
        writer.clear()
    for i in range(len(planets)):
        planet = planets[i]

        writer.penup()
        writer.goto(-500, 150 - (i * 20))
        writer.pendown()
        font = ("Arial", 14, "normal")
        if planet[7] and not blackhole_formed:
            writer.color("green")
            writer.write(f"{planet[0]} [{str(i + 1)}]: On", align="left", font=font)
        else:
            text = f"{planet[0]} [{str(i + 1)}]: Off"
            if blackhole_formed:
                text = f"{planet[0]}: Demolished in black hole"
            writer.color("red")
            writer.write(text, align="left", font=font)
    if not w and not blackhole_formed:
        write_speed(True)
    writing_status = False

# write the speed of each planet on the screen
def write_speed(w=False):
    writer.penup()
    writer.color("gold")
    writer.goto(-500, 0)
    writer.pendown()
    if not w:
        writer.clear()
    writer.write(f"Speed: {simulation_speed}x", align="left", font=("Arial", 14, "normal"))
    if not w:
        write_status(True)
########################################################



########################################################
# KEYBINDS TO MODIFY SIMULATION
########################################################
# function to listen to key presses in the turtle window
screen.listen()

# allow custom speed when they press the enter button
def custom_speed():
    global simulation_speed, simulation_running, blackhole_formed

    if not simulation_running or blackhole_formed:
        return

    # prompt the user for a simulation speed, and keep asking
    # until they give a valid integer input
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

# do 10x speed change if they are holding down control/command
# (depends on if they are on MacOS or Windows)
ctrl = False
def ctrl_down():
    global ctrl
    ctrl = True
def ctrl_up():
    global ctrl
    ctrl = False
key_name = "Meta_L" if os.name == "posix" else "Control_L"
screen.onkeypress(ctrl_down, key_name)
screen.onkeyrelease(ctrl_up, key_name)

# speed up the simulation
def speedup():
    global simulation_speed, writing_status, blackhole_formed
    if writing_status or blackhole_formed:
        return
    writing_status = True
    simulation_speed += 1 * (10 if ctrl else 1)
    write_speed()
screen.onkey(speedup, "Up")

# slow down the simulation
def slowdown():
    global simulation_speed, writing_status, blackhole_formed
    if writing_status or blackhole_formed:
        return
    writing_status = True
    simulation_speed -= 1 * (10 if ctrl else 1)
    write_speed()
screen.onkey(slowdown, "Down")

# adds the event listener for a key
def add_listener(n):
    def handler():
        global writing_status, blackhole_formed
        if writing_status or blackhole_formed:
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

    screen.onkey(handler, str(n + 1))

# allow user to enable/disable planets using the numbers 1 to length of planets
for n in range(len(planets)):
    add_listener(n)

def run_asteroid():
    global asteroid_enabled
    if not simulation_running or asteroid_enabled:
        return
    asteroid_enabled = True
    asteroid.showturtle()
screen.onkey(run_asteroid, "a")
########################################################



########################################################
# MAIN LOOP
########################################################
# main loop that will go forever until asteroid wrecks everything
i = 0
while True:
    angle = i * simulation_speed # changes the speed of the objects
    orbiting_planets = list.copy(planets)

    if "Sun" in caught_planets:
        orbiting_planets.append(["Sun", sun, "yellow", None, None, 1, [], False])

    # for each planet, move to position calculated from current angle, with the sun as the center
    # using trig functions (FYI, python math only accepts radians, not degrees)
    for j in range(len(orbiting_planets)):
        planet = orbiting_planets[j]
        x = None
        y = None
        if planet[0] not in caught_planets:
            origin = planet[3]
            if supernova_forming:
                origin *= (1 - (time_since_supernova / SUPERNOVA_DURATION))
            x = origin * sin(radians(angle * planet[5])) + sun.xcor()
            y = origin * cos(radians(angle * planet[5])) + sun.ycor()
        else:
            origin = 100
            if supernova_forming:
                origin *= (1 - (time_since_supernova / SUPERNOVA_DURATION))
            x = origin * sin(radians(angle * planet[5] * 4)) + asteroid.xcor()
            y = origin * cos(radians(angle * planet[5] * 4)) + asteroid.ycor()
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
            elif time_since_supernova >= SUPERNOVA_DURATION:
                moon[0].hideturtle()
        if i == 0:
            planet[1].showturtle()
        elif time_since_supernova >= SUPERNOVA_DURATION:
            planet[1].hideturtle()

        if asteroid_enabled:
            if abs(planet[1].xcor() - asteroid.xcor()) < asteroid_gravity_radius and abs(planet[1].ycor() - asteroid.ycor()) < asteroid_gravity_radius and planet[0] not in caught_planets:
                caught_planets.append(planet[0])
            elif abs(asteroid.xcor()) < asteroid_gravity_radius and abs(asteroid.ycor()) < asteroid_gravity_radius and "Sun" not in caught_planets:
                caught_planets.append("Sun")
                supernova_forming = True
    # also delete the loading text if this is the first iteration
    if i == 0:
        simulation_running = True
        writer.clear()
        write_status()
    elif time_since_supernova >= SUPERNOVA_DURATION:
        blackhole.goto(asteroid.xcor(), asteroid.ycor())
        asteroid.hideturtle()
        blackhole.showturtle()
        break

    if asteroid_enabled:
        asteroid.forward(5 + min(max(simulation_speed, 0), 8))
    if supernova_forming:
        time_since_supernova += 1
    i += 1

# write status again now that supernova has exploded
simulation_running = False
blackhole_formed = True
write_status()
########################################################

# start screen updates
screen.mainloop()