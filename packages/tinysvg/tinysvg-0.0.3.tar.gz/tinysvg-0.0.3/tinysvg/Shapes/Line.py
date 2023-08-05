
from tinysvg.Shapes.Element import Element
class Line(Element):
  def __init__(self,x1,y1,x2,y2):
    super().__init__()
    self.attributes["x1"] = str(x1)
    self.attributes["y1"] = str(y1)
    self.attributes["x2"] = str(x2)
    self.attributes["y2"] = str(y2)
  def x1(value):
    self.attributes["x1"] = str(value)
    return self
  def x2(value):
    self.attributes["x2"] = str(value)
    return self
  def y1(value):
    self.attributes["y1"] = str(value)
    return self 
  def y2(value):
    self.attributes["y2"] = str(value)
    return self
  def toSvg(self):
    return super().toSvg("line")


