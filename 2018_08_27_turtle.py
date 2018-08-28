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


def turtle_settings(one, two, three):  # takes turtles and sets them up for use
    function_list = [one, two, three]
    for i in range(1, 3):
        function_turtle = function_list[i]
        function_turtle.penup()
        function_turtle.goto(0, -300)
        function_turtle.pendown()
        function_turtle.speed(0)
        function_turtle.pencolor(random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))
        function_turtle.hideturtle()
    one.penup()
    one.goto(0, -320)
    x, y = one.xcor(), one.ycor()
    one.pendown()
    one.circle(20)
    one.penup()
    one.goto(0, 0)
    one.pendown()
    one.speed(0)
    one.pencolor(turtle_1_color)
    one.shape("triangle")
    one.shapesize(2, 2, 2)
    return x, y


def get_mouse_coordinates(x, y):  # receives the x and y coordinates of a click
    mouse_x = x
    mouse_y = y
    print(mouse_x)
    print(mouse_y)
    if math.sqrt((0 - mouse_x) ** 2 + (-320 - mouse_y) ** 2) < 20:
        print("reeee")
        return True


# def show_clicks():
#     print(clicks)
#     print(len(clicks))
#     print(clicks[0])
#     print(clicks[1])
#     clicks.clear()


turtle_1 = turtle.Turtle()
turtle_2 = turtle.Turtle()
turtle_3 = turtle.Turtle()

secret_x, secret_y = turtle_settings(turtle_1, turtle_2, turtle_3)
turtle_1.ondrag(turtle_1.goto)



if screen.onclick(get_mouse_coordinates):
    for i in range(1, 100):
        turtle_2.circle(200 - 2 * i)
    for i in range(1, 100):
        turtle_3.circle(400 - 2 * i)

# screen.onkey(show_clicks, "a")
screen.onclick(get_mouse_coordinates)
screen.listen()
screen.update()
screen.mainloop()


# test