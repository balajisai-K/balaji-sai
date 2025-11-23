import turtle
import time
import random

# --- Global Variables ---
DELAY = 0.1
SCORE = 0
HIGH_SCORE = 0

# --- Setup the Screen (Window) ---
window = turtle.Screen()
window.title("Classic Snake Game")
window.bgcolor("green")
window.setup(width=600, height=600)
window.tracer(0) # Turns off the screen updates

# --- Snake Head ---
head = turtle.Turtle()
head.speed(0) # Animation speed (0 is fastest)
head.shape("square")
head.color("black")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# --- Snake Food ---
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# --- Scoreboard Pen ---
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write(f"Score: {SCORE}  High Score: {HIGH_SCORE}", align="center", font=("Courier", 24, "normal"))

# --- Snake Segments List ---
segments = []

# --- Functions for Movement ---
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

def reset_game():
    global SCORE, HIGH_SCORE, DELAY
    time.sleep(1)
    head.goto(0, 0)
    head.direction = "stop"

    # Hide the segments
    for segment in segments:
        segment.goto(1000, 1000)
    
    # Clear the segments list
    segments.clear()

    # Reset score and delay
    SCORE = 0
    DELAY = 0.1
    
    # Update score display
    pen.clear()
    pen.write(f"Score: {SCORE}  High Score: {HIGH_SCORE}", align="center", font=("Courier", 24, "normal"))


# --- Keyboard Bindings ---
window.listen()
window.onkeypress(go_up, "w")
window.onkeypress(go_down, "s")
window.onkeypress(go_left, "a")
window.onkeypress(go_right, "d")
# Also bind to arrow keys for convenience
window.onkeypress(go_up, "Up")
window.onkeypress(go_down, "Down")
window.onkeypress(go_left, "Left")
window.onkeypress(go_right, "Right")


# --- Main Game Loop ---
while True:
    window.update() # Manually update the screen

    # Check for Border Collision (Game Over)
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        reset_game()

    # Check for Food Collision
    if head.distance(food) < 20:
        # Move the food to a random spot
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

        # Add a new segment to the snake
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)

        # Shorten the delay (increase speed)
        DELAY -= 0.001

        # Increase the score
        SCORE += 10
        if SCORE > HIGH_SCORE:
            HIGH_SCORE = SCORE
        
        # Update the score display
        pen.clear()
        pen.write(f"Score: {SCORE}  High Score: {HIGH_SCORE}", align="center", font=("Courier", 24, "normal"))

    # Move the end segments first in reverse order
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move() # Move the snake head

    # Check for Self-Collision
    for segment in segments:
        if segment.distance(head) < 20:
            reset_game()

    # Pause for the delay
    time.sleep(DELAY)

window.mainloop()