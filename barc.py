# coding: utf-8
# -------------------------------------------#
# Barcode Isolating code                     #
# -------------------------------------------#
# Written up by Alexander Miles              #
# Available at http://www.mrplaceholder.com  #
# Last updated: August 28th, 2012            #
# -------------------------------------------#

from PIL import Image
import ImageFilter
from scipy import *
from scipy import ndimage
from pylab import *

def find_barcode(fname, s=15, t=50, disp=True, verbose=False):
    '''
    This function takes in a file name (jpg, png, bmp, gif) and
    attempts to locate a barcode. 

    Arguments:

    fname: A file name presented as a string.
    s: A sigma value (radius) for a Gaussian blur filter
       used to remove excess detail in the original image.
       Defaults to 15.
    t: The threshold cutoff to use when isolate the barcode.
       Defaults to 50.
    disp: True causes the function to display the results
          using matplotlib.
    verbose: True causes extra text output.
    '''
    ii = Image.open(fname)        # Open the given filename string
    iL = ii.convert('L')          # Convert the image to greyscale

    i = iL.copy()                 # Make a copy to work with
    i = i.filter(ImageFilter.BLUR)# Blur the original slightly to
                                  # remove high-freq. detail.
    
    iy, ix = gradient(array(i))   # Take the gradient of the image
    ix = ndimage.gaussian_filter(ix, sigma=s) # Blur the differentials 
    iy = ndimage.gaussian_filter(iy, sigma=s) #
    
    id = abs( abs(ix)-abs(iy) )   # Find the magnitude difference
    id_b = id.copy()
    
    id[id > t] = 255              # Using the keyword argument t
    id[id < t] = 0                # we threshold the difference image.
        
    xdiff = diff(sum(id, axis=0)) # Find sum along the x-axis then
    xdiffmax = xdiff.max()        # find the largest change. This is
    xdiffmin = xdiff.min()        # the edges of the barcode in X.

    ydiff = diff(sum(id, axis=1)) # Similarly in Y.
    ydiffmax = ydiff.max()
    ydiffmin = ydiff.min()


    x = arange(id.shape[1])      # Make a mesh of x and y values
    y = arange(id.shape[0])      # the same size as the image

    uc_x = x[xdiff==xdiffmax][0] # Use the mesh to pick out the
    lc_x = x[xdiff==xdiffmin][0] # coordinates where the derivative
    uc_y = y[ydiff==ydiffmax][0] # is maximum along x and y (the 
    lc_y = y[ydiff==ydiffmin][0] # barcode edges).

    if verbose:
        print "Max deriv: (" , xdiffmax, " , ", ydiffmax, ")"
        print "Min derivL (" , xdiffmin, " , ", ydiffmin, ")"
        print "Corner coodinates: (" , uc_x, " , ", uc_y, "), (" , lc_x, " , ", lc_y, ")"

    '''
    This next block goes through increasing the area considered 
    part of the barcode without going off the edges of the image.
    '''
    
    if (uc_x - 0.05*id.shape[1]) > 0: 
        uc_x -= 0.05*id.shape[1]
    else:
        uc_x = 0.0
    if (lc_x + 0.05*id.shape[1]) < id.shape[1]: 
        lc_x += 0.05*id.shape[1]
    else:
        lc_x = id.shape[1]
    if (uc_y - 0.05*id.shape[0]) > 0: 
        uc_y -= 0.05*id.shape[0]
    else:
        uc_y = 0.0
    if (lc_y + 0.05*id.shape[0]) < id.shape[0]:
        lc_y += 0.05*id.shape[0]
    else:
        lc_y = id.shape[0]
    
    sub_img = array(ii)[uc_y:lc_y,uc_x:lc_x]
    
    try:

        def hide_axes():
            '''
            This function remove the numbers from the axes
            on the images, as they're not needed.
            '''
            ax = gca()
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)

        if disp==True:
            subplot(1,5,1)
            imshow(ii, origin='lower')
            #hide_axes()
            title('Original')
            subplot(1,5,2)
            jet()
            imshow(ix)
            #hide_axes()
            title(r'$\frac{d I}{dx}$')
            subplot(1,5,3)
            imshow(iy)
            #hide_axes()
            title(r'$\frac{d I}{dy}$')
            subplot(1,5,4)
            imshow(id_b)
            #hide_axes()
            title(r'$\left|\frac{d I}{dx}\right| - \left|\frac{d I}{dy}\right|$')
            subplot(1,5,5)
            imshow(id)
            #hide_axes()
            title('Thresholded at t='+str(t))
            show()    
            figure()
            bone()
            imshow(sub_img)
            #hide_axes()
            show()
    except ValueError:
        print "Hit a ValueError: If the differential images are too detailed, try increasing s (the blur radius). If the thresholded image has no white areas, decrease t (threshold value)."
    return sub_img
