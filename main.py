
import pygame
import time
import math

#------------------------------------------------variables----------------------------------------------------
#window
window_dimentions = [1920,1080]

#grid
grid_dimentions = [25,15]
sprite_dimentions = [72,72]
grid_topleft = [(window_dimentions[0] % (grid_dimentions[0] * sprite_dimentions[0])) / 2, (window_dimentions[1] % (grid_dimentions[1] * sprite_dimentions[1])) / 2]

#import levels
levels = []
level_save = []
with open('levels.txt', 'r') as data:
	for line in data:
		if line[0] == '*':
			levels.append(level_save)
			level_save = []
		else:
			row_save = []
			for i in line.split():
				row_save.append(int(i))
			level_save.append(row_save)
level = 1
board = levels[level - 1]

#sprites
sprite_walls = []
for i in range(1,17):
	sprite_walls.append(pygame.image.load('images/spritemap{}.png'.format(i)))
sprite_red = []
for i in range(17,33):
	sprite_red.append(pygame.image.load('images/spritemap{}.png'.format(i)))
sprite_head = pygame.image.load('images/misc_head.png')
sprite_end = pygame.image.load('images/misc_end.png')
sprite_dot = pygame.image.load('images/misc_dot.png')
sprite_select = pygame.image.load('images/misc_select.png')
sprite_blur = pygame.image.load('images/misc_blur.png')

#initiate pygame and windows
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
win = pygame.display.set_mode(window_dimentions, pygame.FULLSCREEN)
pygame.display.set_caption("Morph")

#misc
background_colour = (33,33,33)
walls_id = [10,19]
red_id = [20,29]
idle = True
move_tick_speed = 0.025
move_split = False
rearrange = False
holding_block = False
moving = False
min_size = 2
delay = False


#-----------------------------------------update screen--------------------------------------
def draw():
	#draw background
	win.fill(background_colour)

	#draw grid system
	for i in range(1, grid_dimentions[1]+1):
		for j in range(1, grid_dimentions[0]+1):
			#display walls
			if board[i][j] >= walls_id[0] and board[i][j] <= walls_id[1]:
				tilemap([(j-1)*sprite_dimentions[0]+grid_topleft[0], (i-1)*sprite_dimentions[1]+grid_topleft[1]], [j, i], sprite_walls)
			
			#draw end zone
			if board[i][j] == 2:
				win.blit(sprite_end, [(j-1)*sprite_dimentions[0]+grid_topleft[0], (i-1)*sprite_dimentions[1]+grid_topleft[1]])

	if rearrange:
		win.blit(sprite_blur, [0,0])

	for i in range(1, grid_dimentions[1]+1):
		for j in range(1, grid_dimentions[0]+1):
			if board[i][j] == 3:
				win.blit(sprite_select, [(j-1)*sprite_dimentions[0]+grid_topleft[0], (i-1)*sprite_dimentions[1]+grid_topleft[1]])

			#display red 'blob'
			if board[i][j] >= red_id[0] and board[i][j] <= red_id[1]:
				tilemap([(j-1)*sprite_dimentions[0]+grid_topleft[0], (i-1)*sprite_dimentions[1]+grid_topleft[1]], [j, i], sprite_red)
			#draw head on 'blob'
			if board[i][j] == 21 and idle and moving == False:
				win.blit(sprite_head, [(j-1)*sprite_dimentions[0]+grid_topleft[0], (i-1)*sprite_dimentions[1]+grid_topleft[1]])
				#draw movement dots
				if possible_moves[0] and idle:
					win.blit(sprite_dot, [(j-1)*sprite_dimentions[0]+grid_topleft[0], (i-2)*sprite_dimentions[1]+grid_topleft[1]])
				if possible_moves[1] and idle:
					win.blit(sprite_dot, [(j)*sprite_dimentions[0]+grid_topleft[0], (i-1)*sprite_dimentions[1]+grid_topleft[1]])
				if possible_moves[2] and idle:
					win.blit(sprite_dot, [(j-1)*sprite_dimentions[0]+grid_topleft[0], (i)*sprite_dimentions[1]+grid_topleft[1]])
				if possible_moves[3] and idle:
					win.blit(sprite_dot, [(j-2)*sprite_dimentions[0]+grid_topleft[0], (i-1)*sprite_dimentions[1]+grid_topleft[1]])
			elif board[i][j] == 24 and moving:
				win.blit(sprite_head, [(j-1)*sprite_dimentions[0]+grid_topleft[0], (i-1)*sprite_dimentions[1]+grid_topleft[1]])
			elif board[i][j] == 21 and idle == False and moving == False:
				win.blit(sprite_head, [(j-1)*sprite_dimentions[0]+grid_topleft[0], (i-1)*sprite_dimentions[1]+grid_topleft[1]])

	#update screen
	pygame.display.update()

def tilemap(draw_position, grid_position, sprite):
	#get sprite IDs
	if sprite == sprite_walls:
		id_range = walls_id
	elif sprite == sprite_red:
		id_range = red_id

	#calculate sprite look and draw sprite
	if not(board[grid_position[1]-1][grid_position[0]] >= id_range[0] and board[grid_position[1]-1][grid_position[0]] <= id_range[1]) and not(board[grid_position[1]][grid_position[0]+1] >= id_range[0] and board[grid_position[1]][grid_position[0]+1] <= id_range[1]) and not(board[grid_position[1]+1][grid_position[0]] >= id_range[0] and board[grid_position[1]+1][grid_position[0]] <= id_range[1]) and not(board[grid_position[1]][grid_position[0]-1] >= id_range[0] and board[grid_position[1]][grid_position[0]-1] <= id_range[1]):
		win.blit(sprite[0], draw_position)
	if (board[grid_position[1]-1][grid_position[0]] >= id_range[0] and board[grid_position[1]-1][grid_position[0]] <= id_range[1]) and not(board[grid_position[1]][grid_position[0]+1] >= id_range[0] and board[grid_position[1]][grid_position[0]+1] <= id_range[1]) and (board[grid_position[1]+1][grid_position[0]] >= id_range[0] and board[grid_position[1]+1][grid_position[0]] <= id_range[1]) and not(board[grid_position[1]][grid_position[0]-1] >= id_range[0] and board[grid_position[1]][grid_position[0]-1] <= id_range[1]):
		win.blit(sprite[1], draw_position)
	if not(board[grid_position[1]-1][grid_position[0]] >= id_range[0] and board[grid_position[1]-1][grid_position[0]] <= id_range[1]) and (board[grid_position[1]][grid_position[0]+1] >= id_range[0] and board[grid_position[1]][grid_position[0]+1] <= id_range[1]) and not(board[grid_position[1]+1][grid_position[0]] >= id_range[0] and board[grid_position[1]+1][grid_position[0]] <= id_range[1]) and (board[grid_position[1]][grid_position[0]-1] >= id_range[0] and board[grid_position[1]][grid_position[0]-1] <= id_range[1]):
		win.blit(sprite[2], draw_position)
	if not(board[grid_position[1]-1][grid_position[0]] >= id_range[0] and board[grid_position[1]-1][grid_position[0]] <= id_range[1]) and not(board[grid_position[1]][grid_position[0]+1] >= id_range[0] and board[grid_position[1]][grid_position[0]+1] <= id_range[1]) and (board[grid_position[1]+1][grid_position[0]] >= id_range[0] and board[grid_position[1]+1][grid_position[0]] <= id_range[1]) and not(board[grid_position[1]][grid_position[0]-1] >= id_range[0] and board[grid_position[1]][grid_position[0]-1] <= id_range[1]):
		win.blit(sprite[3], draw_position)
	if not(board[grid_position[1]-1][grid_position[0]] >= id_range[0] and board[grid_position[1]-1][grid_position[0]] <= id_range[1]) and not(board[grid_position[1]][grid_position[0]+1] >= id_range[0] and board[grid_position[1]][grid_position[0]+1] <= id_range[1]) and not(board[grid_position[1]+1][grid_position[0]] >= id_range[0] and board[grid_position[1]+1][grid_position[0]] <= id_range[1]) and (board[grid_position[1]][grid_position[0]-1] >= id_range[0] and board[grid_position[1]][grid_position[0]-1] <= id_range[1]):
		win.blit(sprite[4], draw_position)
	if (board[grid_position[1]-1][grid_position[0]] >= id_range[0] and board[grid_position[1]-1][grid_position[0]] <= id_range[1]) and not(board[grid_position[1]][grid_position[0]+1] >= id_range[0] and board[grid_position[1]][grid_position[0]+1] <= id_range[1]) and not(board[grid_position[1]+1][grid_position[0]] >= id_range[0] and board[grid_position[1]+1][grid_position[0]] <= id_range[1]) and not(board[grid_position[1]][grid_position[0]-1] >= id_range[0] and board[grid_position[1]][grid_position[0]-1] <= id_range[1]):
		win.blit(sprite[5], draw_position)
	if not(board[grid_position[1]-1][grid_position[0]] >= id_range[0] and board[grid_position[1]-1][grid_position[0]] <= id_range[1]) and (board[grid_position[1]][grid_position[0]+1] >= id_range[0] and board[grid_position[1]][grid_position[0]+1] <= id_range[1]) and not(board[grid_position[1]+1][grid_position[0]] >= id_range[0] and board[grid_position[1]+1][grid_position[0]] <= id_range[1]) and not(board[grid_position[1]][grid_position[0]-1] >= id_range[0] and board[grid_position[1]][grid_position[0]-1] <= id_range[1]):
		win.blit(sprite[6], draw_position)
	if not(board[grid_position[1]-1][grid_position[0]] >= id_range[0] and board[grid_position[1]-1][grid_position[0]] <= id_range[1]) and (board[grid_position[1]][grid_position[0]+1] >= id_range[0] and board[grid_position[1]][grid_position[0]+1] <= id_range[1]) and (board[grid_position[1]+1][grid_position[0]] >= id_range[0] and board[grid_position[1]+1][grid_position[0]] <= id_range[1]) and not(board[grid_position[1]][grid_position[0]-1] >= id_range[0] and board[grid_position[1]][grid_position[0]-1] <= id_range[1]):
		win.blit(sprite[7], draw_position)
	if not(board[grid_position[1]-1][grid_position[0]] >= id_range[0] and board[grid_position[1]-1][grid_position[0]] <= id_range[1]) and not(board[grid_position[1]][grid_position[0]+1] >= id_range[0] and board[grid_position[1]][grid_position[0]+1] <= id_range[1]) and (board[grid_position[1]+1][grid_position[0]] >= id_range[0] and board[grid_position[1]+1][grid_position[0]] <= id_range[1]) and (board[grid_position[1]][grid_position[0]-1] >= id_range[0] and board[grid_position[1]][grid_position[0]-1] <= id_range[1]):
		win.blit(sprite[8], draw_position)
	if (board[grid_position[1]-1][grid_position[0]] >= id_range[0] and board[grid_position[1]-1][grid_position[0]] <= id_range[1]) and not(board[grid_position[1]][grid_position[0]+1] >= id_range[0] and board[grid_position[1]][grid_position[0]+1] <= id_range[1]) and not(board[grid_position[1]+1][grid_position[0]] >= id_range[0] and board[grid_position[1]+1][grid_position[0]] <= id_range[1]) and (board[grid_position[1]][grid_position[0]-1] >= id_range[0] and board[grid_position[1]][grid_position[0]-1] <= id_range[1]):
		win.blit(sprite[9], draw_position)
	if (board[grid_position[1]-1][grid_position[0]] >= id_range[0] and board[grid_position[1]-1][grid_position[0]] <= id_range[1]) and (board[grid_position[1]][grid_position[0]+1] >= id_range[0] and board[grid_position[1]][grid_position[0]+1] <= id_range[1]) and not(board[grid_position[1]+1][grid_position[0]] >= id_range[0] and board[grid_position[1]+1][grid_position[0]] <= id_range[1]) and not(board[grid_position[1]][grid_position[0]-1] >= id_range[0] and board[grid_position[1]][grid_position[0]-1] <= id_range[1]):
		win.blit(sprite[10], draw_position)
	if not(board[grid_position[1]-1][grid_position[0]] >= id_range[0] and board[grid_position[1]-1][grid_position[0]] <= id_range[1]) and (board[grid_position[1]][grid_position[0]+1] >= id_range[0] and board[grid_position[1]][grid_position[0]+1] <= id_range[1]) and (board[grid_position[1]+1][grid_position[0]] >= id_range[0] and board[grid_position[1]+1][grid_position[0]] <= id_range[1]) and (board[grid_position[1]][grid_position[0]-1] >= id_range[0] and board[grid_position[1]][grid_position[0]-1] <= id_range[1]):
		win.blit(sprite[11], draw_position)
	if (board[grid_position[1]-1][grid_position[0]] >= id_range[0] and board[grid_position[1]-1][grid_position[0]] <= id_range[1]) and not(board[grid_position[1]][grid_position[0]+1] >= id_range[0] and board[grid_position[1]][grid_position[0]+1] <= id_range[1]) and (board[grid_position[1]+1][grid_position[0]] >= id_range[0] and board[grid_position[1]+1][grid_position[0]] <= id_range[1]) and (board[grid_position[1]][grid_position[0]-1] >= id_range[0] and board[grid_position[1]][grid_position[0]-1] <= id_range[1]):
		win.blit(sprite[12], draw_position)
	if (board[grid_position[1]-1][grid_position[0]] >= id_range[0] and board[grid_position[1]-1][grid_position[0]] <= id_range[1]) and (board[grid_position[1]][grid_position[0]+1] >= id_range[0] and board[grid_position[1]][grid_position[0]+1] <= id_range[1]) and not(board[grid_position[1]+1][grid_position[0]] >= id_range[0] and board[grid_position[1]+1][grid_position[0]] <= id_range[1]) and (board[grid_position[1]][grid_position[0]-1] >= id_range[0] and board[grid_position[1]][grid_position[0]-1] <= id_range[1]):
		win.blit(sprite[13], draw_position)
	if (board[grid_position[1]-1][grid_position[0]] >= id_range[0] and board[grid_position[1]-1][grid_position[0]] <= id_range[1]) and (board[grid_position[1]][grid_position[0]+1] >= id_range[0] and board[grid_position[1]][grid_position[0]+1] <= id_range[1]) and (board[grid_position[1]+1][grid_position[0]] >= id_range[0] and board[grid_position[1]+1][grid_position[0]] <= id_range[1]) and not(board[grid_position[1]][grid_position[0]-1] >= id_range[0] and board[grid_position[1]][grid_position[0]-1] <= id_range[1]):
		win.blit(sprite[14], draw_position)
	if (board[grid_position[1]-1][grid_position[0]] >= id_range[0] and board[grid_position[1]-1][grid_position[0]] <= id_range[1]) and (board[grid_position[1]][grid_position[0]+1] >= id_range[0] and board[grid_position[1]][grid_position[0]+1] <= id_range[1]) and (board[grid_position[1]+1][grid_position[0]] >= id_range[0] and board[grid_position[1]+1][grid_position[0]] <= id_range[1]) and (board[grid_position[1]][grid_position[0]-1] >= id_range[0] and board[grid_position[1]][grid_position[0]-1] <= id_range[1]):
		win.blit(sprite[15], draw_position)


#------------------------------------------------------Move-----------------------------------------------------------
#check possible directions player can move
def test_directions():
	directions = [False, False, False, False]
	#run checks 4 times for each direction
	for direction in range(4):
		#copy board
		board_save = []
		for i in board:
			board_row = []
			for j in i:
				board_row.append(j)
			board_save.append(board_row)
		possible = True
		found_spot = True
		while found_spot:
			found_spot = False
			if not possible:
				break
			#memorize blocks next to affected blocks
			for i in range(1, grid_dimentions[1]+1):
				for j in range(1, grid_dimentions[0]+1):
					if board_save[i][j] == 20 and (board_save[i-1][j] == 21 or board_save[i+1][j] == 21 or board_save[i][j-1] == 21 or board_save[i][j+1] == 21):
						board_save[i][j] = 22
			#remove affected blocks
			for i in range(1, grid_dimentions[1]+1):
				for j in range(1, grid_dimentions[0]+1):
					if board_save[i][j] == 21:
						board_save[i][j] = 0
						#check is affected block is able to move
						if board_save[i-1][j] >= 10 and direction == 0:
							possible = False
						elif board_save[i][j+1] >= 10 and direction == 1:
							possible = False
						elif board_save[i+1][j] >= 10 and direction == 2:
							possible = False
						elif board_save[i][j-1] >= 10 and direction == 3:
							possible = False
			#prepare remembered blocks to be moved
			for i in range(1, grid_dimentions[1]+1):
				for j in range(1, grid_dimentions[0]+1):
					if board_save[i][j] == 22:
						board_save[i][j] = 21
						found_spot = True
		if possible:
			directions[direction] = True

	return directions
possible_moves = test_directions()

def move(direction):
	global idle, possible_moves, moving
	if (direction == 'up' and possible_moves[0] == True) or (direction == 'right' and possible_moves[1] == True) or (direction == 'down' and possible_moves[2] == True) or (direction == 'left' and possible_moves[3] == True):
		idle = False
		moving = True
		head = True
		found_spot = True
		while found_spot:
			found_spot = False
			#memorize blocks next to affected blocks
			for i in range(1, grid_dimentions[1]+1):
				for j in range(1, grid_dimentions[0]+1):
					if board[i][j] == 20 and (board[i-1][j] == 21 or board[i+1][j] == 21 or board[i][j-1] == 21 or board[i][j+1] == 21):
						board[i][j] = 22
			#remove ghost blocks
					if board[i][j] == 25:
						board[i][j] = 0

			#move affected blocks
			for i in range(1, grid_dimentions[1]+1):
				for j in range(1, grid_dimentions[0]+1):
					if board[i][j] == 21:
						if move_split:
							board[i][j] = 0
						else:
							board[i][j] = 25
						#check is affected block is able to move
						if direction == 'up':
							if head:
								board[i-1][j] = 24
								head = False
							else:
								board[i-1][j] = 23
						elif direction == 'right':
							if head:
								board[i][j+1] = 24
								head = False
							else:
								board[i][j+1] = 23
						elif direction == 'down':
							if head:
								board[i+1][j] = 24
								head = False
							else:
								board[i+1][j] = 23
						elif direction == 'left':
							if head:
								board[i][j-1] = 24
								head = False
							else:
								board[i][j-1] = 23
			#prepare remembered blocks to be moved
			for i in range(1, grid_dimentions[1]+1):
				for j in range(1, grid_dimentions[0]+1):
					if board[i][j] == 22:
						board[i][j] = 21
						found_spot = True
			draw()
			time.sleep(move_tick_speed)
		for i in range(1, grid_dimentions[1]+1):
			for j in range(1, grid_dimentions[0]+1):
				if board[i][j] == 24:
					board[i][j] = 21
				elif board[i][j] == 23:
					board[i][j] = 20
				elif board[i][j] == 25:
					board[i][j] = 0
		moving = False
		gravity()
		draw()
		idle = True
		# possible_moves = test_directions()

def gravity():
	moved = True
	while moved:
		moved = False
		scanned = True
		while scanned:
			scanned = False
			for i in range(1, grid_dimentions[1]+1):
				for j in range(1, grid_dimentions[0]+1):
					if board[i][j] == 10 or board[i][j] == 24 or board[i][j] == 23:
						if board[i-1][j] == 20:
							board[i-1][j] = 23
							scanned = True
						if board[i+1][j] == 20:
							board[i+1][j] = 23
							scanned = True
						if board[i][j-1] == 20:
							board[i][j-1] = 23
							scanned = True
						if board[i][j+1] == 20:
							board[i][j+1] = 23
							scanned = True
						if board[i-1][j] == 21:
							board[i-1][j] = 24
							scanned = True
						if board[i+1][j] == 21:
							board[i+1][j] = 24
							scanned = True
						if board[i][j-1] == 21:
							board[i][j-1] = 24
							scanned = True
						if board[i][j+1] == 21:
							board[i][j+1] = 24
							scanned = True

		fall = False
		for i in range(1, grid_dimentions[1]+1):
			for j in range(1, grid_dimentions[0]+1):
				if board[i][j] == 20 or board[i][j] == 21:
					fall = True
		time.sleep(0.05)
		if fall:
			draw()
			for i in range(1, grid_dimentions[1]+1):
				i = grid_dimentions[1]+1 - i
				for j in range(1, grid_dimentions[0]+1):
					if board[i][j] == 20 and board[i+1][j] < 10:
						board[i+1][j] = 20
						board[i][j] = 0
						moved = True
					if board[i][j] == 21 and board[i+1][j] < 10:
						board[i+1][j] = 21
						board[i][j] = 0
						moved = True

		for i in range(1, grid_dimentions[1]+1):
			for j in range(1, grid_dimentions[0]+1):
				if board[i][j] == 24:
					board[i][j] = 21
				elif board[i][j] == 23:
					board[i][j] = 20


def check_size():
	size = 0
	#scan for size of blob
	found_spot = True
	while found_spot:
		found_spot = False
		for k in range(1, grid_dimentions[1]+1):
			for l in range(1, grid_dimentions[0]+1):
				if board[k][l] == 20 and ((board[k-1][l] == 21 or board[k+1][l] == 21 or board[k][l-1] == 21 or board[k][l+1] == 21) or (board[k-1][l] == 22 or board[k+1][l] == 22 or board[k][l-1] == 22 or board[k][l+1] == 22)):
					board[k][l] = 22
					found_spot = True

	#check if clicked block is connected to head
	for k in range(1, grid_dimentions[1]+1):
		for l in range(1, grid_dimentions[0]+1):
			if board[k][l] == 22:
				size += 1

	#reset body to defult values
	for k in range(1, grid_dimentions[1]+1):
		for l in range(1, grid_dimentions[0]+1):
			if board[k][l] == 22:
				board[k][l] = 20

	return size

min_size = check_size()

def check_selection():
	global holding_block, rearrange, idle, possible_moves
	#get mouse pos
	mouseX, mouseY = pygame.mouse.get_pos()
	for i in range(1, grid_dimentions[1]+1):
		for j in range(1, grid_dimentions[0]+1):
			#check if movement button is clicked
			if board[i][j] == 21 and idle:
				win.blit(sprite_head, [(j-1)*sprite_dimentions[0]+grid_topleft[0], (i-1)*sprite_dimentions[1]+grid_topleft[1]])
				#draw movement dots
				if possible_moves[0] and idle and mouseX > (j-1)*sprite_dimentions[0]+grid_topleft[0] and mouseX < (j-1)*sprite_dimentions[0]+grid_topleft[0]+sprite_dimentions[0] and mouseY > (i-2)*sprite_dimentions[1]+grid_topleft[1] and mouseY < (i-2)*sprite_dimentions[1]+grid_topleft[1]+sprite_dimentions[1]:
					move('up')
				if possible_moves[1] and idle and mouseX > (j)*sprite_dimentions[0]+grid_topleft[0] and mouseX < (j)*sprite_dimentions[0]+grid_topleft[0]+sprite_dimentions[0] and mouseY > (i-1)*sprite_dimentions[1]+grid_topleft[1] and mouseY < (i-1)*sprite_dimentions[1]+grid_topleft[1]+sprite_dimentions[1]:
					move('right')
				if possible_moves[2] and idle and mouseX > (j-1)*sprite_dimentions[0]+grid_topleft[0] and mouseX < (j-1)*sprite_dimentions[0]+grid_topleft[0]+sprite_dimentions[0] and mouseY > (i)*sprite_dimentions[1]+grid_topleft[1] and mouseY < (i)*sprite_dimentions[1]+grid_topleft[1]+sprite_dimentions[1]:
					move('down')
				if possible_moves[3] and idle and mouseX > (j-2)*sprite_dimentions[0]+grid_topleft[0] and mouseX < (j-2)*sprite_dimentions[0]+grid_topleft[0]+sprite_dimentions[0] and mouseY > (i-1)*sprite_dimentions[1]+grid_topleft[1] and mouseY < (i-1)*sprite_dimentions[1]+grid_topleft[1]+sprite_dimentions[1]:
					move('left')
			#check if part of blob body is clicked
			if board[i][j] == 20 and holding_block == False:
				if mouseX > (j-1)*sprite_dimentions[0]+grid_topleft[0] and mouseX < (j-1)*sprite_dimentions[0]+grid_topleft[0]+sprite_dimentions[0] and mouseY > (i-1)*sprite_dimentions[1]+grid_topleft[1] and mouseY < (i-1)*sprite_dimentions[1]+grid_topleft[1]+sprite_dimentions[1]:
					found_spot = True
					while found_spot:
						found_spot = False
						#scan and remember blocks connected to head
						for k in range(1, grid_dimentions[1]+1):
							for l in range(1, grid_dimentions[0]+1):
								if board[k][l] == 20 and ((board[k-1][l] == 21 or board[k+1][l] == 21 or board[k][l-1] == 21 or board[k][l+1] == 21) or (board[k-1][l] == 22 or board[k+1][l] == 22 or board[k][l-1] == 22 or board[k][l+1] == 22)):
									board[k][l] = 22
									found_spot = True

					#check if clicked block is connected to head
					if board[i][j] == 22:
						if holding_block == False:
							rearrange = True
							holding_block = True
							idle = False
							board[i][j] = 0

					#reset body to defult values
					for k in range(1, grid_dimentions[1]+1):
						for l in range(1, grid_dimentions[0]+1):
							if board[k][l] == 22:
								board[k][l] = 20

			#exit rearrange mode
			if board[i][j] == 21 and holding_block == False:
				if mouseX > (j-1)*sprite_dimentions[0]+grid_topleft[0] and mouseX < (j-1)*sprite_dimentions[0]+grid_topleft[0]+sprite_dimentions[0] and mouseY > (i-1)*sprite_dimentions[1]+grid_topleft[1] and mouseY < (i-1)*sprite_dimentions[1]+grid_topleft[1]+sprite_dimentions[1]:
					gravity()
					possible_moves = test_directions()
					rearrange = False
					idle = True

			#place block
			if board[i][j] == 3 and rearrange and holding_block:
				board[i][j] = 20
				square_count = check_size()
				if square_count >= min_size:
					holding_block = False
				else:
					board[i][j] = 3



#-------------------------------------------game loop----------------------------------------
while True:
	#fps
	time.sleep(0.01)
	#check events
	for event in pygame.event.get():
		#if x pressed quit
		if event.type == pygame.QUIT:
			pygame.quit()
		#if mouse button is pressed and left click is held
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			check_selection()

	#display holding block icon
	if holding_block and rearrange:
		for i in range(1, grid_dimentions[1]+1):
			for j in range(1, grid_dimentions[0]+1):
				if board[i][j] == 3:
					board[i][j] = 0
		mouseX, mouseY = pygame.mouse.get_pos()
		mouse_grid = [math.floor((mouseX - grid_topleft[0])/sprite_dimentions[0]+1),math.floor((mouseY - grid_topleft[1])/sprite_dimentions[1]+1)]
		if board[mouse_grid[1]][mouse_grid[0]] == 0:
			board[mouse_grid[1]][mouse_grid[0]] = 3

	#move with keyboard, arrows or wasd
	keys = pygame.key.get_pressed()
	if (keys[pygame.K_w] or keys[pygame.K_UP]) and possible_moves[0] and idle:
		move('up')
		delay = True
	elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and possible_moves[1] and idle:
		move('right')
		delay = True
	elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and possible_moves[2] and idle:
		move('down')
		delay = True
	elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and possible_moves[3] and idle:
		move('left')
		delay = True

	#update the screen
	draw()
	if delay:
		time.sleep(0.2)
		delay = False
