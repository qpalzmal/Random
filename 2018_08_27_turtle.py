import turtle
import random
import math

screen = turtle.Screen()  # creates screen and changes settings
screen.setup(1366, 768)
screen.colormode(255)
screen.tracer(2)

turtle_1_color = screen.textinput("Color", "Enter the color you want to draw with")  # asks user for pen color
draw_preset = False


# draw_preset = screen.textinput("Draw Preset Design",
#                                "Enter (Y) if you want to draw some preset designs or (N) if you don't want to: ")
# if str(draw_preset) == "Y" or str(draw_preset) == "y":
#     draw_preset = True
# else:
#     draw_preset = False


def turtle_settings(trt_one, trt_two):  # takes turtles and sets them up for user
    trt_two.penup()
    trt_two.goto(0, -320)
    trt_two.pendown()
    trt_two.circle(20)
    trt_two.penup()
    trt_two.goto(0, -300)
    trt_two.pendown()
    trt_two.speed(0)
    trt_two.pencolor(random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))
    trt_two.hideturtle()

    trt_one.penup()
    trt_one.goto(0, 0)
    trt_one.pendown()
    trt_one.speed(0)
    trt_one.pencolor(turtle_1_color)
    trt_one.shape("triangle")
    trt_one.shapesize(.5, .5, .5)
    return 0, -300


def get_mouse_coordinates(x, y):  # receives the x and y coordinates of a click
    print(x)
    print(y)
    if math.sqrt((x - 0) ** 2 + (y - -300) ** 2) <= 20:
        print("test")


def use_pen():
    if turtle_1.isdown():
        turtle_1.penup()
    else:
        turtle_1.pendown()


def clear_pen():
    turtle_1.clear()


def random_color():
    turtle_1.pencolor(random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))


turtle_1 = turtle.Turtle()
turtle_2 = turtle.Turtle()

secret_x, secret_y = turtle_settings(turtle_1, turtle_2)
turtle_1.ondrag(turtle_1.goto)


if draw_preset:
    for i in range(1, 100):
        turtle_2.circle(200 - 2 * i)  # draws some special designs
    for i in range(1, 100):
        turtle_2.circle(400 - 2 * i)

screen.onkey(use_pen, "space")
screen.onkey(clear_pen, "z")
screen.onkey(random_color, "x")
screen.onclick(get_mouse_coordinates)
screen.listen()
screen.update()
screen.mainloop()

