# Using SMOG-2.4.4 
# sourcing SMOG

source /home_b/gargi/smog-2.4.4/configure.smog2

# Generate default C-alpha model
  **Here put only the ATOM, HETATM, TER and END line but no BOND line <br />
  This will generate .contacs, .contacts.CG, .ndx, .top and .gro files <br />
  use the following command**

smog2 -i input.pdb -CA -dname CA 

# Now modify the input PDB file such that there will be only lines with CA (amino acid) and C1 (sugar)
**The trick is the atom indeces will follow the residue indeces <br />
  At the end of the file (after the END line) add BOND lines <br />
  the syntax is the following <br />
  BOND chain_num1 res_num1 chain_num2 res_num2 energy_group <br />
  the chains will be identified with the TER lines(no need to include that in PDB) <br />
  The modification is to be done by the adjustpdb.py script in this repo <br />
  say the PDB has been saved in the name calpha2.pdb <br />**

smog2 -i calpha2.pdb -t /home_b/gargi/smog-2.4.4/SBM_calpha -c CA.contacts.CG -warn 1 -dname CA.withbond

**this will generate a .ndx, .top and .gro file**

# Running simulation using GROMACS-4.5.4

# sourceing gromacs-4.5.4

source /software/smog454/bin/GMXRC.bash

# generate a mdrun.mdp file keeping the following text in it. You might need to change the parameters if needed

  integrator = sd ;Run control: Use Langevin Dynamics protocols. <br /> 
  dt = 0.0005 ;time step in reduced units. <br /> nsteps = 100000 ;number of integration steps <br /> nstxout = 100000 ;frequency to write coordinates to output trajectory .trr file. <br /> nstvout = 100000 ;frequency to write velocities to output trajectory .trr file <br /> nstlog = 1000 ;frequency to write energies to log file <br /> nstenergy = 1000 ;frequency to write energies to energy file <br /> nstxtcout = 1000 ;frequency to write coordinates to .xtc trajectory <br /> xtc_grps = system ;group(s) to write to .xtc trajectory (assuming no ndx file is supplied to grompp). <br /> energygrps = system ;group(s) to write to energy file <br /> nstlist = 20 ;Frequency to update the neighbor list <br /> ns_type = grid ; use grid-based neighbor searching <br /> rlist = 3.0 ;cut-off distance for the short-range neighbor list <br /> rcoulomb = 3.0 ; cut-off distance for coulomb interactions <br /> rvdw = 3.0 ; cut-off distance for Vdw interactions <br /> coulombtype = User <br /> vdwtype = User <br /> pbc = no ; Periodic boundary conditions in all the directions <br /> table-extension = 10 ; (nm) Should equals half of the box's longest diagonal. <br /> tc-grps = system ;Temperature coupling <br /> tau_t = 1.0 ; Temperature coupling time constant. Smaller values = stronger coupling. <br /> ref_t = 80.0 ; ~1 reduced temperature unit (see Gromacs manual or SMOG 2 manual for details) <br /> Pcoupl = no ;Pressure coupling <br /> gen_vel = yes ;Velocity generation <br /> gen_temp = 80.0 <br /> gen_seed = -1 <br /> ld_seed = -1 <br /> comm_mode = angular ; center of mass velocity removal.

# When using user-defined potentials (i.e. not 6-12, or direct Coulomb interactions),  <br /> then it is necessary to provide a table file that contains tabulated potentials and forces using the smog_tablegen tool 

-N exponent of attractive non-bonded interaction 6 <br /> -M exponent of repulsive non-bondedinteraction 12 <br />-ic total monovalent ion concentration(Molar) for DH interaction 0 <br /> -temp simulation temperature corresponding to room temperature (Gromacs units) 300 <br /> -units units to be used in the simulation (kCal or kJ) kCal <br /> -sd distance (nm) to start switching function for electrostatics 1.0 <br /> -sc distance (nm) at which switching function enforces elec. Interactions go to zero 1.5 <br /> -tl length (nm) of table 5 <br /> -table output table file name table.xvg <br /> -help show options N/A

# generate the table using the following command

smog_tablegen -N 10 -M 12 -tl 20.0 -table table.xvg

# Generate the .tpr file using the command

grompp -f mdrun.mdp -c smog.gro -p smog.top -o run.tpr

# Performing MD simulation

mdrun -s run.tpr -noddcheck -table table.xvg -tablep table.xvg

# after running a simulation

trjconv -s run.tpr -f traj.xtc -o mdnoPBC.xtc -pbc mol -center

# creating a PDB file to view from simulation

trjconv -s run.tpr -f mdnoPBC.xtc -dt 5 -o traj.pdb
