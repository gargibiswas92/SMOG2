#Using SMOG-2.4.4 
#sourcing SMOG

source /home_b/gargi/smog-2.4.4/configure.smog2

#Generate default C-alpha model
#Here put only the ATOM, HETATM, TER and END line but no BOND line
#This will generate .contacs, .contacts.CG, .ndx, .top and .gro files
#use the following command

smog2 -i input.pdb -CA -dname CA

#Now modify the input PDB file such that there will be only lines with CA (amino acid) and C1 (sugar)
#The trick is the atom indeces will follow the residue indeces
#At the end of the file (after the END line) add BOND lines
#the syntax is the following
#BOND chain_num1 res_num1 chain_num2 res_num2 energy_group
#the chains will be identified with the TER lines(no need to include that in PDB)
#The modification is to be done by the adjustpdb.py script in this repo
#say the PDB has been saved in the name calpha2.pdb

smog2 -i calpha2.pdb -t /home_b/gargi/smog-2.4.4/SBM_calpha -c CA.contacts.CG -warn 1 -dname CA.withbond

#this will generate a .ndx, .top and .gro file

#Running simulation using GROMACS-4.5.4

#sourceing gromacs-4.5.4

source /software/smog454/bin/GMXRC.bash

#generate a mdrun.mdp file keeping the following text in it. You might need to change the parameters if needed

integrator = sd ;Run control: Use Langevin Dynamics protocols. dt = 0.0005 ;time step in reduced units. nsteps = 100000 ;number of integration steps nstxout = 100000 ;frequency to write coordinates to output trajectory .trr file. nstvout = 100000 ;frequency to write velocities to output trajectory .trr file nstlog = 1000 ;frequency to write energies to log file nstenergy = 1000 ;frequency to write energies to energy file nstxtcout = 1000 ;frequency to write coordinates to .xtc trajectory xtc_grps = system ;group(s) to write to .xtc trajectory (assuming no ndx file is supplied to grompp). energygrps = system ;group(s) to write to energy file nstlist = 20 ;Frequency to update the neighbor list ns_type = grid ; use grid-based neighbor searching rlist = 3.0 ;cut-off distance for the short-range neighbor list rcoulomb = 3.0 ; cut-off distance for coulomb interactions rvdw = 3.0 ; cut-off distance for Vdw interactions coulombtype = User vdwtype = User pbc = no ; Periodic boundary conditions in all the directions table-extension = 10 ; (nm) Should equals half of the box's longest diagonal. tc-grps = system ;Temperature coupling tau_t = 1.0 ; Temperature coupling time constant. Smaller values = stronger coupling. ref_t = 80.0 ; ~1 reduced temperature unit (see Gromacs manual or SMOG 2 manual for details) Pcoupl = no ;Pressure coupling gen_vel = yes ;Velocity generation gen_temp = 80.0 gen_seed = -1 ld_seed = -1 comm_mode = angular ; center of mass velocity removal.

#When using user-defined potentials (i.e. not 6-12, or direct Coulomb interactions), then it is necessary to provide a table file that contains tabulated potentials and forces using the smog_tablegen tool

-N exponent of attractive non-bonded interaction 6 -M exponent of repulsive non-bondedinteraction 12 -ic total monovalent ion concentration(Molar) for DH interaction 0 -temp simulation temperature corresponding to room temperature (Gromacs units) 300 -units units to be used in the simulation (kCal or kJ) kCal -sd distance (nm) to start switching function for electrostatics 1.0 -sc distance (nm) at which switching function enforces elec. Interactions go to zero 1.5 -tl length (nm) of table 5 -table output table file name table.xvg -help show options N/A

#generate the table using the following command

smog_tablegen -N 10 -M 12 -tl 20.0 -table table.xvg

#Generate the .tpr file using the command

grompp -f mdrun.mdp -c smog.gro -p smog.top -o run.tpr

#Performing MD simulation

mdrun -s run.tpr -noddcheck -table table.xvg -tablep table.xvg

#after running a simulation

trjconv -s run.tpr -f traj.xtc -o mdnoPBC.xtc -pbc mol -center

#creating a PDB file to view from simulation

trjconv -s run.tpr -f mdnoPBC.xtc -dt 5 -o traj.pdb#Using SMOG-2.4.4 #sourcing SMOG
