import turtle

# Function to execute the pseudocode commands using the Turtle module
def draw_pseudocode(pseudocode):
    # Split the pseudocode by lines to process each command
    commands = pseudocode.split('\n')
    
    # Create a turtle object
    t = turtle.Turtle()
    screen = turtle.Screen()
    t.speed(1)  # Set the speed of the turtle

    # Initialize an empty list to hold repeat block commands
    repeat_commands = []
    repeating = False

    # Loop through each command and execute it
    for command in commands:
        command = command.strip()
        if not command:
            continue  # Skip any empty lines

        if repeating:
            if command == ']':
                # End of repeat block, execute all commands within the block
                for _ in range(repeat_times):
                    for repeat_command in repeat_commands:
                        do_command(t, repeat_command)
                # Reset the repeat command list and flag
                repeat_commands = []
                repeating = False
            else:
                # Inside a repeat block, collect commands
                repeat_commands.append(command)
        else:
            if command.startswith('repeat'):
                parts = command.split()
                repeat_times = int(parts[1])
                repeating = True  # Set the flag that we are inside a repeat block
            else:
                # Execute a single command
                do_command(t, command)
    
    # Hide the turtle and display the result
    t.hideturtle()
    screen.mainloop()  # Keep the window open until it is clicked

# Function to execute a single command
def do_command(turtle_obj, command):
    parts = command.split()
    action = parts[0]
    if len(parts) > 1:
        value = float(parts[1])

    if action == 'forward':
        turtle_obj.forward(value)
    elif action == 'back':
        turtle_obj.backward(value)
    elif action == 'left':
        turtle_obj.left(value)
    elif action == 'right':
        turtle_obj.right(value)
    elif action == 'penup':
        turtle_obj.penup()
    elif action == 'pendown':
        turtle_obj.pendown()

# Run the drawing function with the pseudocode
pseudocode = """left 90
forward 15
repeat 9 [
  forward 4.5
  left 20
]
forward 10
repeat 9 [
  forward 4.5
  right 20
]
forward 25
penup
back 50
pendown
right 90
forward 50
back 25
right 45
forward 35
back 35
right 90
forward 35
back 35
right 45
forward 25
penup
left 90
forward 40
left 90
forward 50
pendown
right 135
forward 35
left 90
forward 35
back 35
right 135
forward 25
penup
back 25
left 90
forward 30
pendown
forward 20
penup
forward 40
pendown
right 90
forward 25
back 50
right 90
forward 25
back 50
penup
right 180
forward 10
right 90
pendown
forward 30
repeat 60 [
  forward 1
  left 3
]
forward 30
penup
right 90
forward 20
right 90
pendown
forward 50
back 50
left 90
forward 5
repeat 9 [
  forward 5
  right 20
]
forward 10
left 135
forward 30
left 45
penup
forward 20
pendown
left 90
forward 50
back 50
right 90
forward 25
penup
forward 10
left 90
forward 25
right 90
pendown
forward 20
penup
forward 30
right 90
pendown
forward 25
back 50
left 90
penup
forward 30
pendown
repeat 150 [
  forward 0.75
  right 3
]
right 15
forward 40
left 105
penup
forward 35
pendown
repeat 210 [
  forward 0.75
  left 3
]
left 170
forward 40
right 80
penup
forward 30
pendown
forward 25
right 100
forward 50
penup
left 10
forward 20
right 90
back 30
pendown
repeat 2 [
  forward 580
  right 90
  forward 90
  right 90
]
"""
draw_pseudocode(pseudocode)