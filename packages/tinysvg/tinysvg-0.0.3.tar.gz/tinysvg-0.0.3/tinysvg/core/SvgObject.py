

class SvgObject(object):
	def __init__(self):
		# Svg attributes
		self.attributes = {}
		self.subObjects = []

		# Objects which are not SvgObject but are still contained
		# between the svg tags. (ex: text in Text object.)
		self.contains   = []
	def toSvg(self,tag):
		ret = "<"+tag+" "
		for attribute in self.attributes:
		  ret += attribute+"='"+self.attributes[attribute]+"' "
		ret += ">"
		for value in self.subObjects:
			ret += value.toSvg()
		for value in self.contains:
		  ret += value
		ret += "</"+tag+">"
		return ret