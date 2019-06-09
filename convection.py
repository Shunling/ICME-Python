import numpy
import copy
import math
import pylab
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LogNorm

# 3D plots
def plottimestep(x, y, u):
  """Does a surface plot of u as a function of x and y.
  """
  fig = pylab.figure()
  ax = Axes3D(fig, azim=-128, elev=43)
  surf = ax.plot_surface(x, y, u, rstride=1, cstride=1, norm=LogNorm(), cmap = pylab.cm.jet)
  pylab.xlabel("x")
  pylab.ylabel("y")
  pylab.show(block=False)

# create a 2D Gaussian
def gaussian_2D(nRows,nCols,xmax,ymax):
    dx = xmax/(nCols - 1)
    dy = ymax/(nRows - 1)
    u = numpy.empty((nRows,nCols))
    for i in range(nCols):
        for j in range(nRows):
            x = i * dx;
            y = j * dy;
            u[j,i] = math.exp(-(x-xmax/2.)**2-(y-ymax/2.)**2)
    return u

# print maximum value and index
def printMax(u,t):
    idx = numpy.unravel_index(u.argmax(),u.shape);
    print "%d %d %d %.6f" %(t,idx[0],idx[1],numpy.amax(u))

# problem parameters
xmax  = 10.
ymax  = 10.
nRows = 101
nCols = 101
nTimeSteps = 200
dt = 0.01
cx = 1.
cy = 1.
dx = xmax/(nCols - 1)
dy = ymax/(nRows - 1)

uold = numpy.empty((nRows,nCols))
unew = gaussian_2D(nRows,nCols,xmax,ymax)

printMax(unew,0)
for t in range(nTimeSteps):
    uold = copy.deepcopy(unew)
    for i in range(1,nCols-1):
        for j in range(1,nRows-1):
            unew[i,j] = uold[i,j] - cy * dt *(uold[i,j]-uold[i-1,j])/dy - cx * dt * (uold[i,j] - uold[i,j-1])/dx
    printMax(unew,t+1)        

# Plot
x = numpy.zeros((nRows, nCols), dtype=numpy.float64)
y = numpy.zeros((nRows, nCols), dtype=numpy.float64)
for i in range(nCols):
    for j in range(nRows):
      x[i,j] = i*dx
      y[i,j] = j*dy

plottimestep(x,y,unew)
