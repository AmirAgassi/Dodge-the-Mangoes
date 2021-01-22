import numpy,torch,base64,io,linecache,functools,argparse,__future__,pygame,random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

global level; level = 1

leftrightdata="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"
wavedata = "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"
gldata = "iVBORw0KGgoAAAANSUhEUgAAAQQAAAEECAMAAAD51ro4AAADAFBMVEUAAAD08/Dy8Ozz8ej28e3z6+P16+P149L07+j05dP03sfx6Nnz6dz13M7059r1zK3qjWftyKTzvpH9mhvx2cLtsI73wp3zz7b04cbz3tX5olP3p2r21Mb57LnpuHf5uIP0zLr59dH6l0DwvZXulCv2n0T4rH/5niL39cbvk3D9kSHvmELwp1T0p1758KLnmAvss57+lyntnHryq5ryphXvlRv7uHfmrXHomRzp0sP+vhb3oDfyuaX20qXzpYb91ir71kr3nFXktJ39nC/8zjH50EnmpVjusIT686f+xSH+yjD0nyf72s7yvqrwwrD7uo3zz73xpCTinkLopof8y7HhlnT7ty74lpP6v0XpmjL11sfuzL339bPujiLstKbuoov5l0jwtJj64XTssmn41Zf5hSbfmGj5jjLjqZP57YXnvrHxxqb+2kDhpIP9qab8zmXum4D4ybb621z87of29JD93nH4zI347s39inHeh1/0qIH+1GD56W/7rmf714D96pz9jYTruK/75lz97OnglXnovaj4xRn/4Nv3pHr34t7o4N3hw6bppy37tpT8zb7y0MD38fjv3zboxRr7nGH47PLphD7/28T0sXLk3djUliPk4+P/zwT/xwH50cH/ywH40L7/wgL+ywz/xgr5ywHz0QL/0wT208D1zb7+2AT3zwP5xwP70wT41QP/zxT8zgL0xQP00sT41Mf5wAP32wPznwb/vQb/08T/yBT+twX608LujVr8mAr+zr/8zrf9oQn9sAPx1QL21c79073wygH+1sj4zRHv1b3+qAf5xrj/1hPwlgjqzgPwzLr2uqTxuJb6sI/s1gL5jWHzswT83cvwzMT007TxvAPt4ALt2sf9rp/7uJv959z9zcj5oHjymGj+rxrrpwL98Ov7u67pswX1qQT527/0gWL+jA3nhE7heUX+3gT59/r0fUr/2dPuyLP8yqf+qInwdDzwhwvz2BXu7ebsqXTvyxH+1LXnwgL4ytbkv5D+oGDgbDXhk1LybxXe1wT0/bApAAAAm3RSTlMABAYMCRIWJw8sOSIbMh5S/l15/kn+aEc//sepVVCUkEAz3HDj05z3Rf7+yLuyav798P79/fyjoPH+/t+uYf374Lv45+TMtId6/vTt6pyK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"
# All images are stored in Base64 directly as strings above
# to avoid any problems when sending the program to a different computer.

image = pygame.image.load(io.BytesIO(base64.b64decode(leftrightdata)))
wave = pygame.transform.scale(pygame.image.load(io.BytesIO(base64.b64decode(wavedata))),(150,135))
gl = pygame.image.load(io.BytesIO(base64.b64decode(gldata)))
# Decodes the string data to Pygame images.


class gl3D:
	# The main class containing all of the 3D functions
	# provided from PyOpenGL. These are used throughout
	# the program for all of the 3D effects.
	def perspective(a,h,w,i):			return gluPerspective(a,h,w,i)
	def translateF(rota,rotb,rotc):		return glTranslatef(rota,rotb,rotc)
	def rotateF(a,b,c,d):				return glRotatef(a,b,c,d)
	def clear(buffer):
		if buffer:						return glClear(buffer)
		else:							print('clear buffer empty??');	return glClear(buffer)
	def beginGLspace(GLsetting):		return glBegin(GLsetting)
	def endGLspace():					return glEnd()
	def vertex3FV(verticies):			return glVertex3fv(verticies)
	def color3FV(color):				return glColor3fv(color)
	def getDoubleV(MATRIX):				return glGetDoublev(MATRIX)
	def getBufferBits(name):
		if name=='COLOR_BUFFER_BIT':	return GL_COLOR_BUFFER_BIT
		if name=='DEPTH_BUFFER_BIT':	return GL_DEPTH_BUFFER_BIT
	def getSpaceSetting(name):
		if name=='LINES':				return GL_LINES
		if name=='QUADS':				return GL_QUADS


class Cubes:
	# The main class storing each one of the individual
	# cubes on the screen. It is responsible for 
	# holding all individual verticies, setting
	# new verticies along with the movement of the
	# game, and drawing the cubes on the screen.

	def __init__(self,game):
		# Defines the point data for a cube.

		self.surfaces 	= 	(0,1,2,3),(3,2,7,6),(6,7,5,4),(4,5,1,0),(1,5,7,2),(4,0,3,6)
		self.colors		=	(1,1,0),(1,1,0),(1,0,0),(0,1,0),(1,1,0),(0,1,0)
		self.vertices 	=	(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,-1),(1,-1,1),(1,1,1),(-1,-1,1),(-1,1,1)
		self.cube_dict	=	{}
		amt = 8 + (level * 3)
		for x in range(amt):	self.cube_dict[x] = self.set_vertices(game.max_distance)
		# Makes 15 cubes with random positions between
		# the start and the maximum distance.


	def makeCubes(self,freshvertices):
		# Draws each one of the stored cubes
		# on the screen.

		gl3D.beginGLspace(gl3D.getSpaceSetting("QUADS"))
		# Sets the current OpenGL mode.

		for surface in self.surfaces:
			x=0
			for vertex in surface:  
				x+=1;
				gl3D.vertex3FV(freshvertices[vertex])
				gl3D.color3FV(self.colors[x])
				# Draws each cube on the screen
				# based on the stored verticies.

		gl3D.endGLspace()
		# Ends the OpenGL drawing.

	def set_vertices(self,max_distance):
		# Sets positions for a cube randomly
		# on the ground.

		global new_vertices;
		x_value_change,	y_value_change,	z_value_change = random.randrange(-13,-1), 0, random.randrange(-1*max_distance,-20)
		# Generates X, Y, and Z values to modify
		# the original cube position with.

		new_vertices=[]
		for vert in self.vertices:
			new_vert=[]
			new_x,new_y,new_z	=	vert[0]+x_value_change,	vert[1]+y_value_change, vert[2]+z_value_change
			new_vert.append(new_x)
			new_vert.append(new_y)
			new_vert.append(new_z)
			new_vertices.append(new_vert)
			# Modifies the original cube position with
			# the new X, Y, and Z offsets and
			# stores them in a new table.

		return new_vertices

class Ground:
	def __init__(self):
		# Defines the verticies of the floor.
		self.floorverticies=(-300,-0.1,50),(300,-0.1,50),(-300,-0.1,-3000),(300,-0.1,-3000)

	def refreshGround(self):
		# Redraws the ground.

		gl3D.beginGLspace(gl3D.getSpaceSetting("QUADS"))
		# Begins the OpenGL mode.

		for vertex in self.floorverticies:  gl3D.color3FV((-0.3+0.1*level,1.1-0.1*level,1.1-0.1*level));  gl3D.vertex3FV(vertex)
		# Draws each one of the floor verticies.
		
		gl3D.endGLspace()
		# Ends the OpenGL drawing.
		
class Menu:
	def __init__(self,type):
		# Initializes the menu class instance
		# with all of the necessary data.
		self.verticies=(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,-1),(1,-1,1),(1,1,1),(-1,-1,1),(-1,1,1)
		self.edges=(0,1),(0,3),(0,4),(2,1),(2,3),(2,7),(6,3),(6,4),(6,7),(5,1),(5,4),(5,7)
		self.type=type;	pygame.display.quit()

	def show(self):
		# Shows a menu screen depending on the type
		# of screen specificed.
		if self.type=='intro':
			pygame.init();pygame.display.set_caption('intro');surface=pygame.display.set_mode((800,600));clock=pygame.time.Clock();color=pygame.Color('white');hue=0;stop=True
			# Initializes the new pygame window in 2D mode.
			while stop:
				for event in pygame.event.get():
					if event.type==pygame.QUIT:		pygame.quit();	quit()
					if event.type==pygame.KEYDOWN:	stop=False
					# Quits the program if the X button is clicked.
				hue=(hue+1)%360;	color.hsva=hue,100,100,100
				# Defines the new rainbow background hue.

				surface.fill(color);myfont=pygame.font.SysFont('Arial',120);smallfont=pygame.font.SysFont('Arial',45);label=myfont.render('Hi :)', 10, (255-color[0],255-color[1],255-color[2]));labeltwo=smallfont.render('due to limitations with pygame and',10,(color[0]*0.3,color[1]*0.5,color[2]*0.7));labelthree=smallfont.render("the 3D engine, text can't be",10,(color[0]*0.3,color[1]*0.5,color[2]*0.7));labelfour=smallfont.render('displayed when 3d objects are on',10,(color[0]*0.3,color[1]*0.5,color[2]*0.7));labelfive=smallfont.render('screen, so the game will explained',10,(color[0]*0.3,color[1]*0.5,color[2]*0.7));labelsix=smallfont.render('before any 3D objects appear on',10,(color[0]*0.3,color[1]*0.5,color[2]*0.7));labelseven=smallfont.render('the screen.',10,(color[0]*0.3,color[1]*0.5,color[2]*0.7));surface.blit(label,(70,50));surface.blit(labeltwo,(70,190));surface.blit(labelthree,(70,260));surface.blit(labelfour,(70,330));surface.blit(labelfive,(70,400));surface.blit(labelsix,(70,470));surface.blit(labelseven,(70,540));surface.blit(wave,(350,40));pygame.display.flip();clock.tick(24)
				# Draws the intro menu
			stop=True

			while stop:
				for event in pygame.event.get():
					if event.type==pygame.QUIT:		pygame.quit();	quit()
					if event.type==pygame.KEYDOWN:	stop=False
					# Quits the program if the X button is clicked.
				hue=(hue+1)%360;	color.hsva=hue,100,100,100
				# Defines the new rainbow background hue.
				labelone=smallfont.render('The left and right keys move',10,(color[0]*0.3,color[1]*0.5,color[2]*0.7));labeltwo=smallfont.render('your character.',10,(color[0]*0.3,color[1]*0.5,color[2]*0.7));surface.fill(color);surface.blit(labelone,(70,330));surface.blit(labeltwo,(70,390));surface.blit(image,(190,50));pygame.display.flip();clock.tick(24)
				# Draws the intro menu
			stop=True
			while stop:
				for event in pygame.event.get():
					if event.type==pygame.QUIT:		pygame.quit();quit()
					if event.type==pygame.KEYDOWN:	stop=False
					# Quits the program if the X button is clicked.
				hue=(hue+1)%360;	color.hsva=hue,100,100,100
				# Defines the new rainbow background hue.
				labeltwo=smallfont.render('The menu screen is up next,',10,(color[0]*0.3,color[1]*0.5,color[2]*0.7));labelthree=smallfont.render('press any key to start',10,(color[0]*0.3,color[1]*0.5,color[2]*0.7));labelfour=smallfont.render('the game once you get to',10,(color[0]*0.3,color[1]*0.5,color[2]*0.7));labelfive=smallfont.render('the menu!',10,(color[0]*0.3,color[1]*0.5,color[2]*0.7));surface.fill(color);surface.blit(labeltwo,(110,190));surface.blit(labelthree,(110,260));surface.blit(labelfour,(110,330));surface.blit(gl,(250,10));surface.blit(labelfive,(110,400));pygame.display.flip();clock.tick(24)
				# Draws the intro menu
		elif self.type == "start":
		    rot=0;
		    stop=True
		    pygame.init()
		    display=1200,800
		    pygame.display.set_mode(display,  DOUBLEBUF	|  OPENGL )
		    gl3D.perspective(45,display[0]/display[1],0.1,50.0);	gl3D.translateF(rot,rot,-5)
			# Initializes the new pygame window in 3D mode
			# then draws the initial wireframe cube.

		    while stop:
		        for event in pygame.event.get():
		            if event.type==pygame.QUIT:	pygame.quit();	quit()
		            if event.type == pygame.KEYDOWN: stop=False
		        # Quits the program if the X button is clicked.
		        
		        gl3D.rotateF(1,3,1,1);	gl3D.clear(gl3D.getBufferBits("COLOR_BUFFER_BIT")|gl3D.getBufferBits("DEPTH_BUFFER_BIT"));	gl3D.beginGLspace(gl3D.getSpaceSetting("LINES"))
		        # Rotates the cube on the menu screen.

		        for edge in self.edges:
		            for vertex in edge:	gl3D.vertex3FV(self.verticies[vertex])
		            # Draws each vertex of the cube.
		        gl3D.endGLspace();	pygame.display.flip();	pygame.time.wait(10)
		        # Ends the new drawing, refreshes the screen and waits 10 seconds
		        # before the next rotation.


		elif self.type == "nextlevel":
			pygame.init();	pygame.display.set_caption('next level');	surface=pygame.display.set_mode((800,600));	clock=pygame.time.Clock();	color=pygame.Color('white');	hue=0;	stop=True
			# Initializes the new pygame window in 2D mode.

			while stop:
				for event in pygame.event.get():
					if event.type==pygame.QUIT:	pygame.quit();	quit()
					if event.type==pygame.KEYDOWN:stop=False
					# Quits the program if the X button is clicked.
			
				hue=(hue+1)%360;	color.hsva=hue,100,100,100;	surface.fill(color)
				# Defines the new rainbow background hue.
				
				myfont=pygame.font.SysFont('Arial',120);	smallfont=pygame.font.SysFont('Arial',60);	label=myfont.render('You win!',10,(255-color[0],255-color[1],255-color[2]));	labeltwo=smallfont.render('Press any key to continue',10,(255-color[0],255-color[1],255-color[2]));labelthree=smallfont.render('Level: '+str(level),10,(255-color[0],255-color[1],255-color[2]));surface.blit(label,(70,150));surface.blit(labeltwo,(70,290));surface.blit(labelthree,(70,360));pygame.display.flip();clock.tick(30)
				# Draws the next level menu

		else:
			pygame.init();	pygame.display.set_caption('Example');	surface=pygame.display.set_mode((800,600));	clock=pygame.time.Clock();	color=pygame.Color('white');	hue=0;	stop=True
			# Initializes the new pygame window in 2D mode.
			while stop:
				for event in pygame.event.get():
					if event.type==pygame.QUIT:	pygame.quit();	quit()
					if event.type==pygame.KEYDOWN:stop=False
					# Quits the program if the X button is clicked.
				
				hue=(hue+1)%360;	color.hsva=hue,100,100,100;	surface.fill(color)
				# Defines the new rainbow background hue.
				
				myfont=pygame.font.SysFont('Arial',120);	smallfont=pygame.font.SysFont('Arial',60);	label=myfont.render('Game Over!',10,(255-color[0],255-color[1],255-color[2]));	labeltwo=smallfont.render('Press any key to continue',10,(255-color[0],255-color[1],255-color[2]));surface.blit(label,(70,150));surface.blit(labeltwo,(70,290));pygame.display.flip();clock.tick(30)
				# Draws the final menu.

class Game:
	def __init__(self):
		# Initializes the game variables and
		# Pygame itself, then makes a new
		# window and sets it to 3D mode.

		self.display=1600,1200
		self.window=pygame.display.set_mode(self.display,DOUBLEBUF|OPENGL)
		self.x_move,self.y_move=0,0
		self.max_distance=300
		self.level = 1
		self.won = False
		self.object_passed=False

		gl3D.perspective(90,self.display[0]/self.display[1],0.1,150.0)
		gl3D.translateF(0,0,0)
		# Sets the window to 3D mode and
		# defines the perspective of the 
		# camera.


class Camera:
	def __init__(self):
		# Initializes the camera variables.

		self.camera_x,self.camera_y,self.camera_z,self.x=0,0,0,0

	def refreshCamera(self):
		# Refreshes the camera variables with
		# fresh positions.

		self.x=gl3D.getDoubleV(GL_MODELVIEW_MATRIX)
		self.camera_x,self.camera_y,self.camera_z=self.x[3][0],self.x[3][1],self.x[3][2]




game = Game() # Defines the new instance of the Game class.
			  # This is only used to initialize Pygame and
			  # OpenGL for now.

Menu("intro").show() # Shows the Intro menu.

while True: # Starts a loop.
	Menu("start").show() # Shows the Start menu.

	pygame.display.quit() # Closes the initial Pygame window 
						  # only used to initialize OpenGL.

	game = Game() # Defines the new instance of the Game class.
	cubes = Cubes(game) # Defines the new instance of the Cubes class.
	ground = Ground() # Defines the new instance of the Ground class.
	cam = Camera() # Defines the new instance of the Camera class.

	while not game.object_passed: # Loops until a collision is detected.

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
				# Quits the game if the X button is pressed.

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:  game.x_move = 0.1
				if event.key == pygame.K_RIGHT: game.x_move = -0.1
				# Moves the character left or right depending on the
				# key inputted.

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:  game.x_move = 0
				if event.key == pygame.K_RIGHT: game.x_move = 0
				# Stops moving the character depending on the 
				# key lifted.

		cam.refreshCamera()
		# Refreshes the Camera variables based on character position.

		if cam.camera_x > 12 and game.x_move>0:		game.x_move=0
		if cam.camera_x < 0 and game.x_move<0:	game.x_move=0
		# Ensures the character never moves out of bounds.

		if cam.camera_z<-315:	game.won = True;	level+=1; 	break
		# Wins the level if the character has ran past the
		# maximum cube distance.
		
		for item in cubes.cube_dict:
			if cam.camera_z > cubes.cube_dict[item][0][2] and cam.camera_z < cubes.cube_dict[item][5][2]:
				if abs(cubes.cube_dict[item][0][0]) < cam.camera_x*1.18 < abs(cubes.cube_dict[item][2][0]):
					print("collision detected... oof");	game.object_passed = True
					# Detects collisions with any of the cubes on the
					# ground based on camera and cube positions.


		gl3D.translateF(game.x_move,game.y_move,0.05 + (level * 0.033)) # Moves the Camera forward
																		# along with the game.

		gl3D.clear(gl3D.getBufferBits("COLOR_BUFFER_BIT") | gl3D.getBufferBits("DEPTH_BUFFER_BIT"))
		# Clears the OpenGL color and depth buffer.

		ground.refreshGround() # Refreshes the ground on screen.
		
		for each_cube in cubes.cube_dict:		cubes.makeCubes(cubes.cube_dict[each_cube])
		# Draw each cube on screen.

		pygame.display.flip() # Refresh the screen to view the changes.

	if game.won:
		# Move onto the next level screen
		# if the game was won.
		game.won=False
		Menu("nextlevel").show()
	else:
		# Move onto the game over screen
		# if the game was lost.
		Menu("end").show()
		level = 1