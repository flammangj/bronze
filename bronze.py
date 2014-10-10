import libtcodpy as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 45
LIMIT_FPS = 20

color_dark_wall = libtcod.Color(0,0,100)
color_dark_ground = libtcod.Color(50,50,150)

class Rect:
	def __init__(self, x, y, w, h):
		self.x1 = x
		self.y1 = y
		self.x2 = x+w
		self.y2 = y+h

class Tile:
	def __init__(self, blocked, block_sight = None):
		self.blocked = blocked
		
		if block_sight is None: block_sight = blocked
		self.block_sight = block_sight
		
def create_room(room):
	global map
	for x in range(room.x1, room.x2 +1):
		for y in range (room.y1, room.y2 + 1):
			map[x][y].blocked = False
			map[x][y].block_sight = False
			
		
def make_map():
	global map
	
	map= [[ Tile(True)
		for y in range(MAP_HEIGHT)]
			for x in range(MAP_WIDTH)]
			
	room1 = Rect(20,15,10,15)
	room2 = Rect(50,15,10,15)
	create_room(room1)
	create_room(room2)
	create_h_tunnel(25,55,23)
	
	player.x = 25
	player.y = 23
	
def create_h_tunnel(x1, x2, y):
	global map
	for x in range(min(x1, x2), max(x1, x2) +1):
		map[x][y].blocked = False
		map[x][y].block_sight = False

def create_v_tunnel(y1, y2, x):
	global map
	for y in range(min(y1, y2), max(y1, y2)+1):
		map[x][y].blocked = False
		map[x][y].block_sight = False
	
def render_all():
	
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			wall = map[x][y].block_sight
			if wall:
				libtcod.console_set_char_background(con,x,y,color_dark_wall,libtcod.BKGND_SET)
			else:
				libtcod.console_set_char_background(con,x,y,color_dark_ground,libtcod.BKGND_SET)
	
	for object in objects:
		object.draw()
	
	libtcod.console_blit(con, 0,0,SCREEN_WIDTH, SCREEN_HEIGHT,0,0,0)


class Object:
	def __init__(self, x, y, char, color):
		self.x = x
		self.y = y
		self.char = char
		self.color = color
 
	def move(self, dx, dy):
		#move by the given amount
		if not map[self.x + dx][self.y + dy].blocked:
			self.x += dx
			self.y += dy
 
	def draw(self):
		#set the color and then draw the character that represents this object at its position
		libtcod.console_set_default_foreground(con, self.color)
		libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
 
	def clear(self):
		#erase the character that represents this object
		libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

def handle_keys():
	key = libtcod.console_check_for_keypress(True)
	
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
		
	elif key.vk == libtcod.KEY_ESCAPE:
		return True
		
	if libtcod.console_is_key_pressed(libtcod.KEY_UP):
		player.move(0, -1)
		
	elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
		player.move(0, 1)
		
	elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
		player.move(-1,0)
		
	elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
		player.move(1,0)

#INITIALIZATION
libtcod.console_set_custom_font('dejavu12x12_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod bronze', False)
libtcod.sys_set_fps(LIMIT_FPS)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', libtcod.white)

npc = Object(SCREEN_WIDTH/2-6, SCREEN_HEIGHT/2-2, '@', libtcod.yellow)

objects = [npc, player]

make_map()

while not libtcod.console_is_window_closed():
	render_all()
	
	libtcod.console_flush()
	
	for object in objects:
		object.clear()
		
	exit = handle_keys()
	if exit:
		break