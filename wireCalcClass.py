#!/usr/bin/python3
# file: capaCalc.py
# content: capacitance calculator
# created: 2021 March 30 Tuesday
# modified:
# modification:
# author: roch schanen
# comment:

# system 1D

from numpy import linspace
from numpy import shape
from numpy import zeros
from numpy import sign

from matplotlib.pyplot import subplots
from matplotlib.pyplot import show
from matplotlib.pyplot import xlim
from matplotlib.pyplot import ylim

from sys import exit as exitProcess

class system1D():

    def __init__(self):

        # define geometry
        self.boundaries = -1.0, +1.0

        # charges
        self.n = 99

        # set default distribution
        a, b = self.boundaries
        self.coordinates = linspace(a, b, self.n)

        # running parameters
        self.step = 0

        return

    fileHandle = None

    def openFile(self, filePath = './data.txt'):
        self.fileHandle = open(filePath, 'w')
        if not self.fileHandle:
            print(f'Error: could not open file "{filePath}"')
            print(f'exiting...')
            exitProcess(1)
        return self.fileHandle

    def closeFile(self):
        if self.fileHandle:
            self.fileHandle.close()
        return 

    def export(self):
        if self.fileHandle:
            fh = self.fileHandle
            fh.write(f'{self.step} ')
            for x in self.coordinates:
                fh.write(f'{x:+.6e} ')
            # End-Of-Line
            fh.write('\n')
            return

    axisHandle = None

    def openFigure(self):
        fig, ax = subplots()
        self.axisHandle = ax
        return self.axisHandle

    def showFigure(self):
        xlim(-1.0, +1.0)
        ylim(+0.0, +1.0)
        show()
        return

    def addPlot(self, *style):
        # get parameters
        ca, n = self.coordinates, self.n-1
        # init arrays
        pa = zeros(n) # average positions array
        da = zeros(n) # average densities array
        # compute data
        for i in range(n):
            pa[i] = (ca[i+1]+ca[i])/2.0
            da[i] = 1.0/(ca[i+1]-ca[i])/n
        # add plot
        self.axisHandle.plot(pa, da , *style) 
        return

    def runStep(self):
        
        # get parameters
        ca = self.coordinates
        a, b = self.boundaries

        # init arrays
        fa = zeros(shape(ca)) # forces array
        da = zeros(shape(ca)) # displacament array

        # forces
        for i, xi in enumerate(ca):
            for j, xj in enumerate(ca):
                if i == j: continue
                fa[i] += sign(xi-xj)/(xi-xj)**2

        # displacements
        for i, f in enumerate(fa):
            # compute virtual displacement
            da[i] = 0.00003*f*(b-a)/self.n
            # coerce displacements to constraints
            x = ca[i] + da[i]
            if x < a: da[i] = a - ca[i]
            if x > b: da[i] = b - ca[i]

        # update positions
        for i in range(self.n):
            self.coordinates[i] += da[i]

        # update step index
        self.step += 1

        # done
        return

    def runUntil(self, value):
        while self.step < value:
            self.runStep()
        return


# EXAMPLE ############################################################

if __name__ == "__main__":

    from sys import version as pythonVersion

    print("file: capaCalc.py")
    print("content: capacitance calculator")
    print("created: 2021 March 31 Wednesday")
    print("author: roch schanen")
    print("comment:")
    print("run Python3:" + pythonVersion)

    S = system1D()

    S.openFile('data2.txt')
    S.openFigure()
    S.addPlot('--b')

    S.runUntil(1000)
    S.addPlot('--b')

    S.runUntil(2000)
    S.addPlot('-r')
    S.export()

    S.showFigure()
    S.closeFile()

'''
the necessity to reduce the displacement factor "0.00003" to such
a low value is determined by the high density regions where an excess
of displacement can overlap the positions of the nearest neigbourgs.
some more subtles conditions to prevent this overlap and also preserve
the copmputation time to reasonable values are necessary for this model.
Another approach is to divide instead the wire in pieces which charge
may vary during the computation: this is the next version of the 1D engine.
'''