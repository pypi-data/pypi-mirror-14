from tinysvg.Shapes.Element import Element

class Polygon(Element):
  def __init__(self,points):
    super().__init__()
    self.attributes["points"] = Element.array_format(points)

  def points(value):
    self.attributes["points"] = Element.array_format(points)
    return self

  def toSvg(self):
    return super().toSvg("polygon")

if __name__ == "__main__":
  pol = Polygon([(60,20),(100,40),(100,80),(60,100),(20,80),(20,40)])
  print(pol.toSvg())

