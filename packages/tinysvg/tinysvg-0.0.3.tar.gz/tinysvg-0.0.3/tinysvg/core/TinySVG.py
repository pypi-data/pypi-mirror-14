import os 
from tinysvg.core import Canvas
def touch(fname,times=None):
  try:
  	os.remove(fname)
  except OSError:
  	pass
  with open(fname,'a'):
    os.utime(fname,times)

class TinySVG(object):
  def __init__(self,svg_file,canvas = Canvas(120,120)):
    self.svg_file = svg_file
    self.canvas = canvas
  def write(self):
  	touch(self.svg_file)
  	handle =open(self.svg_file,"r+")
  	handle.write(self.canvas.toSvg())
