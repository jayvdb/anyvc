#!/usr/bin/python
import os, sys


from distutils.core import setup

def read_readme():
    f = open(os.path.join('docs', 'source', 'readme.rst'))
    readme = f.read()
    f.close()
    return readme

#XXX: anyvc should do that itself
def getversion():
    if not os.path.exists('.hg'):
        return None # not in a repository

    # execute hg out of this directory with a custom environment which
    # includes the pure Python modules in mercurial/pure
    pypath = os.environ.get('PYTHONPATH', '')
    purepath = os.path.join('mercurial', 'pure')
    os.environ['PYTHONPATH'] = os.pathsep.join(['mercurial', purepath, pypath])
    os.environ['HGRCPATH'] = '' # do not read any config file
    cmd = '%s hg id -it' % sys.executable

    try:
        l = os.popen(cmd).read().split()
    except OSError, e:
        print "warning: could not establish Mercurial version: %s" % e

    os.environ['PYTHONPATH'] = pypath

    while len(l) > 1 and l[-1][0].isalpha(): # remove non-numbered tags
        l.pop()
    if l:
        version = l[-1] # latest tag or revision number
        if version.endswith('+'):
            version += time.strftime('%Y%m%d')
        return version

version = getversion()
if version:
    f = file("anyvc/__version__.py", "w")
    f.write('# this file is autogenerated by setup.py\n')
    f.write('version = "%s"\n' % version)
    f.close()
else:
    if os.path.exists('anyvc/__version__.py'):
        os.unlink('anyvc/__version__.py')
    version = "unknown"


setup(
    version = version,
    name = 'anyvc',
    packages = [
        'anyvc',
        'anyvc.repository',
        'anyvc.workdir',
    ],
    scripts = ['bin/vc'],

    description='Library to access any version control system.',
    url='http://www.bitbucket.org/RonnyPfannschmidt/anyvc/',
    author='Ronny Pfannschmidt',
    author_email='Ronny.Pfannschmidt@gmx.de',
    long_description=read_readme(),
    classifiers = [
        'Intended Audience :: Developers',
    ],
)
