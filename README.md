The script provides a function that takes an image and returns a smaller cropped version containing just the bar code.

CONTRIBUTORS:
Alexander Miles (alexanderashtonmiles)

PYTHON INFORMATION:
Works on Python 2.6, other versions not tested. Requires pylab (matplotlib), PIL, scipy, and numpy to function.

CHANGE LOG:
       Version 0.1.1:
       	       - Initial release

USEAGE:
	Insert "from barc import *" and feed find_barcode() a path to an image file as a string. The function will run with default parameters and return the sub-image as a numpy array. Passing the keyword argument disp as True will cause it to display the various results along the way. Additional keyword arguments are documented in the docstring for find_barcode().

TODO:
	Add a way to detect arbitrarily rotated bar codes, which at present cannot be detected. Increase selectivity in images wherein details look bar code-like. Add a way to deal with additional 2D code types like QR codes and color-based codes.