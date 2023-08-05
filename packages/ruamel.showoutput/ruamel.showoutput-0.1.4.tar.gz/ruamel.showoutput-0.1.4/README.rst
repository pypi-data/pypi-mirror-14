
show_ouput works like check_output, but showing progress 

There is a plethora of ways of calling an external
program in Python. For longer running commands you want
to be able to see what is happening, so ``subprocess.check_output()``
is not really usable. Falling back to ``os.system()`` with 
the need to ``' '.join()``  the command is not that useful
as you don't have an exit status


``show_output()`` works like ``check_output()`` (including the
``input=`` keyword parameter), but will display the progress to
``stdout``.  The total output is returned to the caller, or passed
back in the Exceptions ``output`` attribute, raised if the return code
from the calling process is non-zero.
