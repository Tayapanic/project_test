import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from numpy import *

go=False
inputX=raw_input("Write the function for X: ")
inputY=raw_input("Write the function for Y: ")
inputZ=raw_input("Write the function for Z: ")

if len(inputX)>0 and len(inputY)>0 and len(inputZ)>0:
  go=True

if go==True:
  mpl.rcParams['legend.fontsize'] = 10
  fig = plt.figure()
  ax = fig.gca(projection='3d')

  t = linspace(-4 * pi, 4 * pi, 200)

  #I would like that the user input convert in the function for each "axis"
  z = t
  x = sin(t)
  y = cos(t)

  ax.plot(x, y, z, label='Test')

  ax.legend()
  plt.show()