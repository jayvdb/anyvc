# copyright 2008 by Ronny Pfannschmidt
# license lgpl3 or later

from __future__ import with_statement

from anyvc.metadata import state_descriptions

class WdWrap(object):
    """wraps a vcs"""
    def __init__(self, vc, path):
        self.__path = path
        self.__vc = vc

    def __getattr__(self, name):
        return getattr(self.__vc, name)

    def bpath(self, name):
        return self.__path.join(name)

    def put_files(self, mapping):
        for name, content in mapping.items():
            path = self.__path.ensure(name)
            path.write(content.rstrip() + '\n')

    def has_files(self, *files):
        missing = [name for name in map(self.bpath, files) if not name.check()]
        assert not missing, 'missing %s'%', '.join(missing)
        return not missing

    def delete_files(self, *relpaths):
        for path in relpaths:
            self.bpath(path).remove()

    def check_states(self, exact=True, **kw):
        """takes a mapping of filename-> state
        if exact is true, additional states are ignored
        returns true if all supplied files have the asumed state
        """
        __tracebackhide__ = True
        assert isinstance(exact, bool)
        mapping = dict((rn, state) for state, rns in kw.items() for rn in rns)
        print mapping
        used = set()
        all = set()
        infos = list(self.status())
        print infos
        for info in infos:
            all.add(info.abspath)
            print info
            assert info.state in state_descriptions
            if info.relpath in mapping:
                expected = mapping[info.relpath]
                assert info.state==expected, "%s wanted %s but got %s"%(
                        info.relpath,
                        expected,
                        info.state,
                        )
                used.add(info.relpath)

        untested = set(mapping) - used

        print 'all:', sorted(all)
        print 'used:', sorted(used)
        print 'missing?:', sorted(all - used)
        print 'untested:', sorted(untested)
        assert not untested , 'not all excepted stated occured'


class VcsMan(object):
    """
    utility class to manage the creation of repositories and workdirs
    inside of a specific path (usually the tmpdir funcarg of a test)
    """
    def __init__(self, vc, base, xspec, backend):
        self.remote = xspec is not None
        self.vc = vc
        self.base = base.ensure(dir=True)
        self.xspec = xspec
        self.backend = backend

    def __repr__(self): 
        return '<VcsMan %(vc)s %(base)r>'%vars(self)

    def bpath(self, name):
        """
        :returns: path joined with :attr:`base`
        :rtype: py.path.local
        """
        return self.base.join(name)

    def create_wd(self, workdir, source=None):
        """
        :param workdir: name of the target workdir
        :type workdir: str
        :param source: name of a source repository
        :type source: repo or None

        create a workdir if `source` is given, use it as base
        """
        path = self.bpath(workdir)
        source_path = getattr(source, 'path', None)
        wd = self.backend.Workdir(path, create=True, source=source_path)
        return WdWrap(wd, path)

    def make_repo(self, name):
        """
        :param name: name of the repository to create

        create a repository usin the giv
        """
        return self.backend.Repository(
                path=self.bpath(name),
                create=True)

