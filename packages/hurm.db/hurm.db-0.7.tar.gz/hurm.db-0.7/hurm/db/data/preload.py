# -*- coding: utf-8 -*-
# :Project:   hurm
# :Created:   mer 30 dic 2015 18:17:03 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2015, 2016 Lele Gaifax
#

import atexit, datetime, os, re, subprocess, tempfile

import yaml


def time_constructor(loader, node):
    value = loader.construct_scalar(node)
    if value.startswith('T'):
        value = value[1:]
    parts = map(int, value.split(':'))
    return datetime.time(*parts)

yaml.add_constructor('!time', time_constructor)
yaml.add_implicit_resolver('!time', re.compile(r'^T?\d{2}:\d{2}(:\d{2})?$'), ['T'])


def find_in_path(executable):
    path = os.getenv('PATH', os.defpath)
    for d in path.split(os.pathsep):
        epath = os.path.abspath(os.path.join(d, executable))
        if os.path.exists(epath):
            return epath
    return None

def decipher(fname):
    gpg = find_in_path('gpg2') or find_in_path('gpg')
    if not gpg:
        print("ERROR: GPG command line tool is missing!")
        return fname

    print("Input file %s is encrypted, please enter passphrase" % fname)
    with tempfile.NamedTemporaryFile(suffix='.yaml') as f:
        tmpfname = f.name
    subprocess.run([gpg, '-q', '-o', tmpfname, fname], check=True)
    atexit.register(lambda n=tmpfname: os.unlink(n))
    return tmpfname

try:
    fnames
except NameError:
    # ignore, by any chance executed by the test runner
    fnames = []

fnames = [decipher(fname) if fname.endswith('.gpg') else fname for fname in fnames]
