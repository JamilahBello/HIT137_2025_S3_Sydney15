# starting out
import turtle

draw = turtle.Turtle()

while True:
    sides = input("Enter number of sides : ")
    if not sides.isdigit():  # https://realpython.com/python-not-operator/
        print("Please enter a  number")
        continue
    no_of_sides = int(sides)
    if no_of_sides >= 3:
        break
    else:
        print("You need atleast 3 sides for a polygon. Enter valid number.")
        continue

while True:
    length = input("Enter side length : ")
    if not length.isdigit():
        print("Please enter a number")
        continue
    side_length = int(length)
    break

while True:
    depth = input("Enter recursion depth : ")
    if not depth.isdigit():
        print("Please enter a number")
        continue
    recursion_depth = int(depth)
    break


def recuring_shape(depth):
    if depth == 0:
        draw.forward(side_length)
    else:
        recuring_shape(depth - 1)
        draw.right(60)
        recuring_shape(depth - 1)
        draw.left(120)
        recuring_shape(depth - 1)
        draw.right(60)
        recuring_shape(depth - 1)


for side_num in range(int(no_of_sides)):
    recuring_shape(recursion_depth)
    draw.right(360 / no_of_sides)

turtle.done()
