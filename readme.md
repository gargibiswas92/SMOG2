# Using SMOG-2.4.4
## sourcing SMOG

source /home_b/gargi/smog-2.4.4/configure.smog2

**SMOG only works with PDB file having ATOM and HETATM lines, the PDB should be adjusted according to that using grep command**

grep "^ATOM"|"^HETATM" 4gu3.pdb > 4gu3.atoms.pdb

grep "^HETATM" 4gu3.pdb > 2ci2.atoms.pdb

#there should be a "END" line at the end of the PDB, also there should be "TER" lines at theend of each chain of PDB

sed -i -e "\$aEND" 4gu3_n.pdb

#After adjusting the PDB properly adjustPDB tool is to be used to adjust it for smog input

smog_adjustPDB -i ci2-clean.pdb -o ci2-adjusted.pdb > out-smog_adjustPBD.dat

first adjust the PDB in pymol. To remove the remark or comments or header lines at the top.

smog_adjustPDB -i 1pin_N.pdb -o 1pin_adjusted.pdb -insertTER -removeH -removewater -sort
smog_adjustPDB -i 1pin_N.pdb -o 1pin_adjusted.pdb -renumber -removeH -removewater -sort
smog_adjustPDB -i 1pin_adjusted.pdb -o 1pin_adjusted1.pdb -insertTER

AdjustPDB options

-i <filename>                : input PDB to adjust to smog2 format           
-map <filename>              : specify a user-defined mapping file
-legacy                      : use legacy (version < 2.3) non-matching routine
                               for mapping name residues. Must be used in conjunction with -map 
                               Different mapping files used with -default     
-o [adjusted.pdb]            : output pdb file name
-insertTER                   : interactively determine whether to insert "TER" lines 
                               between any non-consecutive residue numbers.
-renumber                    : ignore any residue numbering inconsistencies 
                               and renumber residues sequentially. This option
                               can be dangerous. -insertTER is recommended, unless
                               you are certain that all numbering inconsistencies 
                               should be ignored 
-PDBresnum                   : don't renumber residues. Keep original PDB numbering.
                               can be useful for analysis
                              output PDB probably won't be useful for smog2
 -removeH                    : strip the file of any atoms that begin with "H"
 -removewater                : strip the file of any residues named HOH or WAT
 -gen_map <map name>         : read a template and write a mapping file
 -t <template dir>           : template directory (only for use with -gen_map)
 -large                      : use base-N (N>10) for indexing atom and residues
                               Necessary if a single chain has more than 
                               9999 residues or 99999 atoms.
 -sort                       : reorder atoms in each residue by name 
 -subALA                     : if a residue only has C, CA, N, O, and CB atoms, 
                               then rename it ALA
 -warn [0]                   : convert first N errors to warnings (-1: convert 
                               all errors) 
 -help                       : show options


#Generate default C-alpha model

smog2 -i input.pdb -CA

#Running simulation using GROMACS-4.5.4

#sourceing gromacs-4.5.4

source /software/smog454/bin/GMXRC.bash

#generate a mdrun.mdp file keeping the following text in it. You might need to change the parameters if needed


integrator = sd ;Run control: Use Langevin Dynamics protocols.
dt = 0.0005 ;time step in reduced units.
nsteps = 100000 ;number of integration steps
nstxout = 100000 ;frequency to write coordinates to output trajectory .trr file.
nstvout = 100000 ;frequency to write velocities to output trajectory .trr file
nstlog = 1000 ;frequency to write energies to log file
nstenergy = 1000 ;frequency to write energies to energy file
nstxtcout = 1000 ;frequency to write coordinates to .xtc trajectory
xtc_grps = system ;group(s) to write to .xtc trajectory (assuming no ndx file is supplied to grompp).
energygrps = system ;group(s) to write to energy file
nstlist = 20 ;Frequency to update the neighbor list
ns_type = grid ; use grid-based neighbor searching
rlist = 3.0 ;cut-off distance for the short-range neighbor list
rcoulomb = 3.0 ; cut-off distance for coulomb interactions
rvdw = 3.0 ; cut-off distance for Vdw interactions
coulombtype = User
vdwtype = User
pbc = no ; Periodic boundary conditions in all the directions
table-extension = 10 ; (nm) Should equals half of the box's longest diagonal.
tc-grps = system ;Temperature coupling
tau_t = 1.0 ; Temperature coupling time constant. Smaller values = stronger coupling.
ref_t = 80.0 ; ~1 reduced temperature unit (see Gromacs manual or SMOG 2 manual for details)
Pcoupl = no ;Pressure coupling
gen_vel = yes ;Velocity generation
gen_temp = 80.0
gen_seed = -1
ld_seed = -1
comm_mode = angular ; center of mass velocity removal.

#When using user-defined potentials (i.e.  not 6-12, or direct Coulomb interactions), then it  is necessary  to  provide  a  table  file  that  contains  tabulated  potentials  and  forces using the smog_tablegen tool

-N		 <integer>		 exponent  of  attractive  non-bonded interaction 	         6
-M 		 <integer>	 	 exponent  of  repulsive  non-bondedinteraction             12
-ic 	 <float>	   	 total  monovalent  ion  concentration(Molar) 
                     for DH interaction                                          0
-temp	 <float>		   simulation temperature corresponding to room
                     temperature (Gromacs units)                                300
-units <float>		   units  to  be  used  in  the  simulation (kCal or kJ)     kCal
-sd		 <float>       distance   (nm)   to   start   switching function
                     for electrostatics                                         1.0
-sc    <float>       distance  (nm)  at  which  switching function 
                     enforces  elec.   Interactions go to zero                  1.5
-tl		 <float>		   length (nm) of table                                         5
-table <string>      output table file name                                   table.xvg
-help                show options                                                N/A

#generate the table using the following command

smog_tablegen -N 10 -M 12 -tl 20.0 -table table.xvg

#Generate the .tpr file using the command

grompp -f mdrun.mdp -c smog.gro -p smog.top -o run.tpr

#Performing MD simulation

mdrun -s run.tpr -noddcheck -table table.xvg -tablep table.xvg
  
# A different approach of running simulation

gmx editconf -f pts150.gro -o newbox.gro -c -d 1.0 -bt cubic
gmx grompp -f minim.mdp -c newbox.gro -p pts150.top -o minim.tpr -maxwarn 1 
gmx mdrun -s minim.tpr -noddcheck -v -deffnm minim
gmx grompp -f md.mdp -c minim.gro -p pts150.top -o md.tpr -maxwarn 1 
gmx mdrun -s md.tpr -deffnm mdrun_pts150 -table table.xvg -tablep table.xvg -pin on -gpu_id 01 -ntmpi 2 -ntomp 8 -nb gpu -bonded gpu

#after running a simulation

trjconv -s run.tpr -f traj.xtc -o mdnoPBC.xtc -pbc mol -center

#creating a PDB file to view from simulation

trjconv -s run.tpr -f mdnoPBC.xtc -dt 5 -o traj.pdb
