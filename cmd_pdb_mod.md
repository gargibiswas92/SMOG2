# Removing first 2018 lines from a PDB file
**input PDB pts2.pdb and output PDB pts222.pdb** <br />
sed '1,2018d' pts2.pdb > pts222.pdb
