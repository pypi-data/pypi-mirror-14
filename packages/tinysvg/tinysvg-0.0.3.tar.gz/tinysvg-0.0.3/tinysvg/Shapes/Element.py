from tinysvg.core.SvgObject import SvgObject

class Element(SvgObject):
  def __init__(self):
    super().__init__()
    # Some default attributes all
    # svg-shapes share. 
    self.attributes.update({
      "stroke":"black",
      "stroke-width":"2",
      "fill":"black"
    })
    # The contains array is for entities which are not SvgObject
    # yet are still contained within the element tags. Ex: Text in
    # the text element.
    self.contains = []

    # Sub element array for SvgObject's within the element tags (Ex:Animations)
    self.subElements = []
  def stroke(self,stroke_color):
    self.attributes["stroke"] = stroke_color
    return self
  def stroke_width(self,width):
    self.attributes["stroke_width"] = str(width)
    return self
  def fill(self,fill_color):
    self.attributes["fill"] = fill_color
    return self

  @staticmethod
  def array_format(points):
    # Some elements such as Polygon and Polyline require
    # special formating in their points attribute.
    # this funciton just turns an array of points into
    # a properly formatted string.
    return " ".join(map(lambda x:str(x[0])+","+str(x[1]),points ))
    
  def toSvg(self,tag):
    return super().toSvg(tag)

