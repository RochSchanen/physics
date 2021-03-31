#!/usr/bin/python3
# file: capaCalc.py
# content: capacitance calculator
# created: 2021 March 30 Tuesday
# modified:
# modification:
# author: roch schanen
# comment:

'''
1) basics
	the electrostatics basic law is coulomb law.
	it is valid when there are no moving charges.
	when a charge is free to move, this means that the the forces applied on it cancel out.
	in vaccum charges are completely free, there are no relaxation mecanism. This is beyond the scope of this project.
	in a metal, charges are free but constrained by the volume of the metal.
	further, at equilibrium (static charges), there can't be any electric field or excess charges inside the volume.
	all excess charges are located at the surface of the metal.
	this restrain quite dramatically the geometry for the charge distribution at equilibrium.
	This is what this project relies on to calculate our mutual capacitances.

2) find numerical method
	the method used here is to start from some initial distribution of excess charges on all capacitor plates.
	A uniform distribution seems to be a reasonable choice for most cases.
	We call a plate any piece of metal of any shape as long as its topology is connexe. 
	This distribution will be most likely not near equilibrium.
	then we let the system relax towards the equilibrium state.
	The path to equilibrium is given by the forces applied on the charges.
	No inertial component in this dynamics is defined, so there is no relaxation mecanism needed.
	the total excess charge is set at the start of the simulation and is set to be conserved through out the simulation.
 	the calculation of mutual capacitances can always br done by pairs.
	The initial charges for a given pair of plates are equal and opposite by convention.
	A different choices of charges can only lead to a different resulting set of potenitials.
	There are no method to fix the potential of a metal part:
	The potentials are calculated at the end from the equilibrium charge distribution.
	The mutual capacitance is then simply the total charge divided by the potential difference measured.

3) implement

	- set the geometry for the distribution of the charges in the plate.
	- set the initial distribution with a fixed charge. use a uniform distribution.
	
	to calculate relaxation towards an equilibrium:
	- 1) calculate electric forces on every charge in the system.
	- 2) calculate displacement of charges in the distribution.
	- 3) displace charges respecting the total charge conservation constraint.
	- 4) evaluate equilibrium condition
	- reapeat 1, 2, 3 until 4 is fullfilled
	
	- set a path for evaluating the potential difference bewteen the plates
	- numerically integrate along the path.
	- divide charge by the potential to get the mutual capacitance

4) coding

	- start with a wire and a few charges
	- start with simple parrallel plates for starter

'''


# EXAMPLE ############################################################

if __name__ == "__main__":

    from sys import version as pythonVersion

    print("file: capaCalc.py")
    print("content: capacitance calculator")
    print("created: 2021 March 31 Wednesday")
    print("author: roch schanen")
    print("comment:")
    print("run Python3:" + pythonVersion)

    # instantiate simulator
    # S = system("version 0.00")

    # show all devices defined
    # S.displayPlates()

    # open export file
    # S.openFile()    
    # run simulation    
    # S.runUntil(500)
    # close export file
    # S.closeFile()

    from numpy import linspace

    # finite wire
    xmin, xmax = - 1.0, + 1.0
    
    # positions of the charges
    Qx = linspace(xmin, xmax, 5)

    # calculate the force
    for x in Qx:
    	print(x)

