import turtle #i.e. in 11
draw = turtle.Turtle() #i.e. in 11

# get number of sides from user
while True:
    sides = input("Enter number of sides : ")
    if not sides.isdigit():
        print("Please enter a valid number")
        continue
    no_of_sides = int(sides)
    if no_of_sides >= 3:
        break
    else:
        print("You need atleast 3 sides for a polygon. Enter valid number.")
        continue

# get length from user
while True:
    length = input("Enter side length : ")
    if not length.isdigit():
        print("Please enter a valid number")
        continue
    side_length = int(length)
    break

#get depth from user
while True:
    depth = input("Enter recursion depth : ")
    if not depth.isdigit():
        print("Please enter a valid number")
        continue
    recursion_depth = int(depth)
    break


def recuring_shape(depth):
    if depth == 0:
        draw.forward(side_length/3) #i.e. in 11
    else:
        recuring_shape(depth - 1)
        draw.right(60) #i.e. in 11
        recuring_shape(depth - 1)
        draw.left(120) #i.e. in 11
        recuring_shape(depth - 1)
        draw.right(60) #i.e. in 11
        recuring_shape(depth - 1)


for side_num in range(int(no_of_sides)):
    recuring_shape(recursion_depth)
    draw.right(360 / no_of_sides) #i.e. in 11

turtle.done() #i.e. in 11
