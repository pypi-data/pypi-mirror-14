"""
Save last line to a file specified , builds python script as a stack of commands
i.e. pushes statements to the file in append mode
"""

from IPython.core.magic import Magics, magics_class, line_magic
import os
import io
import logging
from IPython.utils import py3compat
filename='temp.py'
log = logging.getLogger(__name__)
__version__ ='0.2'

@magics_class
class savemagic(Magics): 
  """
  Save last line to a file specified , builds python script as a stack of commands
  i.e. pushes statements to the file in append mode
  """
  @line_magic
  def savef(self, parameter_s=''):
        """Save last line to a file specified , builds python script as a stack of commands
        i.e. pushes statements to the file in append mode

        Usage:\\
          %savef [options]

        Options:

            -s: SET new file to write , otherwise would write to temp.py

            -f: force create new file ( overwrite original to be used with -s )

            -r: use 'raw' input.  By default, the 'processed' history is used,
            so that magics are loaded in their transformed version to valid
            Python.  If this option is given, the raw input as typed as the
            command line is used instead.

        It works in modes either you can start a file or write commands,not both simultaneously
        This function serves as an extension to %save magic function.It writes to
        a file line by line instead of block for rapid development.
        Possible Enhancements (1) merge with save

        """

        opts, args = self.parse_options(parameter_s, 'srf', mode='list')
        set_f= 's' in opts
        raw = 'r' in opts
        force = 'f' in opts
        ext = u'.ipy' if raw else u'.py'
        n = 1
        global filename

        if set_f:
            filename = unquote_filename(args[0])
            if not filename.endswith((u'.py',u'.ipy')):
                filename += ext

        elif args:
            n = int(args[0])

        file_exists = os.path.isfile(filename)

        new_file = (force and file_exists) or not file_exists
        mode = 'w' if new_file else 'a'

        try:
            hist = self.shell.history_manager.get_tail(n, raw)
            cmds = "\n".join([x[2] for x in hist])

        except (TypeError, ValueError) as e:
            print(e.args[0])
            return
        out = py3compat.cast_unicode(cmds)
        with io.open(filename, mode, encoding="utf-8") as f:
            if new_file:
                print('Starting python file: `%s`' % filename)
                f.write(u"# coding: utf-8\n")
            elif not set_f:
                # Only allow setting of file in one command individual files can be pushed later
                f.write(out)
                print(out)
            if not out.endswith(u'\n'):
                f.write(u'\n')

def load_ipython_extension(ipython):
    """
    This is a magic_methods that tells IPython what to do when calling `%Load_ext savef`
    """
    ip = get_ipython()
    ip.register_magics(savemagic)
