from tinysvg.Shapes.Element import Element

class Rectangle(Element):
  def __init__(self,x,y,width,height,rx=0,ry=0):
    super().__init__()
    self.attributes["x"] = str(x)
    self.attributes["y"] = str(y)
    self.attributes["width"] = str(width)
    self.attributes["height"] = str(height)
    self.attributes["rx"] = str(rx)
    self.attributes["ry"] = str(ry)
  def x(value):
    self.attributes["x"] = str(value)
    return self
  def y(value):
    self.attributes["y"] = str(value)
    return self
  def width(value):
    self.attributes["width"] = str(value)
    return self
  def height(value):
    self.attributes["height"] = str(value)
    return self
  def rx(value):
    self.attributes["rx"] = str(value)
    return self
  def ry(value):
    self.attributes["ry"] = str(value)
    return self
  def toSvg(self):
    return super().toSvg("rect")


if __name__=="__main__":
  re = Rectangle(50,50,100,100,0,0)
  print(re.toSvg())
