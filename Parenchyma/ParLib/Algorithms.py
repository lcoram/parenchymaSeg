import numpy
import SimpleITK

# grow from z,x,y, in 3D, erasing one label and putting into place another
def regionGrow3D(z,x,y, newLabel, eraseLabel, labelArray):

  labelArray[z,x,y] = newLabel
  pixels = [] # keep list of pixels included in area
  pixels.append([z,x,y])

  print('called regionGrow3d:', z, x, y)

  while len(pixels) > 0:
    #print('pixels length', len(pixels))
    # get the latest pixel
    z,x,y = pixels.pop()
    if z < labelArray.shape[0]-1 and z > 1 and x < labelArray.shape[1]-1 and x > 1 and y < labelArray.shape[2]-1 and x > 1:
      # grow out to everything connected to this
      if labelArray[z,x+1,y] == eraseLabel:
        labelArray[z,x+1,y] = newLabel
        pixels.append([z,x+1,y])
      if labelArray[z,x-1,y] == eraseLabel:
        labelArray[z,x-1,y] = newLabel
        pixels.append([z,x-1,y])
      if labelArray[z,x,y+1] == eraseLabel:
        labelArray[z,x,y+1] = newLabel
        pixels.append([z,x,y+1])
      if labelArray[z,x,y-1] == eraseLabel:
        labelArray[z,x,y-1] = newLabel
        pixels.append([z,x,y-1])
      if labelArray[z,x+1,y+1] == eraseLabel:
        labelArray[z,x+1,y+1] = newLabel
        pixels.append([z,x+1,y+1])
      if labelArray[z,x-1,y-1] == eraseLabel:
        labelArray[z,x-1,y-1] = newLabel
        pixels.append([z,x-1,y-1])
      if labelArray[z,x+1,y-1] == eraseLabel:
        labelArray[z,x+1,y-1] = newLabel
        pixels.append([z,x+1,y-1])
      if labelArray[z,x-1,y+1] == eraseLabel:
        labelArray[z,x-1,y+1] = newLabel
        pixels.append([z,x-1,y+1])
      # z direction (up / down)
      if labelArray[z+1,x,y] == eraseLabel:
        labelArray[z+1,x,y] = newLabel
        pixels.append([z+1,x,y])
      if labelArray[z-1,x,y] == eraseLabel:
        labelArray[z-1,x,y] = newLabel
        pixels.append([z-1,x,y])

  return labelArray
  
# grow from z,x,y, in 2D, erasing one label and putting into place another
def regionGrow2D(z,x,y, newLabel, eraseLabel, labelArray):

  labelArray[z,x,y] = newLabel
  pixels = [] # keep list of pixels included in area
  pixels.append([z,x,y])

  print('called regionGrow2d:', z, x, y)
    
  # keep array of the area grown into (2D)
  array = labelArray[z,:,:]  
  segmentedInside = numpy.zeros(array.shape,'float')
  segmentedInside[x,y] = newLabel
    
  while len(pixels) > 0:
    #print('pixels length', len(pixels))
    # get the latest pixel
    z,x,y = pixels.pop()
    # grow out to everything connected to this
    if labelArray[z,x+1,y] == eraseLabel:
      labelArray[z,x+1,y] = newLabel
      segmentedInside[x+1,y] = 1
      pixels.append([z,x+1,y])
    if labelArray[z,x-1,y] == eraseLabel:
      labelArray[z,x-1,y] = newLabel
      segmentedInside[x-1,y] = 1
      pixels.append([z,x-1,y])
    if labelArray[z,x,y+1] == eraseLabel:
      labelArray[z,x,y+1] = newLabel
      segmentedInside[x,y+1] = 1
      pixels.append([z,x,y+1])
    if labelArray[z,x,y-1] == eraseLabel:
      labelArray[z,x,y-1] = newLabel
      segmentedInside[x,y-1] = 1
      pixels.append([z,x,y-1])
    if labelArray[z,x+1,y+1] == eraseLabel:
      labelArray[z,x+1,y+1] = newLabel
      segmentedInside[x+1,y+1] = 1
      pixels.append([z,x+1,y+1])
    if labelArray[z,x-1,y-1] == eraseLabel:
      labelArray[z,x-1,y-1] = newLabel
      segmentedInside[x-1,y-1] = 1
      pixels.append([z,x-1,y-1])
    if labelArray[z,x+1,y-1] == eraseLabel:
      labelArray[z,x+1,y-1] = newLabel
      segmentedInside[x+1,y-1] = 1
      pixels.append([z,x+1,y-1])
    if labelArray[z,x-1,y+1] == eraseLabel:
      labelArray[z,x-1,y+1] = newLabel
      segmentedInside[x-1,y+1] = 1
      pixels.append([z,x-1,y+1])

  return segmentedInside

# grow in 2D and then copy to label (baseArray is connectedThreshold or mask)
def copyGrow2D(z,x,y, labelArray, baseArray):

  labelArray[z,x,y] = 1
  pixels = [] # keep list of pixels included in area
  pixels.append([z,x,y])

  print('called copyGrow2d:', z, x, y)
    
  # keep array of the area grown into (2D)
  array = labelArray[z,:,:]  
  segmentedInside = numpy.zeros(array.shape,'float')
  segmentedInside[x,y] = 1
    
  while len(pixels) > 0:
    #print('pixels length', len(pixels))
    # get the latest pixel
    z,x,y = pixels.pop()
    # grow out to everything connected to this
    if baseArray[z,x+1,y] > 0 and labelArray[z,x+1,y] == 0:
      labelArray[z,x+1,y] = 1
      segmentedInside[x+1,y] = 1
      pixels.append([z,x+1,y])
    if baseArray[z,x-1,y] > 0 and labelArray[z,x-1,y] == 0:
      labelArray[z,x-1,y] = 1
      segmentedInside[x-1,y] = 1
      pixels.append([z,x-1,y])
    if baseArray[z,x,y+1] > 0 and labelArray[z,x,y+1] == 0:
      labelArray[z,x,y+1] = 1
      segmentedInside[x,y+1] = 1
      pixels.append([z,x,y+1])
    if baseArray[z,x,y-1] > 0 and labelArray[z,x,y-1] == 0:
      labelArray[z,x,y-1] = 1
      segmentedInside[x,y-1] = 1
      pixels.append([z,x,y-1])
    if baseArray[z,x+1,y+1] > 0 and labelArray[z,x+1,y+1] == 0:
      labelArray[z,x+1,y+1] = 1
      segmentedInside[x+1,y+1] = 1
      pixels.append([z,x+1,y+1])
    if baseArray[z,x-1,y-1] > 0 and labelArray[z,x-1,y-1] == 0:
      labelArray[z,x-1,y-1] = 1
      segmentedInside[x-1,y-1] = 1
      pixels.append([z,x-1,y-1])
    if baseArray[z,x+1,y-1] > 0 and labelArray[z,x+1,y-1] == 0:
      labelArray[z,x+1,y-1] = 1
      segmentedInside[x+1,y-1] = 1
      pixels.append([z,x+1,y-1])
    if baseArray[z,x-1,y+1] > 0 and labelArray[z,x-1,y+1] == 0:
      labelArray[z,x-1,y+1] = 1
      segmentedInside[x-1,y+1] = 1
      pixels.append([z,x-1,y+1])

  return segmentedInside

# loop through the slices, to find the areas connected in 2D to initial mask    
def connected2D(z,x,y, labelArray, connectedArray):

  print('called connected2d:', z, x, y)
    
  maskZ = z
  centroidX = x
  centroidY = y

  # start by getting the segmentation where the mask was drawn
  copyGrow2D(maskZ,centroidX,centroidY, labelArray, connectedArray)
  print('after initial region grow, connected2d:', maskZ, centroidX, centroidY )

  for z in range(maskZ+1, labelArray.shape[0]):
    print('mask:', z)
    for x in range(0,labelArray.shape[1]):
      for y in range(0,labelArray.shape[2]):
        # check if pixel is included in last slice
        if labelArray[z-1,x,y] == 1:
          # check if label array is already included (have already grown into it)
          if labelArray[z,x,y] == 0:
            # then check if connected array is a part of segmented area
            if connectedArray[z,x,y] == 1:
              # add it and grow in 2D
              copyGrow2D(z,x,y,labelArray, connectedArray)
            
  for z in range(maskZ-1, -1, -1):
    print('mask:', z)
    for x in range(0,labelArray.shape[1]):
      for y in range(0,labelArray.shape[2]):
        # check if pixel is included in last slice
        if labelArray[z+1,x,y] == 1:
          # check if label array is already included (have already grown into it)
          if labelArray[z,x,y] == 0:
            # then check if connected array is a part of segmented area
            if connectedArray[z,x,y] == 1:
              # add it and grow in 2D
              copyGrow2D(z,x,y,labelArray, connectedArray)

  print('end connected2D')
  return labelArray
                     

def segment(array, searchLabel):

  maxJ = 0
  minJ = array.shape[0]
  maxK = 0
  minK = array.shape[1]   
    
  isinside = numpy.zeros(array.shape,'float')
  #isinside = numpy.ones(array.shape,'float')
  
  for j in range(0,array.shape[0]):
    for k in range(0,array.shape[1]):
      # grow out from upper left corner (which we assume to be outside)
      # actually we essentially assume the whole left/top edge to be outside
      # unless it is a part of the annotation
      if array[j,k] != searchLabel:
        # NOT a part of the annotation
        if j-1 < 0 or k-1 < 0:
          # this is an edge pixel
          isinside[j,k] = 1
        elif isinside[j-1,k] == 1:
          # a previous adjacent point belonged to the outside
          isinside[j,k] = 1
        elif isinside[j,k-1] == 1:
          # a previous adjacent point belonged to the outside
          isinside[j,k] = 1
        elif isinside[j-1,k-1] == 1:
          # a previous adjacent point belonged to the outside
          isinside[j,k] = 1

  # find biggest & smallest X and Y that are in the annotations
      elif array[j,k] == searchLabel:
        # part of the annotation
        if j > maxJ:
          maxJ = j
        elif j < minJ:
          minJ = j
        elif k > maxK:
          maxK = k
        elif k < minK:
          minK = k
  # end of finding the boundaries
  print(maxJ)
  print(minJ)
  print(maxK)
  print(minK)

  # loop through image again from bottom right corner of subregion
  for j in range(maxJ+1, minJ-1, -1):
    for k in range(maxK+1, minK-1, -1):
      if array[j,k] != searchLabel:
        # NOT a part of the annotation
        if j+1 > maxJ+1 or k+1 > maxK+1:
          # this is an edge pixel
          isinside[j,k] = 1
        elif isinside[j+1,k] == 1:
          # a previous adjacent point belonged to the outside
          isinside[j,k] = 1
        elif isinside[j,k+1] == 1:
          # a previous adjacent point belonged to the outside
          isinside[j,k] = 1
        elif isinside[j+1,k+1] == 1:
          # a previous adjacent point belonged to the outside
          isinside[j,k] = 1
          
  # loop through image again from bottom left corner of subregion
  for k in range(maxK+1, minK-1, -1):
    for j in range(minJ-1, maxJ+1):
      if array[j,k] != searchLabel:
        # NOT a part of the annotation
        if j-1 < minJ-1 or k+1 > maxK+1:
          # this is an edge pixel
          isinside[j,k] = 1
        elif isinside[j+1,k] == 1:
          # an adjacent point belongs to the outside
          isinside[j,k] = 1
        elif isinside[j,k+1] == 1:
          # an adjacent point belongs to the outside
          isinside[j,k] = 1
        elif isinside[j+1,k+1] == 1:
          # an adjacent point belongs to the outside
          isinside[j,k] = 1
        elif isinside[j-1,k] == 1:
          # an adjacent point belongs to the outside
          isinside[j,k] = 1
        elif isinside[j,k-1] == 1:
          # an adjacent point belongs to the outside
          isinside[j,k] = 1
        elif isinside[j-1,k-1] == 1:
          # an adjacent point belongs to the outside
          isinside[j,k] = 1
        elif isinside[j-1,k+1] == 1:
          # an adjacent point belongs to the outside
          isinside[j,k] = 1
        elif isinside[j+1,k-1] == 1:
          # an adjacent point belongs to the outside
          isinside[j,k] = 1

  # loop through image again from top right corner of subregion
  for k in range(minK-1, maxK+1):
    for j in range(maxJ+1, minJ-1, -1):
      if array[j,k] != searchLabel:
        # NOT a part of the annotation
        if k-1 < minK-1 or j+1 > maxJ+1:
          # this is an edge pixel
          isinside[j,k] = 1
        elif isinside[j+1,k] == 1:
          # an adjacent point belongs to the outside
          isinside[j,k] = 1
        elif isinside[j,k+1] == 1:
          # an adjacent point belongs to the outside
          isinside[j,k] = 1
        elif isinside[j+1,k+1] == 1:
          # an adjacent point belongs to the outside
          isinside[j,k] = 1
        elif isinside[j-1,k] == 1:
          # an adjacent point belongs to the outside
          isinside[j,k] = 1
        elif isinside[j,k-1] == 1:
          # an adjacent point belongs to the outside
          isinside[j,k] = 1
        elif isinside[j-1,k-1] == 1:
          # an adjacent point belongs to the outside
          isinside[j,k] = 1
        elif isinside[j-1,k+1] == 1:
          # an adjacent point belongs to the outside
          isinside[j,k] = 1
        elif isinside[j+1,k-1] == 1:
          # an adjacent point belongs to the outside
          isinside[j,k] = 1

  return isinside

         
