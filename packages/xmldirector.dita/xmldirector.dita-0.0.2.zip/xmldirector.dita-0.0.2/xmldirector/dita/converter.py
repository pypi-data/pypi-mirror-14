
import os
import tempfile
import subprocess
import plac

from xmldirector.dita import util
from xmldirector.dita.logger import LOG
from xmldirector.dita import install


cwd = os.path.abspath(os.path.dirname(__file__))
DITA = os.path.join(cwd, 'converters', 'dita', 'bin', 'dita')
DITAC = os.path.join(cwd, 'converters', 'ditac', 'bin', 'ditac')


def dita2html(ditamap, output=None, converter='dita'):

    if converter not in ('dita', 'ditac'):
        raise ValueError('Unknown DITA converter "{}"'.format(converter))

    if converter == 'dita':

        if not os.path.exists(DITA):
            install.install_converter('dita')

        if not output:
            output = tempfile.mkdtemp()
        cmd = '"{}" -f html5 -i "{}" -o "{}" -Droot-chunk-override=to-content'.format(DITA, ditamap, output)

    else:

        if not os.path.exists(DITAC):
            install.install_converter('ditac')

        cmd = '"{}" -c single  -f xhtml "{}" "{}"'.format(DITAC, output, ditamap)

    LOG.info(cmd)
    status, output = util.runcmd(cmd)
    if status != 0:
        LOG.error(output)
        raise RuntimeError('Execution of "{}" failed (status {})'.format(cmd, status))

    return output


def main():
    import plac; plac.call(dita2html)


if __name__ == '__main__':
    main()
