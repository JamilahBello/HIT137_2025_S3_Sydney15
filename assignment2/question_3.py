# starting out
import turtle
draw = turtle.Turtle()

no_of_sides = int(input("Enter number of sides : "))
side_length = 10
# input("Enter side length : ")
recursion_depth = int(input("Enter recursion depth : "))

def recuring_shape(depth):
    if depth == 0 :
        draw.forward(side_length)
        return()
    
    recuring_shape(depth-1)
    draw.forward(side_length)
    draw.right(60)
    draw.forward(side_length)
    draw.left(120)
    draw.forward(side_length)
    draw.right(60)

    recuring_shape(depth-1)


for side_num in range(int(no_of_sides)):
    recuring_shape(0)
    draw.right(90)




turtle.done()
