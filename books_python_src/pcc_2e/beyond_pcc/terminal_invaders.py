import os, getch

# Terminal Invaders
#
# A terminal-based clone of Space Invaders.
#  Eric Matthes
#  @ehmatthes

# This version is meant to use only lists, if statements, while loops
#  No classes, dictionaries, etc.
# https://github.com/ehmatthes/terminal_invaders
# Left arrow is 68, right arrow is 67, space is 32

### PARAMETERS ###

# What the ship looks like.
ship_string = '|-/\-|'


### FUNCTIONS ###

def draw_screen(x_ship, bullets, x_bullets, y_bullets):
    """Given all current parameters, draw the screen."""
    os.system('clear')
    print("Terminal Invaders - press 'q' to quit")
    draw_ship(x_ship)
    draw_bullets(bullets, x_bullets, y_bullets)

def draw_ship(x_pos):
    y_spacing = '\n\n\n'
    x_spacing = ''
    for x in range(0, x_pos):
        x_spacing += ' '
    print(y_spacing + x_spacing + ship_string)

    # Move cursor down, out of the way
    print("\n\n\n\n\n")

def draw_bullet(bullet, bullets, x_bullets, y_bullets):
    index = bullets.index(bullet)
    x_spacing = ''
    for x in range(0, x_bullets[index]):
        x_spacing += ' '
    print(x_spacing + '|')
    #print(x_bullets, x_bullets[index])

def draw_bullets(bullets, x_bullets, y_bullets):
    """Loops through all bullets. Draws bullets, and removes any
    that have disappeared from the screen."""
    for bullet in bullets:
        draw_bullet(bullet, bullets, x_bullets, y_bullets)


### MAIN GAME ###

# These should be dynamic, from current size of window.
game_width = 80
game_height = 40

x_ship = 0
bullet_number = 0
# Store bullets in a list
bullets = []
x_bullets = []
y_bullets = []

# Start with input set to any key value other than 'q'.
input = 'y'

while input != 'q':
    # Test input to see if ship has moved.
    if ord(input) == 67:
        # Right arrow, increase ship position.
        x_ship += 1
    elif ord(input) == 68:
        # Left arrow, decrease ship position.
        x_ship -= 1
    elif ord(input) == 32:
        # Fire a bullet.
        bullets.append('bullet_' + str(bullet_number))
        # This bullet's x position is the ship's x at time of firing.
        x_bullets.append(x_ship)
        y_bullets.append(0)
        bullet_number += 1

    # Keep the ship in bounds.
    if x_ship < 0:
        x_ship = 0
    elif x_ship > game_width:
        x_ship = game_width

    # Draw the screen, which needs the ship's current position,
    #  the list of bullets, 
    draw_screen(x_ship, bullets, x_bullets, y_bullets)

    # Poll for input each time we pass through the loop.
    input = getch.getch()
