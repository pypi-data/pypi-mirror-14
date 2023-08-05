

from tinysvg.Shapes import Element

class Text(Element):
  def __init__(self,text,x,y,font_family="cursive",font_size="55"):
    self.contains.append(text)
    self.attributes["text"] = str(text)
    self.attributes["x"] = str(x)
    self.attributes["y"] = str(y)
    self.attributes["font_family"] = str(font_family)
    self.attributes["font_size"] = str(font_size)
  def toSvg(self):
    return super().toSvg("text")