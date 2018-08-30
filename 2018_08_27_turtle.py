import turtle
import random
import math

screen = turtle.Screen()  # creates screen and changes settings
screen.setup(1366, 768)
screen.colormode(255)
screen.tracer(2)

turtle_1_color = screen.textinput("Color", "Enter the color you want to draw with")  # asks user for pen color
draw_preset = False


# draw_preset = screen.textinput("Draw Preset Design",  # draws special design if "Y" or "y" is entered
#                                "Enter (Y) if you want to draw some preset designs or (N) if you don't want to: ")
# if str(draw_preset) == "Y" or str(draw_preset) == "y":
#     draw_preset = True
# else:
#     draw_preset = False


def turtle_settings(trt_one, trt_two, trt_three):  # takes turtles and sets them up for user
    trt_three.penup()
    trt_three.goto(0, -320)  # draws the circle that is used for special design
    trt_three.pendown()
    trt_three.circle(20)
    trt_three.hideturtle()

    trt_two.penup()
    trt_two.goto(0, -300)  # draws the special design in random colors
    trt_two.pendown()
    trt_two.speed(0)
    trt_two.pencolor(random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))
    trt_two.hideturtle()

    trt_one.penup()
    trt_one.goto(0, 0)
    trt_one.pendown()  # user controlled drawing tool
    trt_one.speed(0)
    trt_one.pencolor(turtle_1_color)
    trt_one.shape("arrow")
    trt_one.resizemode("triangle")
    trt_one.shapesize(.25, .25, .25)
    return 0, -300


def mouse_coordinates(x, y):  # receives the x and y coordinates of a click
    turtle_1.penup()
    turtle_1.goto(x, y)
    turtle_1.pendown()
    print(x)
    print(y)
    if math.sqrt((x - 0) ** 2 + (y - -300) ** 2) <= 20:
        return x, y, True, True


def use_pen():  # "space" key makes the user controlled turtle switch between drawing or not
    if turtle_1.isdown():
        turtle_1.penup()
    else:
        turtle_1.pendown()


def clear_pen():  # "z" key clears all drawing except circle at bottom
    turtle_1.clear()
    if draw_preset:
        turtle_2.clear()


def random_color():  # "x" key change turtle to a random color
    turtle_1.pencolor(random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))
    print(coor_x)


def change_color():  # "c" key asks user to enter color to change turtle to
    trt_1_color = screen.textinput("Color", "Enter the color you want to draw with")
    turtle_1.pencolor(trt_1_color)


turtle_1 = turtle.Turtle()
turtle_2 = turtle.Turtle()
turtle_3 = turtle.Turtle()

secret_x, secret_y = turtle_settings(turtle_1, turtle_2, turtle_3)
turtle_1.ondrag(turtle_1.goto)


if draw_preset:  # draws some special designs
    for i in range(1, 101):
        turtle_2.circle(200 - 2 * i)
    turtle_2.pencolor(random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))
    for i in range(1, 101):
        turtle_2.circle(400 - 2 * i)

screen.onkey(use_pen, "space")  # different keys that help draw
screen.onkey(clear_pen, "z")
screen.onkey(random_color, "x")
screen.onkey(change_color, "c")
screen.onclick(mouse_coordinates)

screen.listen()
screen.update()
screen.mainloop()
