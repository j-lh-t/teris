import pygame
import random
from .shape import shapes,shape_colors, valid_space, convert_shape_format


# Các biến cục bộ
#*_Các biến của cửa sổ chương trình
s_width = 600
#?_Chiều rộng của cửa sổ chương trình
s_height = 700
#?_Chiều cao của cửa sổ chương trình

#*_Cách biến giao diện chơi game
play_width = 300  #?_px
#?_Chiều rộng bằng 300/30 = 10 khối
play_height = 600 #?_px
#?_Chiều cao bằng 600/30 = 20 khối
block_size = 30   #?_px
#?_Kích thước một khối

#*_Căn chỉnh vùng sẽ hiển thị vùng chơi game
top_left_x = 50
top_left_y = s_height - play_height - 5

pygame.display.set_caption('Trò chơi xếp gạch')
#?_Đặt tiêu đề cho cửa sổ game
pygame.font.init()
#?_Đặt font cho các chuỗi xuất hiện trong giao diện game
win = pygame.display.set_mode((s_width, s_height))
#?_Đặt kích thước cửa sổ hiển thị
# SHAPE FORMATS

class Piece(object):  #?_Lớp này để chứa các thuộc tính của trò chơi
	def __init__(self, x, y, shape):
		self.x = x
		self.y = y
		self.shape = shape
		self.color = shape_colors[shapes.index(shape)]
		self.rotation = 0

#?_Lựa chọn khối bất kỳ và thả nó từ vị trí cột thứ 5 tại dòng đầu tiên
def get_shape(): 
  return Piece( shape=random.choice(shapes), x=5, y=0)

#?_Phân vùng giới hạn cửa sổ game
def check_lost(positions):
	for pos in positions:
		x, y = pos
		if y < 1:
			return True
	return False

#?_Tạo khung lưới cho giao diện
def create_grid(locked_pos={}):  
	grid =  [ #*_Tạo lưới tương ứng với chiều rộng và chiều cao của giao diện game
		[
			(0,0,0) #?_Màu đen =)
			for _ in range(int(play_width/block_size))
			#?_Lưới có 10 cột
		] 
		for _ in range(int(play_height/block_size))
		#?_Lưới có 20 dòng
	]

	#*_Khoá giao diện khung lưới
	for i in range(int(play_height/block_size)):
		for j in range(int(play_width/block_size)):
			if (j, i) in locked_pos:
				c = locked_pos[(j,i)]
				grid[i][j] = c
	return grid

def draw_grid(surface, grid): #*_Vẽ lưới lên giao diện
	sx = top_left_x
	sy = top_left_y

	for i in range(len(grid)):
		pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+play_width, sy+ i*block_size))
		for j in range(len(grid[i])):
			pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))

def clear_rows(grid, locked): #*_Xoá các dòng đã đầy và cộng điểm

	inc = 0
	for i in range(len(grid)-1, -1, -1):
		row = grid[i]
		if (0,0,0) not in row:
			inc += 1
			ind = i
			for j in range(len(row)):
				try:
					del locked[(j,i)]
				except:
					continue

	if inc > 0:
		for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
			x, y = key
			if y < ind:
				newKey = (x, y + inc)
				locked[newKey] = locked.pop(key)

	return inc


font_family = 'segoe ui'
def draw_text_middle(surface, text, size, color):
	font = pygame.font.SysFont(font_family, size, bold=True)
	label = font.render(text, 1, color)

	surface.blit(label, (top_left_x + s_width/2.5 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))


def draw_next_shape(shape, surface):
	font = pygame.font.SysFont(font_family, 30)
	label = font.render('Mảnh tiếp theo', 1, (255,255,255))

	sx = top_left_x + play_width + 20
	sy = top_left_y + play_height/2 - 120
	format = shape.shape[shape.rotation % len(shape.shape)]

	for i, line in enumerate(format):
		row = list(line)
		for j, column in enumerate(row):
			if column == '0':
				pygame.draw.rect(surface, shape.color, (sx + 40 + j*block_size, sy + i*block_size, block_size, block_size), 0)

	surface.blit(label, (sx + 10, sy - 100))

def draw_window(surface, grid, score=0): #?_Đặt kiểu chữ và vị trí của chữ "Trò chơi xếp gạch"
	surface.fill((0, 0, 0))

	pygame.font.init()
	font = pygame.font.SysFont(font_family, 45)
	label = font.render('Trò chơi xếp gạch', 1, (255, 255, 255))

	surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

	#?_Điểm hiện tại
	font = pygame.font.SysFont(font_family, 30)
	label = font.render('Điểm: ' + str(score), 1, (255,255,255))

	sx = top_left_x + play_width + 50
	sy = top_left_y + play_height/2 

	surface.blit(label, (sx + 20, sy + 160))

	for i in range(len(grid)):
		for j in range(len(grid[i])):
			pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

	pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

	draw_grid(surface, grid)


def main(win):  # *
	locked_positions = {}
	grid = create_grid(locked_positions)

	change_piece = False
	run = True
	current_piece = get_shape()
	next_piece = get_shape()
	clock = pygame.time.Clock()
	fall_time = 0
	fall_speed = 0.25
	level_time = 0
	score = 0

	while run:
		grid = create_grid(locked_positions)
		fall_time += clock.get_rawtime()
		level_time += clock.get_rawtime()
		clock.tick()

		if level_time/1000 > 5:
			level_time = 0
			if level_time > 0.12:
				level_time -= 0.005

		if fall_time/1000 > fall_speed:
			fall_time = 0
			current_piece.y += 1
			if not(valid_space(current_piece, grid)) and current_piece.y > 0:
				current_piece.y -= 1
				change_piece = True

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.display.quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					current_piece.x -= 1
					if not(valid_space(current_piece, grid)):
						current_piece.x += 1
				if event.key == pygame.K_RIGHT:
					current_piece.x += 1
					if not(valid_space(current_piece, grid)):
						current_piece.x -= 1
				if event.key == pygame.K_DOWN:
					current_piece.y += 1
					if not(valid_space(current_piece, grid)):
						current_piece.y -= 1
				if event.key == pygame.K_UP:
					current_piece.rotation += 1
					if not(valid_space(current_piece, grid)):
						current_piece.rotation -= 1

		shape_pos = convert_shape_format(current_piece)

		for i in range(len(shape_pos)):
			x, y = shape_pos[i]
			if y > -1:
				grid[y][x] = current_piece.color

		if change_piece:
			for pos in shape_pos:
				p = (pos[0], pos[1])
				locked_positions[p] = current_piece.color
			current_piece = next_piece
			next_piece = get_shape()
			change_piece = False
			score += clear_rows(grid, locked_positions) * 10

		draw_window(win, grid, score)
		draw_next_shape(next_piece, win)
		pygame.display.update()

		if check_lost(locked_positions):
			draw_text_middle(win, "THUA RỒI!", 80, (255,255,255))
			pygame.display.update()
			pygame.time.delay(3000)
			run = False


def main_menu():  # *
	run = True
	
	while run:
		win.fill((0,0,0))
		draw_text_middle(win, 'Nhấn phím bất kỳ!', 50, (255,255,255))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				main(win)	

	pygame.display.quit()