from tinysvg.core.SvgObject import SvgObject

class Canvas(SvgObject):
  def __init__(self,height,width):
    super().__init__()
    self.attributes.update({
      "height":str(height),
      "width":str(width),
      "xmlns":"http://www.w3.org/2000/svg"
    })
  def draw(self,diagram):
    self.subObjects.append(diagram)
  def draw_all(self,diagrams):
    for diagram in diagrams:
      self.subObjects.append(diagram)
  def toSvg(self):
    return super().toSvg("svg")

