# Aayan Arif - 24/06/2024
# Finished game

# imports
import turtle
import math
import winsound

# start the music
winsound.PlaySound("Mission.wav", winsound.SND_ASYNC | winsound.SND_LOOP)

# constants
WIDTH = 1000
HEIGHT = 600
SCORE_TO_WIN = 5

# mode variable
game_mode = "start" # Can be set to start, playing, end, garage, or help, affects the game loop

# custom color variables
color_one = "white"
color_two = "white"
selected_player = "one" # Can be one or two, used in order to change sprite colors in the garage

# mute variable
muted = False

# Set up the window
wn = turtle.Screen()
wn.title("Gamma Race")
wn.bgcolor("black")
wn.setup(WIDTH,HEIGHT)
wn.tracer(0)

# Set up the shape for the ship
s = turtle.Shape("compound") #note that the other parameters can be "polygons" or "image"
s.addcomponent([[0,20],[-18,-20],[-6,-12],[6,-12],[18,-20]], "", "white")
s.addcomponent([[0,5],[-5,-5],[5,-5]], "white")
turtle.register_shape("ship_white",s)

# Set up the shape for the orange ship
s = turtle.Shape("compound") #note that the other parameters can be "polygons" or "image"
s.addcomponent([[0,20],[-18,-20],[-6,-12],[6,-12],[18,-20]], "", "white")
s.addcomponent([[0,5],[-5,-5],[5,-5]], "orange")
turtle.register_shape("ship_orange",s)

# Set up the shape for the first player's custom colour ship
def custom_ship_one(color_one):
    s = turtle.Shape("compound") #note that the other parameters can be "polygons" or "image"
    s.addcomponent([[0,20],[-18,-20],[-6,-12],[6,-12],[18,-20]], "", "white")
    s.addcomponent([[0,5],[-5,-5],[5,-5]], color_one)
    turtle.register_shape("ship_custom_one",s)

    # Set up the shape for the ship when accelerating
    s = turtle.Shape("compound") #note that the other parameters can be "polygon" or "image"
    s.addcomponent([[0,20],[-18,-20],[-6,-12],[6,-12],[18,-20]], "", "white")
    s.addcomponent([[0,5],[-5,-5],[5,-5]], color_one)
    s.addcomponent([[-6,-12],[-3,-32],[0,-12]], "orange")
    s.addcomponent([[0,-12],[3,-32],[6,-12]], "orange")
    turtle.register_shape("ship_accel_one",s)

# Set up the shape for the second player's custom colour ship
def custom_ship_two(color_two):
    s = turtle.Shape("compound") #note that the other parameters can be "polygons" or "image"
    s.addcomponent([[0,20],[-18,-20],[-6,-12],[6,-12],[18,-20]], "", "white")
    s.addcomponent([[0,5],[-5,-5],[5,-5]], color_two)
    turtle.register_shape("ship_custom_two",s)

    # Set up the shape for the ship when accelerating
    s = turtle.Shape("compound") #note that the other parameters can be "polygon" or "image"
    s.addcomponent([[0,20],[-18,-20],[-6,-12],[6,-12],[18,-20]], "", "white")
    s.addcomponent([[0,5],[-5,-5],[5,-5]], color_two)
    s.addcomponent([[-6,-12],[-3,-32],[0,-12]], "orange")
    s.addcomponent([[0,-12],[3,-32],[6,-12]], "orange")
    turtle.register_shape("ship_accel_two",s)

# Create a turtle for the static elements
pen_main = turtle.Turtle()
pen_main.hideturtle()

# Create a pen for the sprites
pen_sprite = turtle.Turtle()
pen_sprite.penup()
pen_sprite.hideturtle()
pen_sprite.speed(0)

# Shape
shape = "classic"

# Sprite Class
class Sprite():
    def __init__(self):
        self.x = 0 # x position of self class
        self.y = 0 # y position of self class
        self.heading = 0 # heading
        self.dx = 0
        self.dy = 0
        self.shape = "square" # selects which sprite is used
        self.color = "white" # selects the colour
        self.size = 1.0 # default size
        self.active = True
    
    def render(self, pen):
        if self.active == True:
            pen.goto(self.x, self.y)
            pen.setheading(self.heading)
            pen.shapesize(self.size,self.size)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.stamp()
    
    def update(self):
        self.x += self.dx
        self.y += self.dy
    
    def is_collision(self, other):
        x = self.x - other.x
        y = self.y - other.y
        distance = ((x**2 + (y**2)) ** 0.5)
        if distance < ((10* self.size) + 10 * (self.size)):
            return True
        else:
            return False

# Player Class
class Player(Sprite):
    def __init__(self, shape_main, shape_accel):
        Sprite.__init__(self)
        self.shape_main = shape_main
        self.shape_accel = shape_accel
        self.shape = self.shape_main
        self.player = 1
        self.lap_marker_TL = False
        self.lap_marker_BR = False
        self.timer = 0
        self.score = 0
        self.rotating_left = False
        self.rotating_right = False
        self.accelerating = False
        self.color = "white"
    
    # Reset function
    def reset(self, xpos):
        self.score = 0
        self.x = xpos
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.lap_marker_TL = False
        self.lap_marker_BR = False
    
    # Movement functions
    def rotate_left_start(self):
        self.rotating_left = True
    def rotate_left_stop(self):
        self.rotating_left = False
    def rotate_right_start(self):
        self.rotating_right = True
    def rotate_right_stop(self):
        self.rotating_right = False
    def accelerate_start(self):
        self.accelerating = True
    def accelerate_stop(self):
        self.accelerating = False
    
    # Update function
    def update(self):
        self.x += self.dx
        self.y += self.dy

        # respond to key presses
        if self.rotating_left:
            self.heading += 0.5
        if self.rotating_right:
            self.heading -= 0.5
        if self.accelerating:
            self.shape = self.shape_accel
            self.timer = 50
            ax = math.cos(math.radians(self.heading))
            ay = math.sin(math.radians(self.heading))
            self.dx += ax * 0.002
            self.dy += ay * 0.002
        
        # Change the shape after accelerating
        if self.timer > 0:
            self.timer -= 1
            if self.timer == 0:
                self.shape = self.shape_main
        
        # Check for lap progress
        if self.x < -250 and self.y > 150:
            self.lap_marker_TL = True
        if self.x > 250 and self.y < -150:
            self.lap_marker_BR = True
        
        # Player 1 Finish Line
        if self.player == 1:
            if (self.y < -150) and (self.x > -5) and (self.x < 5):
                if (self.lap_marker_TL == True) and (self.lap_marker_BR == True):
                    print("Player one lap finished")
                    self.score += 1
                    self.lap_marker_TL = False
                    self.lap_marker_BR = False
        
        # Player 2 Finish Line
        if self.player == 2:
            if (self.y > 150) and (self.x > -5) and (self.x < 5):
                if (self.lap_marker_TL == True) and (self.lap_marker_BR == True):
                    self.score += 1
                    self.lap_marker_TL = False
                    self.lap_marker_BR = False

        # Check for collisions with edge of screen
        if (self.x > WIDTH/2) or (self.x < WIDTH/-2):
            self.dx *= -1
        elif (self.y > HEIGHT/2) or (self.y < HEIGHT/-2):
            self.dy *= -1

        # Check for collisions with inner walls
        elif (self.x < 250 and self.x > -250) and (self.y > 140 and self.y < 150): # checks if the player is inside the wall
            self.y = 150 # moves the player to the edge of the wall
            self.dy *= -1 # sets the players direction to the opposite, so it bounces off
        elif (self.x < 250 and self.x > -250) and (self.y > -150 and self.y < -140):
            self.y = -150
            self.dy *= -1
        elif (self.y < 150 and self.y > -150) and (self.x > -250 and self.x < -240):
            self.x = -250
            self.dx *= -1
        elif (self.y < 150 and self.y > -150) and (self.x > 240 and self.x < 250):
            self.x = 250
            self.dx *= -1

# Missile Class
class Missile(Sprite):
    def __init__(self, player):
        Sprite.__init__(self)
        self.shape = "circle"
        self.size = 0.5
        self.color = "red"
        self.active = False
        self.player = player
    
    def fire(self):
        if self.active == False:
            self.active = True
            self.x = self.player.x
            self.y = self.player.y
            self.heading = self.player.heading
            self.dx = self.player.dx + (math.cos(math.radians(self.heading))*1.5)
            self.dy = self.player.dy + (math.sin(math.radians(self.heading))*1.5)
            if muted == False:
                winsound.PlaySound("shoot.wav", winsound.SND_ASYNC)
    
    def update(self):
        self.x += self.dx
        self.y += self.dy
        if (self.x > WIDTH/2) or (self.x < WIDTH/-2):
            self.active = False
        if (self.y > HEIGHT/2) or (self.y < HEIGHT/-2):
            self.active = False

        # check for collision with inner wall
        elif (self.x < 250 and self.x > -250) and (self.y > 140 and self.y < 150): # checks if the missile is inside the wall
            self.y = 150 # moves the missile to the edge of the wall
            self.dy *= -1 # sets the missiles direction to the opposite, so it bounces off
        elif (self.x < 250 and self.x > -250) and (self.y > -150 and self.y < -140):
            self.y = -150
            self.dy *= -1
        elif (self.y < 150 and self.y > -150) and (self.x > -250 and self.x < -240):
            self.x = -250
            self.dx *= -1
        elif (self.y < 150 and self.y > -150) and (self.x > 240 and self.x < 250):
            self.x = 250
            self.dx *= -1

        # check for collision with portal
        elif (self.y < 50 and self.y > -50) and (self.x > -255 and self.x < -240):
            self.x = 280
            self.dx *= 1
        elif (self.y < 50 and self.y > -50) and (self.x > 240 and self.x < 255):
            self.x = -280
            self.dx *= 1

# Button Class
class Button():
    def __init__(self):
        self.Button_x = 0
        self.Button_y = 0
        self.ButtonLength = 100
        self.ButtonWidth = 50
        self.message = "click me"
        self.name = "Menu"
        self.color = "white"

    def draw_button(self, pen_sprite):
        pen_sprite.penup()
        pen_sprite.color(self.color)
        pen_sprite.begin_fill()
        pen_sprite.goto(self.Button_x, self.Button_y)
        pen_sprite.goto(self.Button_x + self.ButtonLength, self.Button_y)
        pen_sprite.goto(self.Button_x + self.ButtonLength, self.Button_y + self.ButtonWidth)
        pen_sprite.goto(self.Button_x, self.Button_y + self.ButtonWidth)
        pen_sprite.goto(self.Button_x, self.Button_y)
        pen_sprite.end_fill()
        pen_sprite.goto(self.Button_x+(self.ButtonLength/2), self.Button_y+(self.ButtonWidth/2))
        pen_sprite.color("black")
        pen_sprite.write(self.message, align="center", font = ('Arial', 15, 'normal'))

    def button_check(self, x,y):
        # Loops through the list of button to check if any are clicked
        for z in buttons:
            z.button_click(x,y)

    def button_click(self, x,y):
        global game_mode
        global pen_main
        global wn
        global color_one
        global color_two
        global selected_player
        global muted
        if self.Button_x <= x <= (self.Button_x + self.ButtonLength):
            if self.Button_y <= y <= (self.Button_y + self.ButtonWidth):

                # button sends the player to the garage screen
                if self.name == "garage":
                    if game_mode == "start":
                        gotogarage()
                        print(self.Button_y, y, self.Button_y + self.ButtonWidth)
                        print("Clicked garage")
                
                # button starts the game
                if self.name == "play":
                    if game_mode == "start":
                        start_game()
                        print(self.Button_y, y, self.Button_y + self.ButtonWidth)
                        print("Clicked play")
                
                # buttons to go back to the title screen
                if self.name == "exit":
                    if game_mode == "playing" or game_mode == "end":
                        returntomenu()
                        print("Clicked exit")
                if self.name == "return":
                    if game_mode == "garage" or game_mode == "help":
                        returntomenu()
                        print('Clicked return')
                
                # button to mute the music in the main screen
                if self.name == "mute":
                    if game_mode == "start":
                        if muted == False:
                            muted = True
                            self.color = "gray"
                            drawmenuscreen()
                            winsound.PlaySound(None, winsound.SND_PURGE)
                            print("Clicked mute, muted")
                        elif muted == True:
                            muted = False
                            self.color = "white"
                            drawmenuscreen()
                            winsound.PlaySound("mission.wav", winsound.SND_ASYNC | winsound.SND_LOOP)
                            print("Clicked mute, unmuted")
                
                if self.name == "save":
                    if game_mode == "garage":
                        print("Clicked save")
                if self.name == "player_one":
                    if game_mode == "garage":
                        button_player_two.color = "white"
                        selected_player = "one"
                        self.color = "gray"
                        drawgaragescreen()
                        print("Selected player: " + selected_player)
                if self.name == "player_two":
                    if game_mode == "garage":
                        button_player_one.color = "white"
                        selected_player = "two"
                        self.color = "gray"
                        drawgaragescreen()
                        print("Selected player: " + selected_player)
                if self.name == "red" or self.name == "blue" or self.name == "green" or self.name == "yellow" or self.name == "pink" or self.name == "purple" or self.name == "white":
                    if game_mode == "garage":
                        if selected_player == "one":
                            color_one = self.color
                            custom_ship_one(color_one)
                            print("Changed color one to: " + self.color)
                        elif selected_player == "two":
                            color_two = self.color
                            custom_ship_two(color_two)
                            print("Changed color two to: " + self.color)
                        for sprite in sprites: # for loop that goes through the list of sprites and updates each of them
                            sprite.render(pen_sprite)
                
                if self.name == "help":
                    if game_mode == "start":
                        gotohelp()
                        print("Clicked help")
                else:
                    pass

# Create player and missile objects
player_one = Player("ship_custom_one", "ship_accel_one")
player_one.shape = "ship_custom_one"
player_one.color = color_one
player_one.x = -325 # sets the initial position of player one
missile_one = Missile(player_one)
custom_ship_one(color_one)

player_two = Player("ship_custom_two", "ship_accel_two")
player_two.shape = "ship_custom_two"
player_two.color = color_two
player_two.x = 325
player_two.player = 2
missile_two = Missile(player_two)
custom_ship_two(color_two)


# Create a list of sprites
sprites = [player_one, missile_one, player_two, missile_two]

# Create buttons
# Creating the button that sends the player to the garage
button_garage = Button()
button_garage.name = "garage"
button_garage.message = "Garage"
button_garage.Button_x = -300
button_garage.Button_y = -240
button_garage.ButtonLength = 290
button_garage.ButtonWidth = 70

# Creating the button that starts the game
button_play = Button()
button_play.name = "play"
button_play.message = "Press to Play"
button_play.Button_x = -300
button_play.Button_y = -150
button_play.ButtonLength = 600
button_play.ButtonWidth = 100

# Creating the button that sends the player to the menu screen
button_exit = Button()
button_exit.name = "exit"
button_exit.message = "Home"
button_exit.Button_x = -30
button_exit.Button_y = -30
button_exit.ButtonLength = 60
button_exit.ButtonWidth = 60

# Creating the button that mutes the game
button_mute = Button()
button_mute.name = "mute"
button_mute.message = "Mute"
button_mute.Button_x = 400
button_mute.Button_y = 200
button_mute.ButtonLength = 50
button_mute.ButtonWidth = 50

# Creating a button to exit the garage or help screen to the menu screen
button_return = Button()
button_return.name = "return"
button_return.message = "Home"
button_return.Button_x = -450
button_return.Button_y = 200
button_return.ButtonLength = 60
button_return.ButtonWidth = 60

# Creating the button that selects player one in the garage
button_player_one = Button()
button_player_one.name = "player_one"
button_player_one.message = "Edit Player One"
button_player_one.Button_x = 0
button_player_one.Button_y = -200
button_player_one.ButtonLength = 150
button_player_one.ButtonWidth = 50

# Creating the button that selects player two in the garage
button_player_two = Button()
button_player_two.name = "player_two"
button_player_two.message = "Edit Player Two"
button_player_two.Button_x = 160
button_player_two.Button_y = -200
button_player_two.ButtonLength = 150
button_player_two.ButtonWidth = 50

# Creating the button for selecting red
button_red = Button()
button_red.name = "red"
button_red.message = ""
button_red.Button_x = -300
button_red.Button_y = 100
button_red.ButtonLength = 50
button_red.ButtonWidth = 50
button_red.color = "red"

# Creating the button for selecting green
button_green = Button()
button_green.name = "green"
button_green.message = ""
button_green.Button_x = -300
button_green.Button_y = 40
button_green.ButtonLength = 50
button_green.ButtonWidth = 50
button_green.color = "green"

# Creating the button for selecting blue
button_blue = Button()
button_blue.name = "blue"
button_blue.message = ""
button_blue.Button_x = -300
button_blue.Button_y = -20
button_blue.ButtonLength = 50
button_blue.ButtonWidth = 50
button_blue.color = "blue"

# Creating the button for selecting yellow
button_yellow = Button()
button_yellow.name = "yellow"
button_yellow.message = ""
button_yellow.Button_x = -300
button_yellow.Button_y = -80
button_yellow.ButtonLength = 50
button_yellow.ButtonWidth = 50
button_yellow.color = "yellow"

# Creating the button for selecting pink
button_pink = Button()
button_pink.name = "pink"
button_pink.message = ""
button_pink.Button_x = -300
button_pink.Button_y = -140
button_pink.ButtonLength = 50
button_pink.ButtonWidth = 50
button_pink.color = "pink"

# Creating the button for selecting purple
button_purple = Button()
button_purple.name = "purple"
button_purple.message = ""
button_purple.Button_x = -300
button_purple.Button_y = -200
button_purple.ButtonLength = 50
button_purple.ButtonWidth = 50
button_purple.color = "purple"

# Creating the button for selecting white
button_white = Button()
button_white.name = "white"
button_white.message = ""
button_white.Button_x = -300
button_white.Button_y = 160
button_white.ButtonLength = 50
button_white.ButtonWidth = 50
button_white.color = "white"

button_help = Button()
button_help.name = "help"
button_help.message = "Tutorial"
button_help.Button_x = 10
button_help.Button_y = -240
button_help.ButtonLength = 290
button_help.ButtonWidth = 70

# Create a list of buttons
buttons = [button_garage, button_play, button_exit, button_mute, button_player_one, button_player_two, button_red, button_green, button_blue, button_yellow, button_pink, button_purple, button_white, button_return, button_help]
menubuttons = [button_garage, button_play, button_mute, button_help]
gamebuttons = [button_exit]
garagebuttons = [button_player_one, button_player_two, button_red, button_green, button_blue, button_yellow, button_pink, button_purple, button_white, button_return]
helpbuttons = [button_return]

# Handle starting/restarting the game
def start_game():
    global game_mode
    if game_mode == "end" or game_mode == "start":
        drawgamescreen()
        player_one.reset(-325)
        player_two.reset(325)
        missile_one.active = False
        missile_two.active = False
        game_mode = "playing"
        if muted == False:
            winsound.PlaySound("shoot.wav", winsound.SND_ASYNC)

# Loads the main menu/title screen
def returntomenu():
    global game_mode
    if game_mode == "playing" or game_mode == "end" or game_mode == "garage" or game_mode == "help":
        game_mode = "start"
        drawmenuscreen()
        if muted == False:
            winsound.PlaySound("Mission.wav", winsound.SND_ASYNC | winsound.SND_LOOP)

# Opens the garage screen
def gotogarage():
    global game_mode
    if game_mode == "start":
        drawgaragescreen()
        game_mode = "garage"
        if muted == False:
            winsound.PlaySound("ambience.wav", winsound.SND_ASYNC | winsound.SND_LOOP)

def gotohelp():
    global game_mode
    if game_mode == "start":
        drawhelpscreen()
        game_mode = "help"
        if muted == False:
            winsound.PlaySound("ambience.wav", winsound.SND_ASYNC | winsound.SND_LOOP)

# Draws the screen for the gameplay
def drawgamescreen():
    pen_main.hideturtle()
    pen_main.color("black")
    pen_main.begin_fill()
    pen_main.goto(-(WIDTH/2), HEIGHT/2) # Top left of screen
    pen_main.goto(WIDTH/2, HEIGHT/2) # Top right of screen
    pen_main.goto(WIDTH/2, -(HEIGHT/2)) # Bottom right of screen
    pen_main.goto(-(WIDTH/2), -(HEIGHT/2)) # Bottom left of screen
    pen_main.goto(-(WIDTH/2), HEIGHT/2) # Top left of screen
    pen_main.end_fill()
    pen_main.pencolor("white")
    pen_main.penup()
    pen_main.goto((-250,-150)) # Starts the inside box
    pen_main.pendown()
    pen_main.goto(-250,-150) # Bottom left corner
    pen_main.goto(250,-150) # Bottom right corner
    pen_main.goto(250,150) # Top right corner
    pen_main.goto(-250,150) # Top left corner
    pen_main.goto(-250,-150) # Finishes the inside box
    pen_main.penup()
    pen_main.goto((0,-150)) # Bottom finish line
    pen_main.pendown()
    pen_main.goto(0,-300)
    pen_main.penup()
    pen_main.goto((0,150)) # Top finish line
    pen_main.pendown()
    pen_main.goto(0,300)
    pen_main.penup()
    pen_main.goto(0,100) # Title
    pen_main.write("Gamma Race", False, align="center", font=("Arial", 25, "normal"))
    pen_main.goto(-180,20) # Label for player one score
    pen_main.write("Player 1", align="center", font=("Arial", 25, "normal"))
    pen_main.goto(180,20) # Label for player two score
    pen_main.write("Player 2", align="center", font=("Arial", 25, "normal"))

    # draw the first portal
    pen_main.goto((-270,-50)) # Starts the portal
    pen_main.pendown()
    pen_main.goto(-270,-50) # Bottom left corner
    pen_main.goto(-250,-50) # Bottom right corner
    pen_main.goto(-250,50) # Top right corner
    pen_main.goto(-270,50) # Top left corner
    pen_main.goto(-255,0) # Centre
    pen_main.goto(-270,-50) # Finishes the inside box
    pen_main.penup()

    # draw the second portal
    pen_main.goto((270,-50)) # Starts the portal
    pen_main.pendown()
    pen_main.goto(270,-50) # Bottom left corner
    pen_main.goto(250,-50) # Bottom right corner
    pen_main.goto(250,50) # Top right corner
    pen_main.goto(270,50) # Top left corner
    pen_main.goto(255,0) # Centre
    pen_main.goto(270,-50) # Finishes the inside box
    pen_main.penup()

    for g in gamebuttons:
        g.draw_button(pen_main)

# Draws the menu screen
def drawmenuscreen():
    pen_sprite.hideturtle()
    pen_sprite.color("black")
    pen_sprite.begin_fill()
    pen_sprite.goto(-(WIDTH/2), HEIGHT/2) # Top left of screen
    pen_sprite.goto(WIDTH/2, HEIGHT/2) # Top right of screen
    pen_sprite.goto(WIDTH/2, -(HEIGHT/2)) # Bottom right of screen
    pen_sprite.goto(-(WIDTH/2), -(HEIGHT/2)) # Bottom left of screen
    pen_sprite.goto(-(WIDTH/2), HEIGHT/2) # Top left of screen
    pen_sprite.end_fill()
    pen_sprite.pencolor("white")
    pen_sprite.goto(0, 0)
    pen_sprite.write("Gamma Race", False, align="center", font=("Onyx", 140, "normal"))
    pen_sprite.goto(0, -75)
    
    # Draw the buttons
    for m in menubuttons:
        m.draw_button(pen_sprite)

# Draws the garage screen
def drawgaragescreen():
    pen_sprite.hideturtle()
    pen_sprite.color("black")
    pen_sprite.begin_fill()
    pen_sprite.goto(-(WIDTH/2), HEIGHT/2) # Top left of screen
    pen_sprite.goto(WIDTH/2, HEIGHT/2) # Top right of screen
    pen_sprite.goto(WIDTH/2, -(HEIGHT/2)) # Bottom right of screen
    pen_sprite.goto(-(WIDTH/2), -(HEIGHT/2)) # Bottom left of screen
    pen_sprite.goto(-(WIDTH/2), HEIGHT/2) # Top left of screen
    pen_sprite.end_fill()
    pen_sprite.pencolor("white")
    pen_sprite.goto(0, 200)
    pen_sprite.write("The Garage", False, align="center", font=("Arial", 40, "normal"))
    pen_sprite.goto(65, 100)
    pen_sprite.write("Player One", False, align="center", font=("Arial", 20, "normal"))
    pen_sprite.goto(235, 100)
    pen_sprite.write("Player Two", False, align="center", font=("Arial", 20, "normal"))

    player_one.reset(75)
    player_two.reset(225)
    for sprite in sprites: # for loop that goes through the list of sprites and updates each of them
        sprite.render(pen_sprite)
    for g in garagebuttons:
        g.draw_button(pen_main)

def drawhelpscreen():
    pen_sprite.hideturtle()
    pen_sprite.color("black")
    pen_sprite.begin_fill()
    pen_sprite.goto(-(WIDTH/2), HEIGHT/2) # Top left of screen
    pen_sprite.goto(WIDTH/2, HEIGHT/2) # Top right of screen
    pen_sprite.goto(WIDTH/2, -(HEIGHT/2)) # Bottom right of screen
    pen_sprite.goto(-(WIDTH/2), -(HEIGHT/2)) # Bottom left of screen
    pen_sprite.goto(-(WIDTH/2), HEIGHT/2) # Top left of screen
    pen_sprite.end_fill()
    pen_sprite.pencolor("white")
    pen_sprite.goto(0, 200)
    pen_sprite.write("Welcome to Gamma Race!", False, align="center", font=("Arial", 40, "normal"))
    pen_sprite.goto(0, 100)
    pen_sprite.write("Press the play button to start the game", align="center", font=("Arial", 20, "normal"))
    pen_sprite.goto(0, 50)
    pen_sprite.write("Go to the garage to customise player colors", align="center", font=("Arial", 20, "normal"))
    pen_sprite.goto(0, 0)
    pen_sprite.write("Left player uses WASD, Right uses Arrow keys", align="center", font=("Arial", 20, "normal"))
    pen_sprite.goto(0, -50)
    pen_sprite.write("CTRL to Fire, Laps completed anti-clockwise", align="center", font=("Arial", 20, "normal"))
    pen_sprite.goto(0, -100)
    pen_sprite.write("Missiles shot bounce off walls and teleport through portals", align="center", font=("Arial", 20, "normal"))
    pen_sprite.goto(0, -150)
    pen_sprite.write("Winner scores 5 points, have fun!", align="center", font=("Arial", 20, "normal"))

    for h in helpbuttons:
        h.draw_button(pen_main)

# Key bindings
wn.listen()
# Player One Controls
wn.onkeypress(player_one.rotate_left_start, "a")
wn.onkeypress(player_one.rotate_right_start, "d")
wn.onkeypress(player_one.accelerate_start, "w")
wn.onkeyrelease(player_one.rotate_left_stop, "a")
wn.onkeyrelease(player_one.rotate_right_stop, "d")
wn.onkeyrelease(player_one.accelerate_stop, "w")
wn.onkeypress(missile_one.fire, "Control_L")
# Player Two Controls
wn.onkeypress(player_two.rotate_left_start, "Left")
wn.onkeypress(player_two.rotate_right_start, "Right")
wn.onkeypress(player_two.accelerate_start, "Up")
wn.onkeyrelease(player_two.rotate_left_stop, "Left")
wn.onkeyrelease(player_two.rotate_right_stop, "Right")
wn.onkeyrelease(player_two.accelerate_stop, "Up")
wn.onkeypress(missile_two.fire, "Control_R")
# Menu Controls
wn.onkeypress(start_game, "Return")
wn.onkeypress(returntomenu, "Escape")
wn.onclick(button_garage.button_check)

drawmenuscreen()
# Start the game loop
while True:
    if game_mode == "start":
        wn.update()  # There was a bug in the original code that the start screen would freeze because the wn.update function was missing

    elif game_mode == "garage":
        wn.update()
    elif game_mode == "playing":
        pen_sprite.clear() # this line is necessary to clear the old instances of the sprite
        # Update the sprites
        for sprite in sprites: # for loop that goes through the list of sprites and updates each of them
            sprite.render(pen_sprite)
            sprite.update()

        # Check if a player has collided with a missile
            if player_two.is_collision(missile_one):
                missile_one.active = False
                print("Player Two Hit!")
                if muted == False:
                    winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
                if player_two.score > 0:
                    player_two.score -= 1
            if player_one.is_collision(missile_two):
                missile_two.active = False
                print("Player One Hit!")
                if muted == False:
                    winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
                if player_one.score > 0:
                    player_one.score -= 1
        
        # Show the scores
        pen_sprite.pencolor("white")
        pen_sprite.goto(-180,-40)
        pen_sprite.write(str(player_one.score), align="center", font=("Arial", 30, "normal"))
        pen_sprite.goto(180,-40)
        pen_sprite.write(str(player_two.score), align="center", font=("Arial", 30, "normal"))

        # Check to see if a player has won
        if player_one.score >= SCORE_TO_WIN:
            if muted == False:
                winsound.PlaySound("Mission.wav", winsound.SND_ASYNC | winsound.SND_LOOP)
            pen_sprite.goto(0, -75)
            pen_sprite.write("Player One Wins!", align="center", font=("Arial", 25, "normal"))
            pen_sprite.goto(0, -100)
            pen_sprite.write("Hit Enter to Play Again", align="center", font=("Arial", 15, "normal"))
            game_mode = "end"
        elif player_two.score >= SCORE_TO_WIN:
            if muted == False:
                winsound.PlaySound("Mission.wav", winsound.SND_ASYNC | winsound.SND_LOOP)
            pen_sprite.goto(0, -75)
            pen_sprite.write("Player Two Wins!", align="center", font=("Arial", 25, "normal"))
            pen_sprite.goto(0, -100)
            pen_sprite.write("Hit Enter to Play Again", align="center", font=("Arial", 15, "normal"))
            game_mode = "end"
        
        wn.update()
    else:
        wn.update()
