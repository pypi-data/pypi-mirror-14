from tinysvg.Shapes import PolyLine
import math


# Turtle class which draws by taking an initial position and moving forward
# for some distance at some angle. Movement can draw (pen_down) or can
# move without drawing (pen_up)
class Turtle(object):
	def __init__(self,position,angle):
		self.points = [position]
		#All actual drawings are contained in self.lines
		#self.points is a buffer for the current line.
		self.x = position[0]
		self.y = position[1]
		self.pen = True
		self.width = 2
		self.angle = angle
	def set_x(self,x):
		self.x = x
	def set_y(self,y):
		self.y = y
	def pen_size(self,size):
		self.width = size
	def pen_up(self):
		self.pen = False
	def isDown(self):
		return not self.pen
	def pen_down(self):
		self.pen = True
	def angle(self):
		return angle
	# calculates the (x,y) coodinates 
	# specified by self.angle and distance.
	def move(self,distance):
		self.x = self.x + distance * math.sin(math.radians(self.angle))
		self.y = self.y + distance * math.cos(math.radians(self.angle))
		if(self.pen):
			self.points.append((self.x,self.y))
	def rotate(self,angle):
		self.angle = (angle + self.angle )%360
	def setAngle(self,angle):
		self.angle = angle
	def draw(self):
		return PolyLine(self.points).stroke_width(self.width).fill("none")
