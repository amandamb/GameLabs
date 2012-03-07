import pygame, sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_START_X = 10
PADDLER_START_X = SCREEN_WIDTH - PADDLE_START_X
PADDLE_START_Y = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SPEED = 10
BALL_WIDTH_HEIGHT = 16

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# This is the rect that goes downt the middle of the screen, splitting the screen in half.
line_rect = pygame.Rect((SCREEN_WIDTH / 2, 0), (10, SCREEN_HEIGHT))
# This is a rect that contains the ball at the beginning it is set in the center of the screen
ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

# Speed of the ball (x, y)
ball_speed = [BALL_SPEED, BALL_SPEED]

# Your paddle vertically centered on the left side
paddle_rect = pygame.Rect((PADDLE_START_X, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))

paddleR_rect = pygame.Rect((PADDLER_START_X, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))

# Scoring: 1 point if you hit the ball, -5 point if you miss the ball
score = 0

opponentScore = 0

# Load the font for displaying the score
font = pygame.font.Font(None, 30)

# Game loop
while True:
	# Event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
			pygame.quit()
		# Control the paddle with the mouse
		elif event.type == pygame.MOUSEMOTION:
			paddle_rect.centery = event.pos[1]
			#paddleR_rect.centery = event.pos[1]
			# correct paddle position if it's going out of window
			if paddle_rect.top < 0:
				paddle_rect.top = 0
			elif paddle_rect.bottom >= SCREEN_HEIGHT:
				paddle_rect.bottom = SCREEN_HEIGHT
			if paddleR_rect.top < 0:
				paddleR_rect.top = 0
			elif paddleR_rect.bottom >= SCREEN_HEIGHT:
				paddleR_rect.bottom = SCREEN_HEIGHT

	# This test if up or down keys are pressed; if yes, move the paddle
	if pygame.key.get_pressed()[pygame.K_UP] and paddle_rect.top > 0:
		paddle_rect.top -= BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_DOWN] and paddle_rect.bottom < SCREEN_HEIGHT:
		paddle_rect.top += BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
		sys.exit(0)
		pygame.quit()
		
	# Update ball position
	ball_rect.left += ball_speed[0]
	ball_rect.top += ball_speed[1]

	# Ball collision with rails
	if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
		ball_speed[1] = -ball_speed[1]
	if  ball_rect.left <= 0:
		ball_speed[0] = -ball_speed[0]
		opponentScore += 1
	if ball_rect.right >= SCREEN_WIDTH:
		ball_speed[0] = -ball_speed[0]
		score += 1

	# Test if the ball is hit by the paddle; if yes reverse speed and add a point
	if paddle_rect.colliderect(ball_rect):
		ball_speed[0] = -ball_speed[0]
		#score += 1
	if paddleR_rect.colliderect(ball_rect):
		ball_speed[0] = -ball_speed[0]
	
	# Clear screen
	screen.fill((255, 255, 255))

	# Render the ball, the paddle, and the score
	pygame.draw.rect(screen, (0, 0, 0), paddle_rect) # Your paddle
	pygame.draw.rect(screen, (0, 0, 0), paddleR_rect) # opponent paddle
	pygame.draw.rect(screen, (100, 0, 100), line_rect) # line down the middle 
	pygame.draw.circle(screen, (0, 0, 0), ball_rect.center, ball_rect.width / 2) # The ball
	score_text = font.render(str(score), True, (0, 0, 0))
	opponentScore_text = font.render(str(opponentScore), True, (0, 0, 0))
	screen.blit(score_text, ((SCREEN_WIDTH / 4) - font.size(str(score))[0] / 2, 5)) # The score
	screen.blit(opponentScore_text, (SCREEN_WIDTH - (SCREEN_WIDTH / 4) - font.size(str(score))[0] / 2, 5))
	
	# Update screen and wait 20 milliseconds
	pygame.display.flip()
	pygame.time.delay(20)
