from tinysvg.Shapes.Element import Element


class Circle(Element):
  def __init__(self,cx,cy,r=10):
    super().__init__()
    self.attributes["cx"] = str(cx)
    self.attributes["cy"] = str(cy)
    self.attributes["r"]  = str(r)
  # x-coordinate of center
  def cx(value):
    self.attributes["cx"] = str(value)
    return self
  # y-coordinate of center
  def cy(value):
    self.attributes["cy"] = str(value)
    return self
  def radius(value):
    self.attributes["r"] = str(value)
    return self
  def toSvg(self):
    return super().toSvg("circle")
