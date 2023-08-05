from setuptools import setup

setup(name="tinysvg",
      version="0.0.3",
      packages = ["tinysvg.Shapes","tinysvg.core","tinysvg.Turtle"],
      zip_safe = True,
      author = "Christian Beasley",
      author_email = "christianbeasley0@gmail.com",
      description = "tinysvg is a thin implementation of svg within python along with simple turtle graphics. Not production stable.",
      license="MIT",
      keywords="svg web turtle graphics",
      url="https://github.com/yyttr3/tinysvg",
      classifiers=[
      	"Development Status :: 3 - Alpha",
      	"Intended Audience :: Developers",
      	"License :: OSI Approved :: MIT License",
      	"Operating System :: OS Independent",
      	"Programming Language :: Python :: 3 :: Only",
      	"Topic :: Multimedia :: Graphics",
      	"Topic :: Internet"
      ],
      install_requires=[],

      )
