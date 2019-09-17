#Pong Implementation

#imported code
import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 14
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = 0
ball_vel = 0
ball_vel = [4,2]
ball_pos = [WIDTH / 2, HEIGHT / 2]
paddle1_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
paddle2_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
paddle1_vel = [0,0]
paddle2_vel = [0,0]
p1_score = 0
p2_score = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    #random number used to determine if ball moves up or down
    up_down = random.randrange(1,3)
    #random velocity for ball when started
    #if ball is sored on right it moves left on new round
    if up_down == 1:
        if direction == LEFT:
            ball_vel[0] = -random.randrange(2,5)
            ball_vel[1] = -random.randrange(1,5)       
        if direction == RIGHT:
            ball_vel[0] = random.randrange(2,5)
            ball_vel[1] = -random.randrange(1,5)
    else:
        if direction == LEFT:
            ball_vel[0] = -random.randrange(2,5)
            ball_vel[1] = random.randrange(1,5)       
        if direction == RIGHT:
            ball_vel[0] = random.randrange(2,5)
            ball_vel[1] = random.randrange(1,5)
        
# define event handlers
#starts new game, resets varriables
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, p1_score, p2_score # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    paddle2_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    p1_score = 0
    p2_score = 0
    spawn_ball(RIGHT)
#handler to draw to canvas   
def draw(canvas):
    global p2_score, p1_score, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_ve;
   
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
 
    #bounces balls off of vertical walls
    if ball_pos[1] >= HEIGHT:
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] <= 0:
        ball_vel[1] = -ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "yellow", "limegreen")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel[1]
    paddle2_pos += paddle2_vel[1]
    
    #keeps paddles on sccreen
    if paddle1_pos <= 0 or paddle1_pos >= HEIGHT - PAD_HEIGHT:
        paddle1_vel[1] = 0
    if paddle2_pos <= 0 or paddle2_pos >= HEIGHT - PAD_HEIGHT:
        paddle2_vel[1] = 0
    if paddle1_pos <= 0:
        paddle1_pos = 0
    if paddle2_pos <= 0:
        paddle2_pos = 0;
    if paddle1_pos >= HEIGHT - PAD_HEIGHT:
        paddle1_pos = HEIGHT - PAD_HEIGHT
    if paddle2_pos >= HEIGHT - PAD_HEIGHT:
        paddle2_pos = HEIGHT - PAD_HEIGHT;
    
    # draw paddles
    canvas.draw_line((HALF_PAD_WIDTH, paddle1_pos), (HALF_PAD_WIDTH, paddle1_pos + PAD_HEIGHT), PAD_WIDTH, "limegreen")
    canvas.draw_line((WIDTH - HALF_PAD_WIDTH, paddle2_pos), (WIDTH - HALF_PAD_WIDTH, paddle2_pos + PAD_HEIGHT), PAD_WIDTH, "limegreen")
    
    # determine whether paddle and ball collide
    #if ball bounces off paddle send it back to the field
    #else award point to opposite player and reset ball
    if ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        if paddle2_pos <= ball_pos[1] and paddle2_pos + PAD_HEIGHT >= ball_pos[1]:
            ball_vel[0] = -ball_vel[0] *1.1 
        else:
            spawn_ball(LEFT)
            p1_score += 1
    if ball_pos[0] - BALL_RADIUS <= 0 + PAD_WIDTH:
        if paddle1_pos <= ball_pos[1] and paddle1_pos + PAD_HEIGHT >= ball_pos[1]:
            ball_vel[0] = -ball_vel[0] * 1.1
        else:
            spawn_ball(RIGHT)
            p2_score += 1
    
    # draw scores 
    canvas.draw_text(str(p1_score), (WIDTH * 0.33, HEIGHT / 5), 70, "limegreen")
    canvas.draw_text(str(p2_score), (WIDTH * 0.6, HEIGHT / 5), 70, "limegreen")
#movement of paddles using various keys 
#increase velocity if key is pressed
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel[1] = 4
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel[1] = -4
        
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel[1] = 4
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel[1] = -4

#stop velocity if key is released
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['s'] or key == simplegui.KEY_MAP['w']:
        paddle1_vel[1] = 0
    if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['up']:
        paddle2_vel[1] = 0
        

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
#create restart button
frame.add_button("Restart Game", new_game, 200)
#assign handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# start frame
frame.start()
new_game()