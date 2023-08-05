
from tinysvg.Shapes.Element import Element
class Ellipse(Element):
  def __init__(self,cx,cy,rx,ry):
    super().__init__()
    self.attributes["cx"] = str(cx)
    self.attributes["cy"] = str(cy)
    self.attributes["rx"] = str(rx)
    self.attributes["ry"] = str(ry)
  def cx(self,value):
    self.attributes["cx"] = str(value)
    return self
  def cy(self,value):
    self.attributes["cy"] = str(value)
    return self
  def radius_x(self,value):
    self.attributes["rx"] = str(value)
    return self
  def radius_y(self,value):
    self.attributes["ry"] = str(value)
    return self
  def toSvg(self):
    return super().toSvg("ellipse")



