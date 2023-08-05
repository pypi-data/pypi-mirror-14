import subprocess as sp
from log_extract import log_extract

def run(lammps_exe, script_name, mpi_command=None):
    """
    Calls LAMMPS to run. Returns data model containing LAMMPS output.
    
    Arguments:
    lammps_exe -- name (and location) of the LAMMPS executable to use.
    script_name -- name of the LAMMPS input script to use.
    mpi_command -- (optional) command line associated with calling MPI to run LAMMPS.
    """
    try:
        if mpi_command is None:
            return log_extract(sp.check_output(lammps_exe + ' -in ' + script_name, shell=True))
        else:
            return log_extract(sp.check_output(mpi_command + ' ' + lammps_exe + ' -in ' + script_name, shell=True))
    except sp.CalledProcessError as e:        
        if e.output != '':
            lines = e.output.split('\n')
            raise ValueError('Invalid LAMMPS input: \n%s' % lines[-2])
        else:
            raise OSError('Failed to run LAMMPS')
