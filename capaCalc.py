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
    the electrostatics basic law is coulomb law. it is valid when there are no
    moving charges. when a charge is free to move, this means that the the
    forces applied on it cancel out. in vaccum charges are completely free,
    there are no relaxation mecanism. This is beyond the scope of this project.
    in a metal, charges are free but constrained by the volume of the metal.
    further, at equilibrium (static charges), there can't be any electric
    field or excess charges inside the volume. all excess charges are located
    at the surface of the metal. this restrain quite dramatically the geometry
    for the charge distribution at equilibrium. This is what this project
    relies on to calculate our mutual capacitances.

2) find numerical method
    the method used here is to start from some initial distribution of excess
    charges on all capacitor plates. A uniform distribution seems to be a
    reasonable choice for most cases. We call a plate any piece of metal of
    any shape as long as its topology is connexe. This distribution will be
    most likely not near equilibrium. then we let the system relax towards the
    equilibrium state. The path to equilibrium is given by the forces applied
    on the charges. No inertial component in this dynamics is defined, so
    there is no relaxation mecanism needed. the total excess charge is set at
    the start of the simulation and is set to be conserved through out the
    simulation. the calculation of mutual capacitances can always br done by
    pairs. The initial charges for a given pair of plates are equal and
    opposite by convention. A different choices of charges can only lead to a
    different resulting set of potenitials. There are no method to fix the
    potential of a metal part: The potentials are calculated at the end from
    the equilibrium charge distribution. The mutual capacitance is then simply
    the total charge divided by the potential difference measured.

3) implement

    - set the geometry for the distribution of the charges in the plate.
    - set the initial distribution with a fixed charge. use a uniform
    distribution.
    - to calculate relaxation towards an equilibrium:
        1) calculate electric forces on every charge in the system.
        2) calculate displacement of charges in the distribution.
        3) displace charges respecting the total charge conservation
        constraint.
        4) evaluate equilibrium condition
        reapeat 1, 2, 3 until 4 is fullfilled
    - set a path for evaluating the potential difference bewteen the plates
    - numerically integrate along the path.
    - divide charge by the potential to get the mutual capacitance

4) coding
    
    develop code progressing in steps:

    - start with a wire and a few charges (units will be dealt with later)
    - continue with simple parallel plates view from their cross section (1D)
    - tilt one plates to measure the effect on the capacitance
    - continue with parallel plates shifted from each other by half their
    length
    - continue with 2D parallel plates
    - continue with circular shape, tilted, etc...

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
    from numpy import shape
    from numpy import zeros
    from numpy import sign

    from matplotlib.pyplot import subplots
    from matplotlib.pyplot import show
    from matplotlib.pyplot import xlim
    from matplotlib.pyplot import ylim
    

    # open file
    fh = open('data.txt', 'w')
    fig, ax = subplots()

    # finite wire
    xmin, xmax = - 1.0, + 1.0

    Cn, Cv = 0, ['b','r','g', 'b','r','g', 'b','r','g']

    # set number of charges
    for N in [100]:
    
        # set the positions of the charges:
        
        # compute a uniform distribution
        Qx = linspace(xmin, xmax, N)

        # plot density distribution at step 0
        Qm = zeros(len(Qx)-1) # average position
        Qc = zeros(len(Qx)-1) # average density
        for i in range(len(Qx)-1):
            Qm[i] = (Qx[i+1]+Qx[i])/2.0
            Qc[i] = 1.0 / (Qx[i+1] - Qx[i])
        ax.plot(Qm, Qc/(N-1), '--', color = Cv[Cn], linewidth = 0.5) 

        # perform a fixed number of steps:

        # some more refined test about
        # defining the equilibrium state
        # must be investigated

        # reduce data to file using a modulo term
        MD = 100

        for n in range(3000):

            # for 49 charges, it turns out that 3000 steps
            # is very close to the convergent distribution
            # this was tested visually using up to 5000 steps
            # however, the minimum number of steps required
            # to reach quasi-equilibrium must dependent on
            # the number of charges and requires investigation

            # intialise simulation step:
            Qf = zeros(shape(Qx))
            Qd = zeros(shape(Qx))

            # calculate forces:

            # the computation takes N(N-1) operations
            for i, xi in enumerate(Qx):
                for j, xj in enumerate(Qx):
                    if i == j: continue
                    Qf[i] += sign(xi-xj)/(xi-xj)**2

            # calculate displacement:
            
            # the dynamics of the system is not physical
            # only the equilibrium positions are physical
            # the displacement are fixed to a fraction of
            # the total volume of the system. imagine some
            # kind of overdamped motion. Also, the higher
            # the number of charges the smaller the fraction
            # to accomodate for higher charge densities,
            # but the computation will take more time.

            F = 1/(30*N)
            
            # this value needs to be adjusted as the number
            # of charges increases: the displacement must
            # remain small enough in order to keep a reasonable
            # distance between the charge a prevent overlaping
            # issues: this needs a more general approach,
            # especially at higher dimensions

            S = F*(max(Qx) - min(Qx)) # size of the system

            for i, f in enumerate(Qf): 

                # the choice for the mode of displacement
                # needs also to be studied: it needs to be
                # small enougth when reaching equilibrium
                # in order to avoid oscillation around the
                # equilibrium point, but not too large to
                # keep displacmennt from being too large.
                # some linear funtion around zero which
                # staturates at some given value (on the
                # order of S/N) should make a good filter

                # Qd[i] = sign(f)*S*F # fixed steps
                Qd[i] = f*S*F # linear steps
                # Qd[i] = filter(f,S,F) # general filter

            # Apply displacement respecting the geometrical
            # constraints.

            for i, d in enumerate(Qd):
                x = Qx[i] + Qd[i]
                if x < xmin: x = xmin
                if x > xmax: x = xmax
                Qx[i] = x

            # this must be generalised to higher dimensions
            # also, the superposition of charges should be
            # avoided and included in the code.

            # partial export data to file
            if not n % MD: 
                fh.write(f'{n} ')
                for x in Qx:
                    fh.write(f'{x:+.6e} ')
                fh.write('\n')

            # partial plot
            if n in [2999]:
                # plot density distribution at step n
                Qm = zeros(len(Qx)-1) # average position
                Qc = zeros(len(Qx)-1) # average density
                for i in range(len(Qx)-1):
                    Qm[i] = (Qx[i+1]+Qx[i])/2.0
                    Qc[i] = 1.0 / (Qx[i+1] - Qx[i])
                ax.plot(Qm, Qc/(N-1), '--', color = Cv[Cn], linewidth = 0.5) 

        # save last line
        fh.write(f'{n} ')
        for x in Qx:
            fh.write(f'{x:+.6e} ')
        fh.write('\n')

        # plot result
        Qm = zeros(len(Qx)-1) # average position
        Qc = zeros(len(Qx)-1) # average density
        for i in range(len(Qx)-1):
            Qm[i] = (Qx[i+1]+Qx[i])/2.0
            Qc[i] = 1.0 / (Qx[i+1] - Qx[i])
        ax.plot(Qm, Qc/(N-1), '.', color = Cv[Cn], linewidth = 1.0) 

        # next set of charges
        Cn += 1

        # done

    xlim(-1.0, +1.0)
    ylim(+0.0, +1.0)
    # ax.plot( linspace(xmin, xmax, N), linspace(xmin, xmax, N), '-')
    # ax.plot(linspace(xmin, xmax, N), Qx, '+') 
    # ax.plot(linspace(xmin, xmax, N), Qx - linspace(xmin, xmax, N), '+') 

fh.close()
show()

# results seems to fit the litterature
# see ref: (check in home computer...)
# however, the method does not allow to
# split the charges into positive and
# negative distributions which would
# leads to the conductor polarisation
# when in an external field: when do
# opposites charges appear?

